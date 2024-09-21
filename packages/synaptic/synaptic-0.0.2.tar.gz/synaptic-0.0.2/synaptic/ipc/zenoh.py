import base64
import json
import logging
import logging as log
import time
from pathlib import Path
from pprint import pprint
from typing import Any, Dict, ForwardRef, Generic, TypeVar

import numpy as np
import zenoh
from more_itertools import first
from pydantic import Field, SkipValidation
from rich import console, traceback
from zenoh import Query, Queryable, Queue, Sample, SampleKind, Session, Reply

from synaptic.ipc import IPC, IPCConfig
from synaptic.serialization import serializers
from synaptic.serialization.msgpack import UnpackException
from synaptic.serialization.serializer import Serializer

traceback.install(show_locals=True)

T = TypeVar("T")
logging.basicConfig(level=logging.DEBUG)
   

console = console.Console()


class ZenohIPC(IPC):
    def __init__(self, settings: IPCConfig,*, root_key: str,  mode:str = "peer", protocol: str = "tcp") -> None:


        logging.debug(f"settings: {settings}")
        self.settings = settings
        self.wire = protocol
        self.connection = [{self.wire: str(self.settings.url)}]
        self.mode = mode
        if not isinstance(settings.serializer, Serializer):
            self.serializer: Serializer = serializers[settings.serializer]()
        if not isinstance(self.serializer, Serializer):
            raise ValueError(f"Invalid serializer: {settings.serializer}")
        self.root_key = root_key
        logging.debug(f"root_key: {root_key}")
        logging.debug(f"mode: {mode}")
        self.session: Session | None = None
        self._local_store: Dict[str, Any] = {}
        self.name = "ZenohProtocol" + time.strftime("%Y%m%d-%H%M%S")

    def __dict__(self) -> dict:
        """Return the object config as a dictionary."""
        return {
            "settings": self.settings,
            "mode": self.mode,
            "root_key": self.root_key,
        }

    def listener(self, sample: Sample) -> None:
        """Callback function for incoming samples."""
        key = Path(str(sample.key_expr)).stem
        logging.debug(f"Listener: Received sample: {sample.key_expr} -> {sample.payload}")
        if sample.kind == SampleKind.DELETE():
            self._local_store.pop(key, None)
        else:
            try:
                # Deserialize the incoming sample's payload
                deserialized_data = self.serializer.frombytes(sample.payload)
                self._local_store[key] = deserialized_data
                logging.debug(f"Listener: Deserialized data: {deserialized_data}")
            except (json.JSONDecodeError, UnpackException) as e:
                # Handle the deserialization error and log it
                log.error(f"Error deserializing sample payload: {e}")
                logging.error(f"Received Error {e}: {sample.key_expr}")
    def initialize(self) -> None:
        if self.session is None:
            try:
                log.debug(f"Initializing Zenoh session with config: {self.settings}")
                config = {
                    "mode": self.mode,
                    "connect": self.connection,
                }
            
                self.session = zenoh.open(config)
                self.sub = self.session.declare_subscriber(self.root_key + "/**", self.listener)
                q = self.session.get(self.root_key, zenoh.Queue())
                if next(q, None) is None:
                    logging.info(f"Creating root key: {self.root_key}")

                    # Create the storage key if it doesn't exist
                    self.queryable: Queryable = self.session.declare_queryable(
                        self.root_key + "/**", self.query_handler
                    )

            except Exception as e:
                log.error(f"Error initializing Zenoh session: {e}")
                self.cleanup()
                raise

    def put(self, key: str, value: Any) -> None:
        if self.session is None:
            self.initialize()
        key = f"{self.root_key}/{key}"
        logging.debug(f"putting key {key} value {value}")
        self.session.put(key, self.serializer.tobytes(value))

    def query_handler(self, query: Query) -> None:
        """Only runs if a queryable is declared by this node."""
        logging.debug(f">> [Queryable ] Received Query '{query.selector.key_expr}'")
        key = str(Path(str(query.selector.key_expr)).stem)
        logging.debug(f"key: {str(key)}")
        if key in self._local_store:
            value = self._local_store[key]

            # Ensure the value is serialized before replying
            reply_data = self.serializer(value)

            query.reply(Sample(query.selector.key_expr, reply_data))
            log.debug(f"Replied to query: {query.selector.key_expr} -> {value}")
        elif str(query.selector.key_expr) == self.root_key:
            response = list(self._local_store.keys())
            reply_data = self.serializer.tobytes(response)
            query.reply(Sample(query.selector.key_expr, reply_data))
        else:
            log.error(f"Query not found: {query.selector.key_expr} with key: {key}")
            logging.debug(f"Query {query.selector.key_expr} not found. Only have: {self._local_store.keys()}")

    def get(self, key: str) -> Any:
        try:
            if self.session is None:
                self.initialize()
            key = f"{self.root_key}/{key}"
            q: Queue[Reply] = self.session.get(key, zenoh.Queue())
            sample: Reply = next(q, None)
            if sample is not None and sample.ok is not None:
                logging.debug(f"Got value: {sample.ok.payload}")
                return self.serializer(sample.ok.payload)
            raise KeyError(f"Key not found: {key}")
        except Exception as e:
            log.error(f"Error getting value from Zenoh: {e}")
            raise

    def stream(self, key: str):
        if self.session is None:
            self.initialize()
        key = f"{self.root_key}/{key}"
        queue = Queue()

        def callback(sample: Sample):
            queue.put(self.serializer(sample.value.payload))

        sub = self.session.declare_subscriber(key, callback)

        def generator():
            try:
                while True:
                    yield queue.get()
            finally:
                sub.undeclare()

        return generator()

    def update(self, values: dict) -> None:
        try:
            if self.session is None:
                self.initialize()
            for key, value in values.items():
                self.put(key, value)
        except Exception as e:
            log.error(f"Error updating values in Zenoh: {e}")
            raise

    def delete(self, key: str) -> None:
        try:
            if self.session is None:
                self.initialize()
            key = f"{self.root_key}/{key}"
            q: Queue[zenoh.Reply] = self.session.get(key, zenoh.Queue())
            if next(q, None) is None:
                raise KeyError(f"Key not found: {key}")
            self.session.delete(key)
            log.debug(f"Key removed: {key}")
        except KeyError:
            raise
        except Exception as e:
            log.error(f"Error deleting key from Zenoh: {e}")
            raise KeyError(f"Key not found: {str(key)[:50]  + '...'}")

    def cleanup(self) -> None:
        if self.session is not None:
            try:
                self.sub.undeclare()
                if hasattr(self, "queryable"):
                    self.queryable.undeclare()
                    self.session.delete(self.root_key)
                self.session.close()
                self.session = None
                log.debug("Zenoh session closed successfully")
            except Exception as e:
                log.error(f"Error closing Zenoh session: {e}")
            finally:
                if self.sub is not None:
                    self.sub.undeclare()
                    self.sub = None
                if hasattr(self, "queryable") and self.queryable is not None:
                    self.queryable.undeclare()
                    self.queryable = None
                if self.session is not None:
                    self.session.close()
                    self.session = None
                log.debug("Cleanup completed")
