from patchUtil import patchList, getARMBLHexString, getFuncEA

patches = [
    (
        'boost player [0 of 1]',
        'Player$$IsQuadrupleBoost',
        '',
        0,
        '01 00 a0 e3 ' +  # MOV r0, 0x01
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'boost player [1 of 1]',
        'Player$$IsAnyBoosted',
        '',
        0,
        '00 10 a0 e1 ' +  # MOV r1, r0
        '01 00 a0 e3 ' +  # MOV r0, 0x01
        '0a 20 a0 e3 ' +  # MOV r2, 0x0a
        '1c 00 c1 e5 ' +  # STRB r0, [r1, 0x1c]
        '20 20 c1 e5 ' +  # STRB r2, [r1, 0x20]
        '24 00 c1 e5 ' +  # STRB r0, [r1, 0x24]
        '28 20 c1 e5 ' +  # STRB r2, [r1, 0x28]
        '2c 00 c1 e5 ' +  # STRB r0, [r1, 0x2c]
        '30 20 c1 e5 ' +  # STRB r2, [r1, 0x30]
        '34 00 c1 e5 ' +  # STRB r0, [r1, 0x34]
        '38 20 c1 e5 ' +  # STRB r2, [r1, 0x38]
        '3c 00 c1 e5 ' +  # STRB r0, [r1, 0x3c]
        '40 20 c1 e5 ' +  # STRB r2, [r1, 0x40]
        '44 00 c1 e5 ' +  # STRB r0, [r1, 0x44]
        '48 20 c1 e5 ' +  # STRB r2, [r1, 0x48]
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'maybe sp awesomeness',
        'FieldObject$$EnableConfuse',
        '',
        int('28', 16),
        'e8 13 00 e3 ' +  # MOV r1, 0x03e8  spVal to 1000
        '3c 11 80 e5 ' +  # STR r1, [r0, 0x13c]
        '00 00 a0 e3 ' +  # MOV r0, 0x00  disable confuse
        ''
    ),
]

patchList(patches)