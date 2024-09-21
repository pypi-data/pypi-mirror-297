import traceback
from typing import Any

import msgpack
from msgpack.exceptions import PackException, UnpackException

from synaptic.serialization.serializer import Serializer
import logging

class MsgPackSerializer(Serializer):
    def tobytes(self, data: Any) -> bytes:
        """Serialize Python data into MessagePack format (bytes)."""
        logging.info(f"serializing data {data}")
        try:
            # Ensure strings are encoded as UTF-8, not binary
            out = msgpack.packb(data, use_bin_type=True)
            logging.info(f"serialized data {out}")
            return out
        except PackException as e:
            traceback.print_exc()
            raise ValueError(f"Error packing data: {e}")

    def frombytes(self, data: bytes) -> Any:
        """Deserialize MessagePack bytes back into Python objects, ensuring correct handling of strings."""
        try:
            logging.info(f"deserializing data in {data}")
            out = msgpack.unpackb(data, raw=False) 
            logging.info(f"deserialized data {out}")
            return out
            # Ensure that binary data is decoded back into strings
     # raw=False ensures binary strings are decoded to UTF-8 strings
        except UnpackException as e:
            traceback.print_exc()
            raise ValueError(f"Error unpacking data: {e}")
