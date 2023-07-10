import asyncio
import logging
import enum

from nordic_uart import NordicUARTClient
from illumi_led import cmd

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class IllumiLEDModes(enum.Enum):
    """The modes of the Illumi LED light strip."""
    RGB = 0
    WHITE = 1
    SCENE = 2
    MIC = 3

class IllumiLEDClient(NordicUARTClient):
    """A client for the Illumi LED light strip."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mode = IllumiLEDModes.RGB
        self._warmth = 0
        self._brightness = 100
        self._saturation = 100
        self._on = True
        self._scene = 0
        self._speed = 100
        self._mic = 1

    def _send(self, data):
        """Send data to the light strip."""
        self.task_write(data)

    def _update(self):
        """Send all current settings to the light strip."""
        if self.mode == IllumiLEDModes.RGB:
            self._send(cmd.mode_cmd(True))
            self._send(cmd.saturation_cmd(self._saturation))
        elif self.mode == IllumiLEDModes.WHITE:
            self._send(cmd.mode_cmd(False))
            self._send(cmd.warmth_cmd(self._warmth))
        elif self.mode == IllumiLEDModes.SCENE:
            self._send(cmd.scene_cmd(self._scene))
            self._send(cmd.speed_cmd(self._speed))
        elif self.mode == IllumiLEDModes.MIC:
            self._send(cmd.mic_cmd(self._mic))

        self._send(cmd.brightness_cmd(self._brightness))
        self._send(cmd.on_off_cmd(self._on))

    def set_color(self, r, g, b):
        """Set the color of the light strip."""
        self._mode = IllumiLEDModes.RGB # no need to send mode_cmd, it's implied by rgb_cmd
        r = int(round(r))
        g = int(round(g))
        b = int(round(b))
        logger.debug("Setting color to %d, %d, %d", r, g, b)
        self._send(cmd.rgb_cmd(r, g, b))
    
    def set_warmth(self, warmth):
        """Set the warmth of the light strip."""
        self._mode = IllumiLEDModes.WHITE 
        self._warmth = warmth
        self._update()

    @property
    def mode(self):
        """The mode of the light strip."""
        return self._mode
    
    @mode.setter
    def mode(self, value: IllumiLEDModes | int):
        if isinstance(value, int):
            value = IllumiLEDModes(value)
        self._mode = value
        self._update()

    @property
    def warmth(self):
        """The warmth of the light strip (0-100)."""
        return self._warmth

    @warmth.setter
    def warmth(self, value):
        self._warmth = value
        self._update()

    @property
    def brightness(self):
        """The brightness of the light strip (0-100)."""
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness = value
        self._update()

    @property
    def saturation(self):
        """The saturation of the light strip (0-100)."""
        return self._saturation

    @saturation.setter
    def saturation(self, value):
        self._saturation = value
        self._update()

    @property
    def on(self):
        """Whether the light strip is on."""
        return self._on

    @on.setter
    def on(self, value):
        self._on = value
        self._update()

    @property
    def off(self):
        return not self.on

    @off.setter
    def off(self, value):
        self.on = not value

    @property
    def scene(self):
        """The scene of the light strip (0-9)."""
        return self._scene
    
    @scene.setter
    def scene(self, value):
        self._mode = IllumiLEDModes.SCENE
        self._scene = value
        self._update()
    
    @property
    def speed(self):
        """The speed of the light strip (0-100)."""
        return self._speed
    
    @speed.setter
    def speed(self, value):
        self._speed = value
        self._update()

    @property
    def mic(self):
        """The mic mode of the light strip (1-4)."""
        return self._mic
    
    @mic.setter
    def mic(self, value):
        self._mode = IllumiLEDModes.MIC
        self._mic = value
        self._update()

    