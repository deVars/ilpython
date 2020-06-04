# server security prevents hacks

CAN_CAST_SKILL_FN = '_ZNK12ACharacterPC12CanCastSkillEPK9SkillInfoj'
IS_ENEMY_EA = getFuncEA('_ZN12ACharacterPC7IsEnemyEv')

patches = [
    # (
    #     'No APK integrity check round 2',
    #     '_ZN35Android_NetmarbleSSecurityPortLayer18DetectApkIntgErrorEbb',
    #     '',
    #     int('0', 16),
    #     '00 00 a0 e3 ' +  # MOV R0, #0
    #     '1e ff 2f e1 ' +  # BX LR
    #     '',
    # ),
    (
        'No APK integrity check round 3',
        '_ZN9LnPublish18NetmarbleSSecurity18DetectApkIntgErrorEbb',
        '',
        int('0', 16),
        '00 00 a0 e3 ' +  # MOV R0, #0
        '1e ff 2f e1 ' +  # BX LR
        '',
    ),
    (
        'No APK integrity check round 4',
        '_ZN18NetmarbleSSecurity18DetectApkIntgErrorEbb',
        '',
        int('0', 16),
        '00 00 a0 e3 ' +  # MOV R0, #0
        '1e ff 2f e1 ' +  # BX LR
        '',
    ),
    (
        'No APK integrity check [0 of 3]',
        '_ZN22JNI_NetmarbleSSecurity18DetectApkIntgErrorEbb',
        '',
        int('20', 16),
        '00 f0 20 e3 ' +  # change CMP -> NOP
        '',
    ),
    (
        'No APK integrity check [1 of 3]',
        '_ZN22JNI_NetmarbleSSecurity18DetectApkIntgErrorEbb',
        '',
        int('27', 16),
        'ea ' +  # change BNE to B
        '',
    ),
    (
        'No APK integrity check [2 of 3]',
        '_ZN22JNI_NetmarbleSSecurity18DetectApkIntgErrorEbb',
        '',
        int('d4', 16),
        '00 f0 20 e3 ' +  # change CMP -> NOP
        '',
    ),
    (
        'No APK integrity check [3 of 3]',
        '_ZN22JNI_NetmarbleSSecurity18DetectApkIntgErrorEbb',
        '',
        int('db', 16),
        'ea ' +  # change BNE to B
        '',
    ),
    (
        'Can always cast skill',
        CAN_CAST_SKILL_FN,
        '',
        int('0', 16),
        '00 48 2d e9 ' +  # STMFD SP!, {R11, LR}
        '00 30 a0 e1 ' +  # MOV R0, R2
        '01 10 a0 e3 ' +  # MOV R1, #1
        getARMBLHexString(IS_ENEMY_EA,
                          getFuncEA(CAN_CAST_SKILL_FN) +
                          int('0', 16) + 12) + ' ' +
        '01 20 20 e0 ' +  # EOR R2, R0, R1 (XOR r0, r0, r1)
        'c9 1a 01 e3 ' +  # MOV R1, #0x1ac9
        '01 20 c3 e7 ' +  # STRB R2, [R3, R1] (set curskill as soulshot)
        '02 00 a0 e1 ' +  # MOV R0, R2
        '00 48 bd e8 ' +  # LDMFD SP!, {R11, LR}
        '1e ff 2f e1 ' +  # BX LR
        '',
    ),
    # (
    #     'No combo clears',
    #     '_ZN12SkillManager10ClearComboEv',
    #     '',
    #     0,
    #     '1e ff 2f e1 ' +  # BX LR
    #     '',
    # ),
    # (
    #     'Combo does not expire',
    #     '_ZNK12SkillManager14IsComboExpiredEv',
    #     '',
    #     0,
    #     '00 00 a0 e3 ' +  # MOV R0, #0
    #     '1e ff 2f e1 ' +  # BX LR
    #     '',
    # ),
    # (
    #     'Increasing combo does not trigger combo time expire [1 of 2]',
    #     '_ZN12SkillManager18IncreaseComboCountEi',
    #     '',
    #     int('3c', 16),
    #     '00 00 50 e1',  # CMP R0, R0
    # ),
    # (
    #     'Increasing combo does not trigger combo time expire [2 of 2]',
    #     '_ZN12SkillManager18IncreaseComboCountEi',
    #     '',
    #     int('48', 16),
    #     '58 01 84 35',  # STRCC R0, [R4, #158]
    # )
]

patchList(patches)