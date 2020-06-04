patches = [
    (
        'No Item decrease',
        'Sekai.SaveDataManager::SubItem',
        '',
        int('1e', 16),
        '16 ' +  # ldc.i4.0  (always subtract 0 to current item)
        ''
    ),
    (
        'Max Setsuna Stocks',
        'Sekai.BattleCharacterPointParameter::get_setsunaPoint',
        '',
        int('0', 16),
        '22 00 00 96 43 ' +  # ldc.r4 #300.0
        '2a ' +  # ret
        '',
    ),
    (
        'Constant MP',
        'Sekai.BattleCharacterStatus::get_nowMagicPoint',
        '',
        int('D', 16),
        '20 0f 27 00 00 ' +  # ldc.i4 #1000
        '00 00 00 00 00 00 ' +  # NOP padding
        ''
    ),
    (
        'NewType Mode [0 of 1]',
        'Sekai.PlayerParameter::get_avoid',
        '',
        int('0', 16),
        '1f 55 ' +  # ldc.i4.s #85
        '2a ' +  # ret
        '00 00 00 ' +  # NOP padding
        ''
    ),
    (
        'NewType Mode [1 of 1]',
        'Sekai.PlayerParameter::get_critical',
        '',
        int('0', 16),
        '1f 64 ' +  # ldc.i4.s #100
        '2a ' +  # ret
        '00 00 00 ' +  # NOP padding
        ''
    ),
]

patchList(patches)