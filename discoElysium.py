from patchUtil import patchList

patches = [
    (
        'Better Items 0 of 1',
        'Sunshine.ContainerSource::RollItems',
        '',
        int('af', 16),
        '2b 04 ' +  # br.s 0x04
        ''
    ),
    (
        'Better Items 1 of 1',
        'Sunshine.ContainerSource::RollItemsOnce',
        '',
        int('b2', 16),
        '2b 04 ' +  # br.s 0x04
        ''
    ),
    (
        'Always Run',
        'FortressOccident.CharacterNavigator::get_isRunning',
        '',
        int('31', 16),
        '17 ' +  # ldc.i4.1
        '2a ' +  # ret
        ''
    ),
    (
        'Run Speed',
        'FortressOccident.CharacterNavigator::OnUpdate',
        '',
        int('42', 16),
        '00 22 00 00 60 40 ' +  # ldc.r4 3.5
        ''
    ),
    # (
    #     'Autorun Distance',
    #     'FortressOccident.CharacterNavigator::.ctor',
    #     '',
    #     int('17', 16),
    #     '22 00 00 00 00 ' +  # ldc.r4 0.0
    #     ''
    # ),
    (
        'Success on all passive checks',
        'PassiveNode::CheckSuccess',
        '',
        int('6a', 16),
        '17 2a 00 ' +  # return true + nop padding
        ''
    ),
    (
        'Success on all other checks',
        'Sunshine.Metric.SunshineRoller::WhiteCheck',
        '',
        int('3d', 16),
        '2b 06 00 00 00 00 ' +  # return true + nop padding
        ''
    ),
]


patchList(patches)