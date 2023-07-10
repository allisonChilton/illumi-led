import struct

def remap(value, in_min, in_max, out_min, out_max) -> bytes:
    val = (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return struct.pack('<H', int(val))

def rgb_cmd(r=255, g=0, b=0):
    return bytes([0x5a, 0x07, 0x01, r, g, b])

def mode_cmd(color: bool):
    if not color:
        return bytes([0x5a, 0x06, 0xf2, 0xe8, 0x03])
    else:
        return bytes([0x5a, 0x07, 0xf4])

def warmth_cmd(warmth: float):
    assert 0 <= warmth <= 100
    return bytes([0x5a, 0x06, 0x01]) + remap(warmth, 0, 100, 0x040D, 0x1AC0)

def brightness_cmd(brightness: float):
    assert 0 <= brightness <= 100
    # brightness = 100 - brightness
    brightness = remap(brightness, 0, 100, 0x0, 0x0FFF)
    data = bytes([0x5a, 0x03, 0x01]) + brightness
    return data

def saturation_cmd(sat: float):
    assert 0 <= sat <= 100
    sat = 100 - sat
    return bytes([0x5a, 0x07, 0x03, 0, sat]) + remap(sat, 0, 100, 0x0, 0x0FFF)

def on_off_cmd(on: bool):
    return bytes([0x5a, 0x01, 0x02, 0xFF if on else 0x00])

def scene_cmd(scene: int):
    assert 0 <= scene <= 9
    return bytes([0x5a, 0x04, 0x01, scene])

def speed_cmd(speed: float):
    assert 0 <= speed <= 100
    return bytes([0x5a, 0x04, 0x04, speed, 0]) + remap(speed, 0, 100, 0x0, 0x00FF)

def mic_cmd(mode: int):
    assert 1 <= mode <= 4
    return bytes([0x5a, 0x09, 0x03, mode])

def mic_sensitivity_cmd(sensitivity: float):
    assert 0 <= sensitivity <= 100
    data = bytes([0x5a, 0x09, 0x01]) + remap(sensitivity, 0, 100, 0x0, 0x0FFF)
    return data
