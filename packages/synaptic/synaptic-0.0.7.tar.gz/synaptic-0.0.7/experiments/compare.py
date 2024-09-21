import asyncio
import torch
import trio
import anyio
from time import time
from concurrent.futures import ThreadPoolExecutor
from arq import create_pool, Worker
from arq.jobs import Job
from arq.connections import RedisSettings
from TTS.api import TTS
from pyannote.audio import Pipeline
from scipy.io import wavfile
import numpy as np
from rich.console import Console
from rich.table import Table
from multiprocessing import Process, Queue
from random import shuffle
from sys import argv
device = "cuda" if torch.cuda.is_available() else "cpu"

# Initialize models
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=device != "cpu")
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")

# Rich Console
console = Console()

def tts_generation(text):
    console.print("Starting TTS generation...", style="bold yellow")
    sentences = text.split(". ")
    complete_audio = b''
    for sentence in sentences:
        if sentence:
            audio_array = np.array(tts.tts(sentence))
            audio_array = (audio_array * 32767).astype(np.int16)
            complete_audio += audio_array.tobytes()
    return complete_audio

def diarize_audio(audio_file):
    console.print("Starting diarization...", style="bold yellow")
    diarization = pipeline(audio_file)
    return diarization

def sync_warmup():
    """Synchronous warmup to preload models and libraries."""
    console.print("Starting warmup...", style="bold blue")
    complete_audio = tts_generation("Sample text for benchmarking.")
    wavfile.write("output_warmup.wav", tts.synthesizer.output_sample_rate, np.frombuffer(complete_audio, dtype=np.int16))
    print(pipeline("output_warmup.wav"))
    console.print("Warmup completed.", style="bold blue")

def timeit(func, is_trio=False):
    start_time = time()
    if is_trio:
        trio.run(func)
    else:
        asyncio.run(func())
    end_time = time()
    return end_time - start_time

# Asyncio + ThreadPoolExecutor
async def main_asyncio():
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        complete_audio = await loop.run_in_executor(pool, tts_generation, "Sample text for benchmarking.")
        wavfile.write("output_asyncio.wav", tts.synthesizer.output_sample_rate, np.frombuffer(complete_audio, dtype=np.int16))
        await loop.run_in_executor(pool, pipeline, "output_asyncio.wav")

# Trio Implementation
async def main_trio():
    complete_audio = await trio.to_thread.run_sync(tts_generation, "Sample text for benchmarking.")
    wavfile.write("output_trio.wav", tts.synthesizer.output_sample_rate, np.frombuffer(complete_audio, dtype=np.int16))
    await trio.to_thread.run_sync(pipeline, "output_trio.wav")

# AnyIO Implementation
async def main_anyio():
    complete_audio = await anyio.to_thread.run_sync(tts_generation, "Sample text for benchmarking.")
    wavfile.write("output_anyio.wav", tts.synthesizer.output_sample_rate, np.frombuffer(complete_audio, dtype=np.int16))
    await anyio.to_thread.run_sync(pipeline, "output_anyio.wav")

# ARQ Implementation
async def tts_generation_arq(ctx, text: str) -> bytes:
    return tts_generation(text)

async def save_audio_arq(ctx, audio: bytes) -> str:
    file_name = "output_arq.wav"
    wavfile.write(file_name, tts.synthesizer.output_sample_rate, np.frombuffer(audio, dtype=np.int16))
    return file_name

async def diarize_audio_arq(ctx, audio_file: str) -> str:
    diarization = pipeline(audio_file)
    return str(diarization)

async def run_arq_pipeline():
    redis = await create_pool(RedisSettings())
    text = "Sample text for benchmarking."

    # Queue the TTS generation task
    job: Job = await redis.enqueue_job('tts_generation_arq', text)
    audio_bytes = await job.result(timeout=300)

    # Queue the task to save the audio
    save_job: Job = await redis.enqueue_job('save_audio_arq', audio_bytes)
    audio_file_path = await save_job.result(timeout=300)

    # Queue the diarization task
    diarization_job: Job = await redis.enqueue_job('diarize_audio_arq', audio_file_path)
    diarization_result = await diarization_job.result(timeout=300)

    console.print("Diarization result:", diarization_result)

def start_arq_worker():
    worker = Worker(
        functions=[tts_generation_arq, save_audio_arq, diarize_audio_arq],
        redis_settings=RedisSettings()
    )
    worker.run()



def benchmark_arq(q: Queue):
    time_taken = timeit(lambda: asyncio.run(run_arq_pipeline()))
    q.put(("ARQ", time_taken))

def benchmark_asyncio(q: Queue):
    time_taken = timeit(main_asyncio)
    q.put(("Asyncio + ThreadPoolExecutor", time_taken))

def benchmark_trio(q: Queue):
    time_taken = timeit(main_trio, is_trio=True)
    q.put(("Trio", time_taken))

def benchmark_anyio(q: Queue):
    time_taken = timeit(main_anyio)
    q.put(("AnyIO", time_taken))

if __name__ == "__main__":
    console.print("Starting benchmarking...", style="bold blue")
    if len(argv) > 1 and argv[1] in {"-h", "--help", "help"}:
        console.print("Usage: python compare.py [trials]", style="bold white")
        exit()

    trials = int(argv[1]) if len(argv) > 1 else 5

    # Run in separate processes after warmup for fair comparison.
    # # Start ARQ worker process
    # worker_process = Process(target=start_arq_worker)
    # worker_process.start()

    processes = [
        {"name": "Asyncio + ThreadPoolExecutor", "func": benchmark_asyncio},
        {"name": "Trio", "func": benchmark_trio},
        {"name": "AnyIO", "func": benchmark_anyio},
        # {"name": "ARQ", "func": benchmark_arq},
    ]
    trial_results = {
        "Asyncio + ThreadPoolExecutor": [],
        "Trio": [],
        "AnyIO": [],
        # "ARQ": []
    }

    for i in range(trials):
        sync_warmup()
        console.print(f"Trial {i + 1} of {trials}\n", style="bold yellow")

        # Run the processes in random order
        q = Queue()
        shuffle(processes)
        for process in processes:
            p = Process(target=process["func"], args=(q,))
            p.start()
            p.join()
        try:
            while not q.empty():
                model, time_taken = q.get()
                trial_results[model].append(time_taken)
        except KeyboardInterrupt as e:
            raise e


    results = {model: sum(times) / len(times) for model, times in trial_results.items()}
    # # Stop the ARQ worker process
    # worker_process.terminate()

    # Create a table for results
    table = Table(title="Benchmark Results")

    table.add_column("Concurrency Model", justify="left", style="cyan", no_wrap=True)
    table.add_column("Time Taken", justify="right", style="magenta")

    for model, time_taken in results.items():
        table.add_row(model, f"{time_taken:.4f} seconds")

    console.print(table)