from typing import Optional, List, Union
from enum import Enum
from pydantic import BaseModel
from .__main__ import compute as _compute


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



# TODO Move into standalone (config) file
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


class UpperLowerBounds(BaseModel):
    low: float
    high: float


class InfrastructurePower(BaseModel):
    operation: UpperLowerBounds
    embodied: UpperLowerBounds

    @classmethod
    def from_tuples(cls, operation, embodied):
        return InfrastructurePower(operation=UpperLowerBounds(low=operation[0], high=operation[1]),
                                   embodied=UpperLowerBounds(low=embodied[0], high=embodied[1]))


class UsersPower(BaseModel):
    operation: float
    embodied: float


class OnlineCalculatorResponse(BaseModel):
    infrastructure: InfrastructurePower
    users: UsersPower
    total_power: UpperLowerBounds
    total_emissions: UpperLowerBounds


def make_device(device):
    if isinstance(device, KnownDevicesEnum):
        device = known_devices[device.value]
    return device


def compute(*args, **kwargs):
    values = _compute(*args, **kwargs)
    result = OnlineCalculatorResponse(
            infrastructure=InfrastructurePower.from_tuples(**values["server"]),
            users=UsersPower(**values["client"]),
            total_power=UpperLowerBounds(**values["total"]),
            total_emissions=UpperLowerBounds(**values["co2"]),
            )
    return result
