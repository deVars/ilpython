from patchUtil import patchList, getARMBLHexString, getFuncEA
patches = [
    (
        'Auto press bubbles',
        '<SpawnBonus>c__Iterator8::MoveNext',
        '',
        int('33f', 16),
        '00 ' +  # NOP ld.arg 0
        '00 00 00 00 00 ' +  # NOP CInterfaceManager.this
        '00 00 00 00 00 ' +  # NOP CInterfaceManager.localPlayerDisease
        '00 00 00 00 00 ' +  # NOP Disease:get_bubbleAutopress()
        '00 00 00 00 00 ' +  # NOP brfalse
        ''
    ),
    (
        'Super stealth mode',
        'GovernmentActionManager::ActionPossible',
        '',
        int('189', 16),
        '2a ' +  # return early because triggering priority is not allowed
        ''
    ),
    (
        'Super mutation instability',
        'SPDisease::get_mutation',
        '',
        int('0', 16),
        '22 00 00 4d 41 ' +  # ldc.r4 12.8125
        '00 ' +  # NOP
        '00 00 00 00 00 ' +  # NOP
        ''
    ),
    (
        'Can mutate any tech [0 of 1]',
        'Disease::EvolveRandomTech_0',
        '',
        int('2', 16),
        '17 ' +  # ldc.i4 1
        '00 00 00 00 00 ' +  # NOP
        ''
    ),
    (
        'Can mutate any tech [1 of 1]',
        'Disease::EvolveRandomTech_0',
        '',
        int('cb', 16),
        '17 ' +  # ldc.i4 1
        '00 00 00 00 00 ' +  # NOP
        ''
    ),
]

patchList(patches)