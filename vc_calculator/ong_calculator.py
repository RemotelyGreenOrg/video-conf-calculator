"""
Based on http://www2.eet.unsw.edu.au/~vijay/pubs/jrnl/14comcomVC.pdf
"""
import math
from collections import namedtuple


class ServerProperties():
    """ from section 3.1
    """
    internet_power_low = 43 # GW
    internet_power_high = 72 # GW
    internet_traffic = 500. * 1024**2 # GB / day

    energy_intensity_low = internet_power_low * 1e6 / (internet_traffic / 24.) # kWh/GB
    energy_intensity_high = internet_power_high * 1e6 / (internet_traffic / 24.) # kWh/GB

    video_bandwidth_low = 0.045 # GB/h
    video_bandwidth_high = 4.5 # GB/h

    power_video_low = energy_intensity_high * video_bandwidth_low
    power_video_high = energy_intensity_high * video_bandwidth_high

    embodied_power_low = 33.2 # GW
    embodied_power_high = 70.7 # GW

    embodied_energy_intensity_low = embodied_power_low * 1e6 / (internet_traffic / 24.) # kWh/GB
    embodied_energy_intensity_high = embodied_power_high * 1e6 / (internet_traffic / 24.) # kWh/GB


Device = namedtuple("Device", "power manufacture_energy manufacture_carbon")
class ClientProperties():
    """ From section 3.2 and 3.3, table 1
    Power in Watts,
    manufacture_energy (Emobdied energy) in MJ / unit
    manufacture_carbon (Carbon emission) in kgCO2e
    """
    laptop = Device(40, 1362, 227)
    personal_comp = Device(150, 2100, 350)

    @staticmethod
    def plasma(area):
        return Device(20 + area * 203,
                      5096 * area,
                      849 * area)

    @staticmethod
    def ledlcd(area):
        return Device(20 + area * 172,
                      3218 * area, 
                      536 * area)

    projector = Device(135, 384, 64)

    high_codec = Device(80, 1120, 187)
    low_codec = Device(26, 364, 61)

    camera = Device(9.5, 120, 20)
    speaker = Device(4.1, 374, 62)
    microphone = Device(2.5, 187, 31)

    router = Device(20, 1000, 167)


def energy_to_co2(energy, location=None):
    return energy * 160 * 1e-6 * 3600
