from patchUtil import patchList, getARMBLHexString, getFuncEA
patches = [
    (
        'skip video ads',
        'AdManager$$IsVideoSkip',
        '',
        0,
        '01 00 a0 e3 ' +  # MOV r0, 0x01
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'skip banners',
        'AdManager$$IsBannerSkip',
        '',
        0,
        '01 00 a0 e3 ' +  # MOV r0, 0x01
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'skip instance',
        'AdManager$$IsInstSkip',
        '',
        0,
        '01 00 a0 e3 ' +  # MOV r0, 0x01
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'tap generates 80 balls',
        'PopManager$$Update',
        '',
        int('330', 16),
        '50 00 a0 e3 ' +  # MOV r0, 0x50
        ''
    ),
    (
        'do not use mats when lv up fails: servants',
        '_OnServantSelectButtonClick_c__AnonStorey2$$__m__0',
        '',
        int('2b8', 16),
        '01 00 a0 e3 ' +  # MOV r0, 0x01
        ''
    ),
    (
        'do not use mats when lv up fails: artifacts',
        '_OnSelectButtonClick_c__AnonStorey0$$__m__0',
        '',
        int('270', 16),
        '01 00 a0 e3 ' +  # MOV r0, 0x01
        ''
    ),
    (
        'Ad box does not expire',
        'AdBoxObj$$Update',
        '',
        int('24', 16),
        '10 0a 08 ee ' +  # VMOV s16, r0  (ignore timer val)
        ''
    ),
    # (
    #     'skill is always available',
    #     'SkillButton$$OnButtonClick',
    #     '',
    #     int('34', 16),
    #     '01 00 a0 e3 ' +  # MOV r0, 0x01  (from LDRB r0, [r4, 0x34])
    #     ''
    # ),
    # (
    #     'skill does not end',
    #     'SkillButton$$UpdateDuringSkillState',
    #     '',
    #     int('c8', 16),
    #     '00 f0 20 e3 ' +  # NOP  (SkillButton$$EndSkill to NOP)
    #     ''
    # ),
]


patchList(patches)
