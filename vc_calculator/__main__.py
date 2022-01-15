from . import ong_calculator as model


def prepare_parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--upper", default=False, action="store_true")
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

    bandwidth = 7 # Mb/s
    bandwidth *= 3600. / 1024 / 8 # Gb/h
    return devices, bandwidth


def lower_bound_model():
    props = model.ClientProperties
    lifetime_hours = 10 * 260 * 4
    devices = [props.laptop, props.router]
    devices = [Device(d, lifetime_hours) for d in devices]
    bandwidth = 0.128 # Mb/s
    bandwidth *= 3600. / 1024 / 8 # Gb/h
    return devices, bandwidth


def main(args=None):
    args = prepare_parser().parse_args(args)

    devices, bandwidth = upper_bound_model() if args.upper else lower_bound_model()
    result = compute(devices, bandwidth)
    print("CO2 (kg/hour):", result.total_emissions.low, result.total_emissions.high)


def compute(devices, bandwidth):
    server_op = server_power(bandwidth)
    server_em = server_embodied_power(bandwidth)
    client_op = client_power(devices, "power")
    client_em = client_power(devices, "embodied_power")
    total_low = client_op + client_em + server_op[0] + server_em[0]
    total_high = client_op + client_em + server_op[1] + server_em[1]
    co2_low = model.energy_to_co2(total_low)
    co2_high = model.energy_to_co2(total_high)
    return dict(server=dict(operation=server_op, embodied=server_em),
                client=dict(operation=client_op, embodied=client_em),
                total=dict(low=total_low, high=total_high),
                co2=dict(low=co2_low, high=co2_high),
                )


if __name__ == "__main__":
    main()
