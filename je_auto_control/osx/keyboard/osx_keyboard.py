import sys

if sys.platform not in ["darwin"]:
    raise Exception("should be only loaded on MacOS")

import time

import AppKit
import Quartz

from je_auto_control.osx.core.utils.osx_vk import osx_key_shift

special_key_table = {
    "key_sound_up": 0,
    "key_sound_down": 1,
    "key_brightness_up": 2,
    "key_brightness_down": 3,
    "key_capslock": 4,
    "key_help": 5,
    "key_power": 6,
    "key_mute": 7,
    "key_arrow_up": 8,
    "key_arrow_down": 9,
    "key_numlock": 10,
    "key_contrast_up": 11,
    "key_contrast_down": 12,
    "key_launch_panel": 13,
    "key_eject": 14,
    "key_vidmirror": 15,
    "key_play": 16,
    "key_next": 17,
    "key_previous": 18,
    "key_fast": 19,
    "key_rewind": 20,
    "key_illumination_up": 21,
    "key_illumination_down": 22,
    "key_illumination_toggle": 23,
}


def normal_key(keycode, is_shift, is_down):
    """
    :param keycode what keycode we want to press or release
    :param is_shift use shift key ?
    :param is_down is_down true = press; false = release
    create event
    post event
    """
    if is_shift:
        event = Quartz.CGEventCreateKeyboardEvent(
            None,
            osx_key_shift,
            is_down
        )
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
    event = Quartz.CGEventCreateKeyboardEvent(
        None,
        keycode,
        is_down
    )
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)


def special_key(keycode, is_shift):
    """
    :param keycode what keycode we want to press or release
    :param is_shift use shift key ?
    create event
    post event
    """
    keycode = special_key_table[keycode]
    event = AppKit.NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2(
        Quartz.NSSystemDefined,
        (0, 0),
        0xa00 if is_shift else 0xb00,
        0,
        0,
        0,
        8,
        (keycode << 16) | ((0xa if is_shift else 0xb) << 8),
        -1
    )
    Quartz.CGEventPost(0, event)


def press_key(keycode, is_shift):
    if keycode in special_key_table:
        special_key(keycode, is_shift)
    else:
        normal_key(keycode, is_shift, True)


def release_key(keycode, is_shift):
    if keycode in special_key_table:
        special_key(keycode, is_shift)
    else:
        normal_key(keycode, is_shift, False)
