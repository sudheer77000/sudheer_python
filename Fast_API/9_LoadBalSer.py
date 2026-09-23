import asyncio
import time
from datetime import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get("/test/{request_id}")
async def test(request_id: int):

    # Start time
    start_perf = time.perf_counter()
    start_time = datetime.now()

    print(
        f"[START] request_id={request_id} "
        f"time={start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}"
    )

    # Simulate slow I/O operation
    await asyncio.sleep(2)

    # End time
    end_perf = time.perf_counter()
    end_time = datetime.now()

    elapsed = end_perf - start_perf

    print(
        f"[END]   request_id={request_id} "
        f"time={end_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]} "
        f"elapsed={elapsed:.3f} seconds"
    )

    return {
        "request_id": request_id,
        "message": "Done",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "elapsed_seconds": round(elapsed, 3),
    }
