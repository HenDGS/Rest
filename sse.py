import asyncio
import time
import pandas as pd
import uvicorn
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from datetime import datetime

app = FastAPI()


def notification2_data():
    stock_movement = pd.read_csv('csvs/stock_control.csv')
    products = pd.read_csv('csvs/products.csv')

    products_with_negative_movement = stock_movement.loc[stock_movement['quantity'] < 0]
    products_with_negative_movement_in_the_last_3_days = products_with_negative_movement.loc[
        products_with_negative_movement['date'] <= (datetime.now() - pd.Timedelta(days=1)).strftime("%d/%m/%Y")]
    products_without_movement = products.loc[~products['code'].isin(
        products_with_negative_movement_in_the_last_3_days['code'])]

    products_with_negative_movement.loc[:, 'date'] = pd.to_datetime(products_with_negative_movement['date'],
                                                                    format="%d/%m/%Y")

    today = datetime.today()
    three_days_ago = today - pd.Timedelta(days=7)

    products_with_negative_movement_in_last_three_days = products_with_negative_movement.loc[
        products_with_negative_movement['date'] >= three_days_ago]
    products_without_movement_in_last_three_days = products_without_movement.loc[
        ~products_without_movement['code'].isin(products_with_negative_movement_in_last_three_days['code'])]

    return products_without_movement_in_last_three_days.to_string(index=False)


@app.get("/")
async def root():
    return {"message": "Hello World"}


STREAM_DELAY = 10  # second
RETRY_TIMEOUT = 15000  # milisecond


@app.get('/stream')
async def message_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break

            # read file "products.csv" and see any if any product quantity is lower than its stock
            products = pd.read_csv('csvs/products.csv')

            for index, row in products.iterrows():
                if row['quantity'] < row['stock']:
                    yield {'event': 'message', 'data': 'Product ' + row['name'] + ' is below its minimum stock'}

            data2 = "Products that haven't been sold in the last 3 days" + notification2_data()

            if data2 != '':
                yield {'event': 'message', 'data': data2}

            # yield {'event': 'message', 'data': 'notification2 hello world'}

            # await asyncio.sleep(STREAM_DELAY)
            time.sleep(STREAM_DELAY)

    return EventSourceResponse(event_generator())


if __name__ == "__main__":
    uvicorn.run(app='sse:app', host="127.0.0.1", port=8001, log_level="info")
