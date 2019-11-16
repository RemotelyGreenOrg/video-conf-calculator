from . import ong_calculator as model


def prepare_parser():
    import argparse
    parser = argparse.ArgumentParser()
    return parser


class Device():
    def __init__(self, device, lifetime_op_hours, use_factor=1):
        self.device = device
        self.lifetime_op_hours = lifetime_op_hours
        self.use_factor = use_factor

    @property
    def power(self):
        return self.device.power * self.use_factor * 1e-3

    @property
    def embodied_power(self):
        lifetime = self.lifetime_op_hours * 3600
        return self.use_factor * self.device.manufacture_energy / lifetime * 1e3

    @property
    def total_power(self):
        return self.power + self.embodied_power


def server_power(bandwidth):
    # kWh / GB
    power_low =  model.ServerProperties.energy_intensity_low
    power_high =  model.ServerProperties.energy_intensity_high
    return bandwidth * power_low, bandwidth * power_high


def server_embodied_power(bandwidth):
    power_low = model.ServerProperties.embodied_energy_intensity_low
    power_high = model.ServerProperties.embodied_energy_intensity_high
    return bandwidth * power_low, bandwidth * power_high


def client_power(devices, attr="total_power"):
    power = sum(map(lambda x: getattr(x, attr), devices))
    return power


def upper_bound_model():
    props = model.ClientProperties
    lifetime_hours = 5 * 260 * 4
    screen_hypot = 65 * 0.025
    screen_area = screen_hypot ** 2 / (16./9 + 9./16)
    devices = [props.camera, props.plasma(screen_area), props.microphone] * 3
    devices += [props.high_codec, props.speaker, props.personal_comp]
    devices = [Device(d, lifetime_hours) for d in devices]
    devices += [Device(props.router, 2 * lifetime_hours)]
    return devices


def main(args=None):
    args = prepare_parser().parse_args(args)

    devices = upper_bound_model()
    bandwidth = 7 # Mb/s
    bandwidth *= 3600. / 1024 / 8 # Gb/h
    server_op = server_power(bandwidth)
    server_em = server_embodied_power(bandwidth)
    client_op = client_power(devices, "power")
    client_em = client_power(devices, "embodied_power")
    print("Embodied", client_em, server_em, [s + client_em for s in server_em])
    print("Operation", client_op, server_op, [s + client_op for s in server_op])


if __name__ == "__main__":
    main()
