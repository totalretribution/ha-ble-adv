# ruff: noqa: S101
"""eWeLink Unit Tests."""

import pytest
from ble_adv.codecs.const import ATTR_ON, LIGHT_TYPE
from ble_adv.codecs.models import BleAdvAdvertisement, BleAdvCodec, BleAdvConfig, BleAdvEncCmd, BleAdvEntAttr

from . import CODECS, _TestEncoderBase, _TestEncoderFull


@pytest.mark.parametrize(
    _TestEncoderBase.PARAM_NAMES,
    [
        ("ewelink_v0/p3", 0xFF, "FF00EE1BC878F64A4491D2E2C76D48546D6EEA0B7351EAADACB1"),
        ("ewelink_v0/r", 0x05, "FFFFEE1BC878F64A4190F63AFFADD337080D8968103289CE5D7D"),
        ("ewelink_tp02", 0x05, "898AEE1BC878F64A0000481A05080500010000000000006E70E3"),
        ("ewelink_tp02", 0x05, "898AEE1BC878F64A000043C80208050008000000000000A32648"),
    ],
)
class TestEncoderEwelink(_TestEncoderBase):
    """eWeLink Encoder tests."""


@pytest.mark.parametrize(
    _TestEncoderFull.PARAM_NAMES,
    [
        # FAN GEAR 1
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A449125E2C76D48D4EBEC6A8BF3D16A2DF397",
            "cmd: 0x15, param: 0x01, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 118, seed: 0x00F3",
            "fan_0: ['on', 'speed'] / {'speed_count': 6, 'on': True, 'speed': 1.0}",
        ),
        # FAN GEAR 2
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A449141E2C76D48F0CFCB4EAFD7F54E094260",
            "cmd: 0x15, param: 0x02, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 18, seed: 0x00D7",
            "fan_0: ['on', 'speed'] / {'speed_count': 6, 'on': True, 'speed': 2.0}",
        ),
        # FAN GEAR 3
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491A5E2C76D4856696CE8097153E8AFA411",
            "cmd: 0x15, param: 0x03, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 246, seed: 0x0071",
            "fan_0: ['on', 'speed'] / {'speed_count': 6, 'on': True, 'speed': 3.0}",
        ),
        # FAN GEAR 4
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A449171E2C76D488EB1B330D1A98B30770605",
            "cmd: 0x15, param: 0x04, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 34, seed: 0x00A9",
            "fan_0: ['on', 'speed'] / {'speed_count': 6, 'on': True, 'speed': 4.0}",
        ),
        # FAN GEAR 5
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491D8E2C76D480A3536B4552D0FB4F3D036",
            "cmd: 0x15, param: 0x05, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 139, seed: 0x002D",
            "fan_0: ['on', 'speed'] / {'speed_count': 6, 'on': True, 'speed': 5.0}",
        ),
        # FAN GEAR 6
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A44919BE2C76D483D020283621A3883C4FA0E",
            "cmd: 0x15, param: 0x06, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 200, seed: 0x001A",
            "fan_0: ['on', 'speed'] / {'speed_count': 6, 'on': True, 'speed': 6.0}",
        ),
        # FAN OFF
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A44913DE2C76D48DEE5E76081F9DB602729AC",
            "cmd: 0x11, param: 0x00, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 110, seed: 0x00F9",
            "fan_0: ['on'] / {'speed_count': 6, 'on': False}",
        ),
        # FAN REVERSE
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A449198E2C76D48C4ADFC7A9BE3C17A3D84AF",
            "cmd: 0x43, param: 0x01, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 203, seed: 0x00E3",
            "fan_0: ['dir'] / {'dir': False}",
        ),
        # FAN FORWARD
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A449194E2C76D48066F3FB8592103B8FF25F8",
            "cmd: 0x43, param: 0x00, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 199, seed: 0x0021",
            "fan_0: ['dir'] / {'dir': True}",
        ),
        # FAN BREEZE
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491A9E2C76D48E28ADA5CBDC5E75C1BAA8C",
            "cmd: 0x42, param: 0x01, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 250, seed: 0x00C5",
            "fan_0: ['preset'] / {'preset': 'breeze'}",
        ),
        # FAN SLEEP
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491F1E2C76D48781040C7275F7DC681DAED",
            "cmd: 0x42, param: 0x01, args: [1,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 162, seed: 0x005F",
            "fan_0: ['preset'] / {'preset': 'sleep'}",
        ),
        # NEUTRAL, BR ~50%
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491D4E2C76D48043C3D89692301BAFD6ED6",
            "cmd: 0x12, param: 0x00, args: [51,50,0]",
            "id: 0x86C63BC8, index: 0, tx: 135, seed: 0x0023",
            "light_0: ['cold', 'warm'] / {'sub_type': 'cww', 'br': 0.51, 'ctr': 0.5}",
        ),
        # NEUTRAL, BR 100%
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491D6E2C76D484B737291266C4EF5B25221",
            "cmd: 0x12, param: 0x00, args: [100,50,0]",
            "id: 0x86C63BC8, index: 0, tx: 133, seed: 0x006C",
            "light_0: ['cold', 'warm'] / {'sub_type': 'cww', 'br': 1.0, 'ctr': 0.5}",
        ),
        # NEUTRAL, BR 1%
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491D2E2C76D48754D4CCA185270CB8C7317",
            "cmd: 0x12, param: 0x00, args: [1,50,0]",
            "id: 0x86C63BC8, index: 0, tx: 129, seed: 0x0052",
            "light_0: ['cold', 'warm'] / {'sub_type': 'cww', 'br': 0.01, 'ctr': 0.5}",
        ),
    ],
)
class TestEncoderEwelinkFull(_TestEncoderFull):
    """eWeLink Encoder / Decoder Full tests."""


@pytest.mark.parametrize(
    _TestEncoderFull.PARAM_NAMES,
    [
        # PAIR
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491A2E2C76D48A69F9C18F981A3185F760E",
            "cmd: 0x13, param: 0x03, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 241, seed: 0x0081",
            "device_0: ['cmd'] / {'cmd': 'pair'}",
        ),
        # ALL OFF
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A44916AE2C76D4885BEBC39DAA2803B7CB951",
            "cmd: 0x11, param: 0x00, args: [2,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 57, seed: 0x00A2",
            "device_0: ['on'] / {'on': False}",
        ),
        # TIMER 1H
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491EFE2C76D48BB808207E89CBE0542B5DC",
            "cmd: 0x11, param: 0x00, args: [2,12,0]",
            "id: 0x86C63BC8, index: 0, tx: 188, seed: 0x009C",
            "device_0: ['cmd'] / {'cmd': 'timer', 's': 3600.0}",
        ),
        # TIMER 2H,
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491A2E2C76D481D2624A15A3A18A3E4D5C2",
            "cmd: 0x11, param: 0x00, args: [2,24,0]",
            "id: 0x86C63BC8, index: 0, tx: 241, seed: 0x003A",
            "device_0: ['cmd'] / {'cmd': 'timer', 's': 7200.0}",
        ),
        # MAIN LIGHT TOGGLE
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A449147E2C76D48437878FC1C6446FDBA50B6",
            "cmd: 0x11, param: 0x02, args: [1,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 20, seed: 0x0064",
            "light_0: ['on'] / {'on': 'toggle'}",
        ),
        # SECOND LIGHT TOGGLE
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A449195E2C76D48A69D9D1CF981A3185F2E14",
            "cmd: 0x11, param: 0x02, args: [4,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 198, seed: 0x0081",
            "light_1: ['on'] / {'on': 'toggle'}",
        ),
        # FULL WHITE, BR 100%
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A44910EE2C76D48211919FB1A06249FD835DD",
            "cmd: 0x12, param: 0x01, args: [100,100,0]",
            "id: 0x86C63BC8, index: 0, tx: 93, seed: 0x0006",
            "light_0: ['cold', 'warm'] / {'sub_type': 'cww', 'br': 1.0, 'ctr': 1.0}",
        ),
        # FULL YELLOW, BR 100%
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491DAE2C76D484078789A1F6745FEB9FB76",
            "cmd: 0x12, param: 0x01, args: [100,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 137, seed: 0x0067",
            "light_0: ['cold', 'warm'] / {'sub_type': 'cww', 'br': 1.0, 'ctr': 0.0}",
        ),
        # NEUTRAL, BR 100%
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A449161E2C76D481E2626C473391BA0E723EF",
            "cmd: 0x12, param: 0x01, args: [100,50,0]",
            "id: 0x86C63BC8, index: 0, tx: 50, seed: 0x0039",
            "light_0: ['cold', 'warm'] / {'sub_type': 'cww', 'br': 1.0, 'ctr': 0.5}",
        ),
        # Night Mode
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A4491B0E2C76D48FEC6C54193D9FB4007C117",
            "cmd: 0x12, param: 0x02, args: [1,50,0]",
            "id: 0x86C63BC8, index: 0, tx: 227, seed: 0x00D9",
            "light_0: ['cold', 'warm'] / {'sub_type': 'cww', 'br': 0.01, 'ctr': 0.5}",
        ),
        # BR+
        (
            "ewelink_v0/r",
            "0201021B05FFFFEE1BC878F64A41909A3AFFADD35C6460E2037B59E2A51366",
            "cmd: 0x12, param: 0x05, args: [0,0,0]",
            "id: 0x1D060310, index: 0, tx: 201, seed: 0x007B",
            "light_0: ['cmd'] / {'sub_type': 'cww', 'cmd': 'B+', 'step': 0.05}",
        ),
        # BR-
        (
            "ewelink_v0/r",
            "0201021B05FFFFEE1BC878F64A4190803AFFADD3AD959213F28AA81354F19A",
            "cmd: 0x12, param: 0x06, args: [0,0,0]",
            "id: 0x1D060310, index: 0, tx: 211, seed: 0x008A",
            "light_0: ['cmd'] / {'sub_type': 'cww', 'cmd': 'B-', 'step': 0.05}",
        ),
        # FAN OSC TOGGLE
        (
            "ewelink_v0/p3",
            "0201011BFFFF00EE1BC878F64A44916AE2C76D483F55048160183A81C63C30",
            "cmd: 0x40, param: 0x02, args: [0,0,0]",
            "id: 0x86C63BC8, index: 0, tx: 57, seed: 0x0018",
            "fan_0: ['osc'] / {'osc': 'toggle'}",
        ),
    ],
)
class TestEncoderEwelinkNoDirect(_TestEncoderFull):
    """eWeLink Encoder / Decoder No Direct tests."""

    _with_reverse = False


@pytest.mark.parametrize(
    _TestEncoderFull.PARAM_NAMES,
    [
        # POWER, remote 0x1A05, no group
        (
            "ewelink_tp02",
            "0201021B05898AEE1BC878F64A0000481A05080500010000000000006E70E3",
            "cmd: 0x01, param: 0x00, args: [0,0,0]",
            "id: 0x00001A05, index: 0, tx: 72, seed: 0x006E",
            "light_0: ['on'] / {'on': 'toggle'}",
        ),
        # GROUP 1 button, also a toggle
        (
            "ewelink_tp02",
            "0201021B05898AEE1BC878F64A0000461A05080501090000000000006465CD",
            "cmd: 0x09, param: 0x00, args: [0,0,0]",
            "id: 0x00001A05, index: 1, tx: 70, seed: 0x0064",
            "light_0: ['on'] / {'on': 'toggle'}",
        ),
        # WARMER, group 1
        (
            "ewelink_tp02",
            "0201021B05898AEE1BC878F64A0000471A05080501070000000000007A7D7A",
            "cmd: 0x07, param: 0x00, args: [0,0,0]",
            "id: 0x00001A05, index: 1, tx: 71, seed: 0x007A",
            "light_0: ['cmd'] / {'sub_type': 'cww', 'cmd': 'K-', 'step': 0.1}",
        ),
        # BRIGHTER, group 2
        (
            "ewelink_tp02",
            "0201021B05898AEE1BC878F64A0000331A0508050204000000000000D044EF",
            "cmd: 0x04, param: 0x00, args: [0,0,0]",
            "id: 0x00001A05, index: 2, tx: 51, seed: 0x00D0",
            "light_0: ['cmd'] / {'sub_type': 'cww', 'cmd': 'B+', 'step': 0.1}",
        ),
        # DIMMER, remote 0xC802, group 1
        (
            "ewelink_tp02",
            "0201021B05898AEE1BC878F64A00002FC802080501050000000000008B46E8",
            "cmd: 0x05, param: 0x00, args: [0,0,0]",
            "id: 0x0000C802, index: 1, tx: 47, seed: 0x008B",
            "light_0: ['cmd'] / {'sub_type': 'cww', 'cmd': 'B-', 'step': 0.1}",
        ),
    ],
)
class TestEncoderEwelinkRemoteNoDirect(_TestEncoderFull):
    """eWeLink 2.4G CCT panel remote: remote presses, decoded only."""

    _with_reverse = False


@pytest.mark.parametrize("on", [True, False])
def test_ewelink_remote_on_off(on: bool) -> None:
    """ON and OFF are both sent as the power toggle, from the remote's address on channel 37."""
    codec = CODECS["ewelink_tp02"]
    assert codec.own_address == "66:55:44:33:22:11"
    assert codec.channel_map == 0x01
    enc_cmds = codec.ent_to_enc(BleAdvEntAttr([ATTR_ON], {ATTR_ON: on}, LIGHT_TYPE, 0), BleAdvCodec.DEF_TRANS_NAME)
    assert enc_cmds == [BleAdvEncCmd(0x01)]
    conf = BleAdvConfig(0x1A05, 0)
    conf.tx_count = 0x48
    conf.seed = 0x6E
    assert codec.encode_advs(enc_cmds[0], conf)[0].to_raw() == bytes.fromhex("0201021B05898AEE1BC878F64A0000481A05080500010000000000006E70E3")


def test_ewelink_remote_bad_id_suffix() -> None:
    """An advert with valid CRC but unknown bytes after the remote ID is not decoded."""
    codec = CODECS["ewelink_tp02"]
    conf = BleAdvConfig(0x1A05, 0)
    conf.seed = 0x6E
    raw = bytearray(codec.encode_advs(BleAdvEncCmd(0x01), conf)[0].raw)
    raw[13] = 0x09  # 0x08 0x05 after the remote ID becomes 0x09 0x05
    raw[-2:] = codec._crc(raw[8:-2]).to_bytes(2, "little")  # noqa: SLF001
    assert codec.decode_adv(BleAdvAdvertisement(0x05, bytes(raw), 0x02)) == (None, None)
