from . import ong_calculator as model


def prepare_parser():
    import argparse
    parser = argparse.ArgumentParser()
    return parser


def main(args=None):
    args = prepare_parser().parse_args(args)


if __name__ == "__main__":
    main()
