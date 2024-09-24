from obelisk import Obelisk


def test_health_check():
    app = Obelisk()
    assert hasattr(app, "__call__")
