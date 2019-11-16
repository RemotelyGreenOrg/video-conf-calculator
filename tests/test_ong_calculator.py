import pytest
from vc_calculator import ong_calculator as ong


def test_server_power():
    vals = ong.ServerProperties()
    assert vals.energy_intensity_high == pytest.approx(3.61, rel=0.1)
    assert vals.energy_intensity_low == pytest.approx(2.17, rel=0.1)

    assert vals.power_video_low == pytest.approx(0.135, rel=0.1)
    assert vals.power_video_high == pytest.approx(13.5, rel=0.1)
