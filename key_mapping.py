# key_mapping.py

keycode_to_vk = {
    # Basic alphanumeric keys (A-Z)
    65: 0x41,  # A
    66: 0x42,  # B
    67: 0x43,  # C
    68: 0x44,  # D
    69: 0x45,  # E
    70: 0x46,  # F
    71: 0x47,  # G
    72: 0x48,  # H
    73: 0x49,  # I
    74: 0x4A,  # J
    75: 0x4B,  # K
    76: 0x4C,  # L
    77: 0x4D,  # M
    78: 0x4E,  # N
    79: 0x4F,  # O
    80: 0x50,  # P
    81: 0x51,  # Q
    82: 0x52,  # R
    83: 0x53,  # S
    84: 0x54,  # T
    85: 0x55,  # U
    86: 0x56,  # V
    87: 0x57,  # W
    88: 0x58,  # X
    89: 0x59,  # Y
    90: 0x5A,  # Z

    # Number keys (0-9)
    48: 0x30,  # 0
    49: 0x31,  # 1
    50: 0x32,  # 2
    51: 0x33,  # 3
    52: 0x34,  # 4
    53: 0x35,  # 5
    54: 0x36,  # 6
    55: 0x37,  # 7
    56: 0x38,  # 8
    57: 0x39,  # 9

    # Special characters
    186: 0xBA,  # ; :
    187: 0xBB,  # = +
    188: 0xBC,  # , <
    189: 0xBD,  # - _
    190: 0xBE,  # . >
    191: 0xBF,  # / ?
    192: 0xC0,  # ` ~
    219: 0xDB,  # [ {
    220: 0xDC,  # \ |
    221: 0xDD,  # ] }
    222: 0xDE,  # ' "

    # Function keys (F1-F12)
    112: 0x70,  # F1
    113: 0x71,  # F2
    114: 0x72,  # F3
    115: 0x73,  # F4
    116: 0x74,  # F5
    117: 0x75,  # F6
    118: 0x76,  # F7
    119: 0x77,  # F8
    120: 0x78,  # F9
    121: 0x79,  # F10
    122: 0x7A,  # F11
    123: 0x7B,  # F12

    # Control keys
    8: 0x08,    # Backspace
    9: 0x09,    # Tab
    13: 0x0D,   # Enter
    16: 0x10,   # Shift
    17: 0x11,   # Ctrl
    18: 0x12,   # Alt
    20: 0x14,   # Caps Lock
    32: 0x20,   # Space

    # Navigation keys
    33: 0x21,   # Page Up
    34: 0x22,   # Page Down
    35: 0x23,   # End
    36: 0x24,   # Home
    37: 0x25,   # Left Arrow
    38: 0x26,   # Up Arrow
    39: 0x27,   # Right Arrow
    40: 0x28,   # Down Arrow
    45: 0x2D,   # Insert
    46: 0x2E,   # Delete

    # Numeric keypad
    96: 0x60,   # NumPad 0
    97: 0x61,   # NumPad 1
    98: 0x62,   # NumPad 2
    99: 0x63,   # NumPad 3
    100: 0x64,  # NumPad 4
    101: 0x65,  # NumPad 5
    102: 0x66,  # NumPad 6
    103: 0x67,  # NumPad 7
    104: 0x68,  # NumPad 8
    105: 0x69,  # NumPad 9
    106: 0x6A,  # NumPad *
    107: 0x6B,  # NumPad +
    109: 0x6D,  # NumPad -
    110: 0x6E,  # NumPad .
    111: 0x6F,  # NumPad /

    # Lock keys
    144: 0x90,  # Num Lock
    145: 0x91,  # Scroll Lock
    19: 0x13,   # Pause/Break

    # Other symbols
    189: 0xBD,  # Minus _
    187: 0xBB,  # Equals +
    191: 0xBF,  # Forward Slash /
    192: 0xC0,  # Grave Accent `
    222: 0xDE,  # Apostrophe '
    221: 0xDD,  # Bracket Right ]
    220: 0xDC,  # Backslash \
    219: 0xDB,  # Bracket Left [
    186: 0xBA,  # Semicolon ;
    188: 0xBC,  # Comma ,
    190: 0xBE,  # Period .
    111: 0x6F,  # Divide /
    107: 0x6B,  # Add +
    109: 0x6D,  # Subtract -
    106: 0x6A,  # Multiply *

    # Modifier keys
    16: 0x10,   # Shift
    17: 0x11,   # Control
    18: 0x12,   # Alt

    # Miscellaneous
    93: 0x5D,   # Context Menu (Right Click Menu Key)
    223: 0xC1,  # Right Alt key
}
