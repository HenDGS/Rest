import asyncio
import uvicorn
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


STREAM_DELAY = 10  # second
RETRY_TIMEOUT = 15000  # milisecond


@app.get('/stream')
async def message_stream(request: Request):
    async def event_generator():
        while True:
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break

            yield {'event': 'message', 'data': 'hello world'}

            await asyncio.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run(app='sse:app', host="127.0.0.1", port=8001, log_level="info")
