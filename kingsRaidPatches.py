import patchUtil

patches = [
    (
        'Remove battle integrity checks',
        'NGame2.NBattleContext.CampaignContext::CheckBattleIntegrity',
        '',
        0,
        '2a'
    ),
    (
        'Integrity checker always a success',
        'NShared.BattleInstanceIntegrityChecker::Run',
        '',
        0,
        '14 2a 00 00 00'
    ),
    # (
    #     # Refer to NShared.BattleCreature##GetUserSkillLevel for addresses
    #     'PCs get 95 percent chance to hit while enemies get 5 percent chance',
    #     'NShared.StatController::TestHitChanceRateResult',
    #     '',
    #     0,
    #     '02 28 bf 8a 00 06 28 d6 83 00 06 6f 4d 84 00 06 ' + \
    #     '2c 04 1f 5f 2b 01 1b 0d 09 1f 64 5a 0d 2b 14 00 '
    #     # '2c 04 1f 5f 2b 01 1b 0d 09 1f 64 5a 0d 2b 1a 00 ' + \
    #     # '00 00 00 00 00 '
    # ),
    (
        'PCs no need MP',
        'NShared.SkillData::GetMp',
        '39 24 00 00 00 03',
        6,
        '28 d6 83 00 06 6f 4d 84 00 06 2c 17 1c 2a 00 00 00 00'
    ),
    (
        'PCs no need cooltime',
        'NShared.SkillController::StartCooltime',
        '2a 02 28 7e 89 00 06',
        7,
        '28 d6 83 00 06 6f 4d 84 00 06 2d 01 2a 03 6f a3 ' + \
        'a6 00 06 0b 2b 04 00 00 00 00 03'
    ),
]

patchList(patches)