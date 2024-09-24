"""Module for representing a JVC Projector command."""

from __future__ import annotations

from collections.abc import Callable
import logging
import re
from typing import Final

from . import const

_LOGGER = logging.getLogger(__name__)

PJOK: Final = b"PJ_OK"
PJNG: Final = b"PJ_NG"
PJREQ: Final = b"PJREQ"
PJACK: Final = b"PJACK"
PJNAK: Final = b"PJNAK"

UNIT_ID: Final = b"\x89\x01"
HEAD_OP: Final = b"!" + UNIT_ID
HEAD_REF: Final = b"?" + UNIT_ID
HEAD_RES: Final = b"@" + UNIT_ID
HEAD_ACK: Final = b"\x06" + UNIT_ID
HEAD_LEN: Final = 1 + len(UNIT_ID)
END: Final = b"\n"

TEST: Final = "\0\0"
VERSION: Final = "IFSV"
MODEL: Final = "MD"
MAC: Final = "LSMA"
SOURCE: Final = "SC"
POWER: Final = "PW"
INPUT: Final = "IP"
REMOTE: Final = "RC"

AUTH_SALT: Final = "JVCKWPJ"


class JvcCommand:
    """Class for representing a JVC Projector command."""

    def __init__(self, code: str, is_ref=False):
        """Initialize class."""
        self.code = code
        self.is_ref = is_ref
        self.ack = False
        self._response: str | None = None

    @property
    def response(self) -> str | None:
        """Return command response."""
        if not self.is_ref or self._response is None:
            return None

        res = self.code + self._response
        val: str = res[len(self.code) :]

        for pat, fmt in self.formatters.items():
            m = re.search(r"^" + pat + r"$", res)
            if m:
                if isinstance(fmt, list):
                    try:
                        return fmt[int(m[1], 16)]
                    except ValueError:
                        msg = "response '%s' not int for cmd '%s'"
                        _LOGGER.warning(msg, val, self.code)
                    except KeyError:
                        msg = "response '%s' not mapped for cmd '%s'"
                        _LOGGER.warning(msg, val, self.code)
                elif isinstance(fmt, dict):
                    try:
                        return fmt[m[1]]
                    except KeyError:
                        msg = "response '%s' not mapped for cmd '%s'"
                        _LOGGER.warning(msg, val, self.code)
                elif callable(fmt):
                    try:
                        return fmt(m)
                    except Exception as e:  # noqa: BLE001
                        msg = "response format failed with %s for '%s (%s)'"
                        _LOGGER.warning(msg, e, self.code, val)
                break

        return val

    @response.setter
    def response(self, data: str) -> None:
        """Set command response."""
        self._response = data

    @property
    def is_power(self) -> bool:
        """Return if command is a power command."""
        return self.code.startswith("PW")

    formatters: dict[str, list | dict | Callable] = {
        # Power
        "PW(.)": [const.STANDBY, const.ON, const.COOLING, const.WARMING, const.ERROR],
        # Input
        "(?:IP|IFIN)(.)": {
            "0": "svideo",
            "1": "video",
            "2": "component",
            "3": "pc",
            "6": const.HDMI1,
            "7": const.HDMI2,
        },
        # Source
        "SC(.)": [const.NOSIGNAL, const.SIGNAL],
        # Model
        "MD(.+)": lambda r: re.sub(r"-+", "-", r[1].replace(" ", "-")),
        # Picture Mode
        "PMPM(..)": {
            "00": "film",
            "01": "cinema",
            "02": "animation",
            "03": "natural",
            "04": "hdr10",
            "06": "thx",
            "0B": "frameadapt_hdr",
            "0C": "user1",
            "0D": "user2",
            "0E": "user3",
            "0F": "user4",
            "10": "user5",
            "11": "user6",
            "14": "hlg",
            "15": "hdr10+",
            "16": "pana_pq",
            "17": "filmmaker",
            "18": "frameadapt_hdr2",
            "19": "frameadapt_hdr3",
        },
        # Picture Mode - Intelligent Lens Aperture
        "PMDI(.)": ["off", "auto1", "auto2"],
        # Picture Mode - Color Profile
        "PMPR(..)": {
            "00": "off",
            "01": "film1",
            "02": "film2",
            "03": "bt709",
            "04": "cinema",
            "05": "cinema2",
            "06": "anime",
            "07": "anime2",
            "08": "video",
            "09": "vivid",
            "0A": "hdr",
            "0B": "bt2020(wide)",
            "0C": "3d",
            "0D": "thx",
            "0E": "custom1",
            "0F": "custom2",
            "10": "custom3",
            "11": "custom4",
            "12": "custom5",
            "21": "dci",
            "22": "custom6",
            "24": "bt2020(normal)",
            "25": "off(wide)",
            "26": "auto",
        },
        # Picture Mode - Color Temp
        "PMCL(..)": {
            "00": "5500k",
            "02": "6500k",
            "04": "7500k",
            "08": "9300k",
            "09": "high",
            "0A": "custom1",
            "0B": "custom2",
            "0C": "hdr10",
            "0D": "xenon1",
            "0E": "xenon2",
            "14": "hlg",
        },
        # Picture Mode - Color Correction
        "PMCC(..)": {
            "00": "5500k",
            "02": "6500k",
            "04": "7500k",
            "08": "9300k",
            "09": "high",
            "0D": "xenon1",
            "0E": "xenon2",
        },
        # Picture Mode - Gamma Table
        "PMGT(..)": {
            "00": "2.2",
            "01": "cinema1",
            "02": "cinema2",
            "04": "custom1",
            "05": "custom2",
            "06": "custom3",
            "07": "hdr_hlg",
            "08": "2.4",
            "09": "2.6",
            "0A": "film1",
            "0B": "film2",
            "0C": "hdr_pq",
            "0D": "pana_pq",
            "10": "thx",
            "15": "hdr_auto",
        },
        # Picture Mode - Color Management, Low Latency, 8K E-Shift
        "PM(?:CB|LL|US)(.)": ["off", "on"],
        # Picture Mode - Clear Motion Drive
        "PMCM(.)": ["off", None, None, "low", "high", "inverse_telecine"],
        # Picture Mode - Motion Enhance
        "PMME(.)": ["off", "low", "high"],
        # Picture Mode - Lamp Power
        "PMLP(.)": ["normal", "high"],
        # Picture Mode - Graphics Mode
        "PMGM(.)": ["standard", "high-res"],
        # Input Signal - HDMI Input Level
        "ISIL(.)": ["standard", "enhanced", "super_white", "auto"],
        # Input Signal - HDMI Color Space
        "ISHS(.)": ["auto", "ycbcr(4:4:4)", "ycbcr(4:2:2)", "rgb"],
        # Input Signal - HDMI 2D/3D
        "IS3D(.)": ["2d", "auto", None, "side_by_side", "top_bottom"],
        # Input Signal - Aspect
        "ISAS(.)": [None, None, "zoom", "auto", "native"],
        # Input Signal - Mask
        "ISMA(.)": [None, "on", "off"],
        # Installation - Lens Control
        "IN(?:FN|FF|ZT|ZW|SL|SR|SU|SD)(.)": ["stop", "start"],
        # Installation - Lens Image Pattern, Lens Lock, Screen Adjust
        "IN(?:IP|LL|SC|HA)(.)": ["off", "on"],
        # Installation - Style
        "INIS(.)": ["front", "front_ceiling", "rear", "rear_ceiling"],
        # Installation - Anamorphic
        "INVS(.)": ["off", "a", "b", "c", "d"],
        # Display - Back Color
        "DSBC(.)": ["blue", "black"],
        # Display - Menu Positions
        "DSMP(.)": [
            "left-top",
            "right-top",
            "center",
            "left-bottom",
            "right-bottom",
            "left",
            "right",
        ],
        # Installation - Source Display, Logo Data
        "DS(?:SD|LO)(.)": ["off", "on"],
        # Function - Trigger
        "FUTR(.)": [
            "off",
            "power",
            "anamo",
            "ins1",
            "ins2",
            "ins3",
            "ins4",
            "ins5",
            "ins6",
            "ins7",
            "ins8",
            "ins9",
            "ins10",
        ],
        # Function - Off Timer
        "FUOT(.)": ["off", "1hour", "2hour", "3hour", "4hour"],
        # Function - Eco Mode, Control4
        "FU(?:EM|CF)(.)": ["off", "on"],
        # Function - Input
        "IFIN(.)": ["hdmi1", "hdmi2"],
        # Function - Source
        "IFIS(..)": {
            "02": "480p",
            "03": "576p",
            "04": "720p50",
            "05": "720p60",
            "06": "1080i50",
            "07": "1080i60",
            "08": "1080p24",
            "09": "1080p50",
            "0A": "1080p60",
            "0B": "nosignal",
            "0C": "720p3d",
            "0D": "1080i3d",
            "0E": "1080p3d",
            "0F": "outofrange",
            "10": "4k(4096)60",
            "11": "4k(4096)50",
            "12": "4k(4096)30",
            "13": "4k(4096)25",
            "14": "4k(4096)24",
            "15": "4k(3840)60",
            "16": "4k(3840)50",
            "17": "4k(3840)30",
            "18": "4k(3840)25",
            "19": "4k(3840)24",
            "1C": "1080p25",
            "1D": "1080p30",
            "1E": "2048x1080p24",
            "1F": "2048x1080p25",
            "20": "2048x1080p30",
            "21": "2048x1080p50",
            "22": "2048x1080p60",
            "23": "3840x2160p120",
            "24": "4096x2160p120",
            "25": "vga(640x480)",
            "26": "svga(800x600)",
            "27": "xga(1024x768)",
            "28": "sxga(1280x1024)",
            "29": "wxga(1280x768)",
            "2A": "wxga+(1440x900)",
            "2B": "wsxga+(1680x1050)",
            "2C": "wuxga(1920x1200)",
            "2D": "wxga(1280x800)",
            "2E": "fwxga(1366x768)",
            "2F": "wxga++(1600x900)",
            "30": "uxga(1600x1200)",
            "31": "qxga",
            "32": "wqxga",
        },
        # Function - Deep Color
        "IFDC(.)": ["8bit", "10bit", "12bit"],
        # Function - Color Space
        "IFXV(.)": ["rgb", "yuv"],
        # Function - Colorimetry
        "IFCM(.)": [
            "nodata",
            "bt601",
            "bt709",
            "xvycc601",
            "xvycc709",
            "sycc601",
            "adobe_ycc601",
            "adobe_rgb",
            "bt2020(constant_luminance)",
            "bt2020(non-constant_luminance)",
            "srgb",
        ],
        # Function - HDR
        "IFHR(.)": {
            "0": "sdr",
            "1": "hdr",
            "2": "smpte_st_2084",
            "3": "hybrid_log",
            "F": "none",
        },
        # Picture Mode - HDR Level
        "PMHL(.)": ["auto", "-2", "-1", "0", "1", "2"],
        # Picture Mode - HDR Processing
        "PMHP(.)": ["static", "frame", "scene"],
        # Picture Mode - HDR Processing
        "PMCT(.)": ["auto", "sdr", None, "hdr10", "hlg"],
        # Picture Mode - Theater Optimizer
        "PMNM(.)": ["off", "on"],
        # Picture Mode - Theater Optimizer Level
        "PMNL(.)": ["reserved", "low", "medium", "high"],
        # Picture Mode - Theater Optimizer Processing
        "PMNP(.)": ["-", "start"],
        # Lan Setup
        "LSDS(.)": [const.OFF, const.ON],
        "LSMA(.+)": lambda r: re.sub(r"-+", "-", r[1].replace(" ", "-")),
        "LSIP(..)(..)(..)(..)": lambda r: f"{int(r[1], 16)}.{int(r[2], 16)}.{int(r[3], 16)}.{int(r[4], 16)}",
    }
