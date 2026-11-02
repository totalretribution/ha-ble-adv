"""eWeLink Codec."""

from __future__ import annotations

from binascii import crc_hqx
from typing import ClassVar

from .const import (
    ATTR_BR,
    ATTR_CMD,
    ATTR_CMD_BR_DOWN,
    ATTR_CMD_BR_UP,
    ATTR_CMD_CT_DOWN,
    ATTR_CMD_CT_UP,
    ATTR_CMD_PAIR,
    ATTR_CMD_TIMER,
    ATTR_CMD_TOGGLE,
    ATTR_COLD,
    ATTR_CT_REV,
    ATTR_DIR,
    ATTR_ON,
    ATTR_OSC,
    ATTR_PRESET,
    ATTR_PRESET_BREEZE,
    ATTR_PRESET_SLEEP,
    ATTR_SPEED,
    ATTR_STEP,
    ATTR_TIME,
    ATTR_WARM,
)
from .models import (
    BleAdvCodec,
    BleAdvConfig,
    BleAdvEncCmd,
    CTLightCmd,
    DeviceCmd,
    Fan6SpeedCmd,
    FanCmd,
    LightCmd,
    Trans,
)
from .models import EncoderMatcher as EncCmd
from .utils import crc16_le


class EWeLinkCodec(BleAdvCodec):
    """eWeLink codec."""

    XOR_MATRIX: ClassVar[bytes] = bytes([0x41, 0x92, 0x53, 0x2A, 0xFC, 0xAB, 0xCE, 0x26, 0x0D, 0x1E, 0x99, 0x78, 0x00, 0x22, 0x99, 0xDE])

    _len = 18
    _seed_max = 0xFE

    def _crc(self, buffer: bytes | bytearray) -> int:
        return crc_hqx(buffer, 0x5555)

    def decrypt(self, buffer: bytearray) -> bytearray | None:
        """Decrypt / unwhiten an incoming raw buffer into a readable buffer."""
        data = bytearray(x ^ self.XOR_MATRIX[i] for i, x in enumerate(buffer[:-2]))
        data[7:-1] = [x ^ data[-1] for x in data[7:-1]]
        if not self.is_eq(int.from_bytes(buffer[-2:], "little"), self._crc(data), "crc"):
            return None
        return data

    def encrypt(self, buffer: bytearray) -> bytearray:
        """Encrypt / whiten a readable buffer."""
        crc = self._crc(buffer).to_bytes(2, "little")
        buffer[7:-1] = [x ^ buffer[-1] for x in buffer[7:-1]]
        buffer[:] = [x ^ self.XOR_MATRIX[i] for i, x in enumerate(buffer)]
        return buffer + crc

    def convert_to_enc(self, decoded: bytearray) -> tuple[BleAdvEncCmd | None, BleAdvConfig | None]:
        """Convert a readable buffer into an encoder command and a config."""
        conf = BleAdvConfig()
        conf.id = int.from_bytes(decoded[1:5], "little")
        conf.tx_count = decoded[0]
        conf.seed = decoded[13]
        return BleAdvEncCmd(decoded[6], decoded[7], decoded[8], decoded[9], decoded[10]), conf

    def convert_from_enc(self, enc_cmd: BleAdvEncCmd, conf: BleAdvConfig) -> bytearray:
        """Convert an encoder command and a config into a readable buffer."""
        uid = conf.id.to_bytes(4, "little")
        return bytearray([conf.tx_count, *uid, 0x01, enc_cmd.cmd, enc_cmd.param, enc_cmd.arg0, enc_cmd.arg1, enc_cmd.arg2, 0x00, 0x00, conf.seed])


class EWeLinkRemoteCodec(BleAdvCodec):
    """eWeLink 2.4G CCT panel remote codec (e.g. LED Driver 50W-2.4G-CCT, EHC_050S105DN_TP02).

    Not whitened. After the header, the 16 bytes are:
        0x00 0x00 | tx_count | id (2, as printed on the remote) | 0x08 0x05 | group (index) | cmd | 0x00 x 6 | seed
    followed by a CRC16 (poly 0x8408 reflected, init 0xAAAA) of these 16 bytes, little endian.
    The lights only accept it from the remote's fixed random address, on channel 37.
    """

    ID_SUFFIX: ClassVar[bytes] = bytes([0x08, 0x05])

    _len = 18
    _tx_max = 256
    _seed_max = 0xFF
    duration = 100
    interval = 20
    repeat = 25
    own_address = "66:55:44:33:22:11"
    channel_map = 0x01

    def _crc(self, buffer: bytes | bytearray) -> int:
        return crc16_le(buffer, 0xAAAA, ref_in=False, ref_out=False)

    def decrypt(self, buffer: bytearray) -> bytearray | None:
        """Check the CRC and remove it."""
        if not self.is_eq(int.from_bytes(buffer[-2:], "little"), self._crc(buffer[:-2]), "crc"):
            return None
        return buffer[:-2]

    def encrypt(self, buffer: bytearray) -> bytearray:
        """Add the CRC."""
        return buffer + self._crc(buffer).to_bytes(2, "little")

    def convert_to_enc(self, decoded: bytearray) -> tuple[BleAdvEncCmd | None, BleAdvConfig | None]:
        """Convert a readable buffer into an encoder command and a config."""
        if not self.is_eq_buf(self.ID_SUFFIX, decoded[3:5], "ID suffix"):
            return None, None
        conf = BleAdvConfig()
        conf.tx_count = decoded[0]
        conf.id = int.from_bytes(decoded[1:3], "big")
        conf.index = decoded[5]
        conf.seed = decoded[13]
        return BleAdvEncCmd(decoded[6]), conf

    def convert_from_enc(self, enc_cmd: BleAdvEncCmd, conf: BleAdvConfig) -> bytearray:
        """Convert an encoder command and a config into a readable buffer."""
        uid = conf.id.to_bytes(2, "big")
        return bytearray([conf.tx_count, *uid, *self.ID_SUFFIX, conf.index, enc_cmd.cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, conf.seed])


TRANSLATORS = [
    Trans(DeviceCmd().act(ATTR_CMD, ATTR_CMD_PAIR), EncCmd(0x13).eq("param", 3)).no_direct(),
    Trans(DeviceCmd().act(ATTR_ON, False), EncCmd(0x11).eq("param", 0).eq("arg0", 2).eq("arg1", 0)).no_direct(),
    Trans(DeviceCmd().act(ATTR_CMD, ATTR_CMD_TIMER), EncCmd(0x11).eq("param", 0).eq("arg0", 2).min("arg1", 1))
    .copy(ATTR_TIME, "arg1", 1 / 300)
    .no_direct(),
    Trans(LightCmd().act(ATTR_ON, True), EncCmd(0x11).eq("param", 2).eq("arg0", 1)).no_reverse(),
    Trans(LightCmd().act(ATTR_ON, False), EncCmd(0x11).eq("param", 2).eq("arg0", 1)).no_reverse(),
    Trans(LightCmd().act(ATTR_ON, ATTR_CMD_TOGGLE), EncCmd(0x11).eq("param", 2).eq("arg0", 1)).no_direct(),
    Trans(LightCmd(1).act(ATTR_ON, True), EncCmd(0x11).eq("param", 2).eq("arg0", 4)).no_reverse(),
    Trans(LightCmd(1).act(ATTR_ON, False), EncCmd(0x11).eq("param", 2).eq("arg0", 4)).no_reverse(),
    Trans(LightCmd(1).act(ATTR_ON, ATTR_CMD_TOGGLE), EncCmd(0x11).eq("param", 2).eq("arg0", 4)).no_direct(),
    Trans(CTLightCmd().act(ATTR_COLD).act(ATTR_WARM), EncCmd(0x12).eq("param", 0)).copy(ATTR_BR, "arg0", 100).copy(ATTR_CT_REV, "arg1", 100),
    Trans(CTLightCmd().act(ATTR_COLD).act(ATTR_WARM), EncCmd(0x12).min("param", 1).max("param", 2))
    .copy(ATTR_BR, "arg0", 100)
    .copy(ATTR_CT_REV, "arg1", 100)
    .no_direct(),
    Trans(CTLightCmd().act(ATTR_CMD, ATTR_CMD_BR_UP).eq(ATTR_STEP, 0.05), EncCmd(0x12).eq("param", 5)).no_direct(),
    Trans(CTLightCmd().act(ATTR_CMD, ATTR_CMD_BR_DOWN).eq(ATTR_STEP, 0.05), EncCmd(0x12).eq("param", 6)).no_direct(),
    Trans(FanCmd().act(ATTR_DIR, True), EncCmd(0x43).eq("param", 0)),  # Forward
    Trans(FanCmd().act(ATTR_DIR, False), EncCmd(0x43).eq("param", 1)),  # Reverse
    Trans(FanCmd().act(ATTR_OSC, ATTR_CMD_TOGGLE), EncCmd(0x40).eq("param", 2)),  # Oscillation TOGGLE
    Trans(FanCmd().act(ATTR_PRESET, ATTR_PRESET_BREEZE), EncCmd(0x42).eq("param", 1).eq("arg0", 0)),
    Trans(FanCmd().act(ATTR_PRESET, ATTR_PRESET_SLEEP), EncCmd(0x42).eq("param", 1).eq("arg0", 1)),
    Trans(Fan6SpeedCmd().act(ATTR_ON, True).act(ATTR_SPEED), EncCmd(0x15)).copy(ATTR_SPEED, "param"),
    Trans(Fan6SpeedCmd().act(ATTR_ON, False), EncCmd(0x11).eq("param", 0).eq("arg0", 0)),
]

# The lights have no explicit ON / OFF: 0x01 (power) and 0x09 (group 1) toggle them.
# 0x02 (night), 0x03 / 0x08 (max brightness, max cold) and 0x0A (group 2) are only seen as events.
REMOTE_TRANSLATORS = [
    Trans(LightCmd().act(ATTR_ON, True), EncCmd(0x01)).no_reverse(),
    Trans(LightCmd().act(ATTR_ON, False), EncCmd(0x01)).no_reverse(),
    Trans(LightCmd().act(ATTR_ON, ATTR_CMD_TOGGLE), EncCmd(0x01)).no_direct(),
    Trans(LightCmd().act(ATTR_ON, ATTR_CMD_TOGGLE), EncCmd(0x09)).no_direct(),
    Trans(CTLightCmd().act(ATTR_CMD, ATTR_CMD_BR_UP).eq(ATTR_STEP, 0.1), EncCmd(0x04)).no_direct(),
    Trans(CTLightCmd().act(ATTR_CMD, ATTR_CMD_BR_DOWN).eq(ATTR_STEP, 0.1), EncCmd(0x05)).no_direct(),
    Trans(CTLightCmd().act(ATTR_CMD, ATTR_CMD_CT_DOWN).eq(ATTR_STEP, 0.1), EncCmd(0x06)).no_direct(),
    Trans(CTLightCmd().act(ATTR_CMD, ATTR_CMD_CT_UP).eq(ATTR_STEP, 0.1), EncCmd(0x07)).no_direct(),
]

STDHDR = [0xEE, 0x1B, 0xC8, 0x78, 0xF6, 0x4A]
CODECS = [
    EWeLinkCodec().id("ewelink_v0").header([0xFF, 0xFF, *STDHDR]).ble(0x01, 0xFF).prefix([0x05, 0x02]).add_translators(TRANSLATORS),
    EWeLinkCodec().id("ewelink_v0", "p3").header([0xFF, 0x00, *STDHDR]).ble(0x01, 0xFF).prefix([0x05, 0x03]).add_translators(TRANSLATORS),
    EWeLinkCodec().id("ewelink_v0", "r").header([0xFF, 0xFF, *STDHDR]).ble(0x02, 0x05).prefix([0x00, 0x02]).add_translators(TRANSLATORS),
    EWeLinkRemoteCodec().id("ewelink_tp02").header([0x89, 0x8A, *STDHDR]).ble(0x02, 0x05).prefix([0x00, 0x00]).add_translators(REMOTE_TRANSLATORS),
]
