from fastapi import FastAPI
from interface import compute, make_device, OnlineDetails


app = FastAPI()


@app.post("/online")
def calculate(body: OnlineDetails):
    devices = body.device_list
    devices = [make_device(d) for d in devices]
    results = compute(devices, body.bandwidth)
    return results
