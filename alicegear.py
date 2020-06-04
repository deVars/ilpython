IS_SKILL_OWNER_ENEMY_EA = getFuncEA('UnitSkillCtrl$$get_IsOwnerEnemy')
IS_PLAYER_UNIT_EA = getFuncEA('UnitBase$$isPlayerUnit')
SKILL_IS_READY_FN = 'UnitSkillCtrl$$isSkillReady'
patches = [
    (
        # this also makes cooltime useless
        'Skill has no activation limit [0 of 2]',
        'UISkillButton$$onPushButton',
        '',
        int('50', 16),
        '01 00 a0 e3 ' +  # mov r0, #1 (fake UISkillButton.isEnable as 1)
        '',
    ),
    (
        'Skill has no activation limit [1 of 2]',
        'UISkillButton$$onPushButton',
        '',
        int('58', 16),
        '01 00 a0 e3 ' +  # mov r0, #1 (fake UISkillButton.isEnableInner as 1)
        '',
    ),
    (
        'Skill has no activation limit [2 of 2]',
        'ActiveSkill$$checkEnableActivate',
        '',
        int('0', 16),
        '01 00 a0 e3 ' +  # mov r0, #1
        '1e ff 2f e1 ' +  # bx lr
        '',
    ),
    (
        'Always charged shots [0 of 3]',
        'UnitChargeCtrl$$updateCharge',
        '',
        int('344', 16),
        '00 f0 20 e3 ' +  # nop
        '00 f0 20 e3 ' +  # nop
        '',
    ),
    (
        'Always charged shots [1 of 3]',
        'UnitChargeCtrl$$updateCharge',
        '',
        int('1bc', 16),
        '00 f0 20 e3 ' +  # nop
        '00 f0 20 e3 ' +  # nop
        '',
    ),
    (
        'Always charged shots [2 of 3]',
        'UnitChargeCtrl$$updateCharge',
        '',
        int('2d8', 16),
        '00 f0 20 e3 ' +  # nop
        '00 f0 20 e3 ' +  # nop
        '',
    ),
    (
        'Always charged shots [3 of 3]',
        'UnitChargeCtrl$$updateCharge',
        '',
        int('32c', 16),
        '20 00 44 e3 ' +  # MOVT r0, #0x4020 (4020:xxxx for r4.0)
        '00 f0 20 e3 ' +  # nop
        '',
    ),
    (
        'No stamina decrease',
        'UnitMainCtrl$$useStaminaRatio',
        '',
        int('dc', 16),
        '00 10 a0 e3 ' +  # mov r1, #0
        '',
    ),
    (
        'No need for area time limits',
        'LimitTime$$get_ElapsedTime',
        '',
        int('0', 16),
        '30 00 a0 e3 ' +  # mov r0, #48 (spend 48 seconds fighting)
        '1e ff 2f e1 ' +  # bx lr
        ''
    ),
]

patchList(patches)