from typing import Optional, List, Union
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from vc_calculator.__main__ import compute, Device


class HardwareDetails(BaseModel):
    wall_power: float
    manufacture_energy: float
    lifetime_op_hours: float = 5000
    use_factor: float = 0.8

    @property
    def power(self):
        return self.wall_power * self.use_factor * 1e-3

    @property
    def embodied_power(self):
        lifetime = self.lifetime_op_hours * 3600
        return self.use_factor * self.manufacture_energy / lifetime * 1e3

    @property
    def total_power(self):
        return self.power + self.embodied_power



known_devices = dict(
                        one=HardwareDetails(wall_power=4., manufacture_carbon=5.,manufacture_energy=7.),
                        pc=HardwareDetails(wall_power=46., manufacture_carbon=53.,manufacture_energy=7.),
                    )

class AutoName(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name

KnownDevicesEnum = AutoName("KnownDevicesEnum", list(known_devices.keys()))


class ConnectionTypes(str, Enum):
    fiveG = "5G"
    cable = "cable"
    wifi ="wi-fi"


class OnlineDetails(BaseModel):
    location: str
    device_list: List[Union[HardwareDetails, KnownDevicesEnum]]
    bandwidth: float
    total_participants: int
    software: Optional[str]
    connection: Optional[ConnectionTypes]


def make_device(device):
    if isinstance(device, KnownDevicesEnum):
        device = known_devices[device.value]
    return device


app = FastAPI()


@app.get("/")
def root():
    return {"Hello": "World!"}


@app.post("/online")
def calculate(body: OnlineDetails):
    devices = body.device_list
    devices = [make_device(d) for d in devices]
    #body.device_list = devices
    results = compute(devices, body.bandwidth)
    return results
