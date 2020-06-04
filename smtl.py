from patchUtil import *

UNIT_IS_ENEMY_EA = getFuncEA('ModelDevil$$get_IsEnemy')
UNIT_IS_PLAYER_EA = getFuncEA('ModelDevil$$get_IsPlayer')

GET_CRITICAL_RATIO = 'ModelDevil$$CriticalRatio'
GET_CRITICAL = 'ModelDevil$$Critical'
IS_CRITICAL = 'ModelDevil$$IsCritical'
# IS_UNIT_AILMENT_HIT_SUCCESS = 'ModelDevil$$IsBadStatusHit'
# GOT_SKILL_COST_FN = 'ModelDevil$$GetSkillTotalCost_44474'
UNIT_HAS_AVOID_DEATH = 'ModelDevil$$get_HasGoodAvoidDeath'
UNIT_HAS_BARRIER = 'ActionEffect$$calcConditionChange'
UNIT_HAS_CHARGEP_01 = 'ActionEffect$$calcPhysicalDamage'
UNIT_HAS_CHARGEM_01 = 'ActionEffect$$calcSkillDamage'
UNIT_HAS_CHARGEM_02 = 'ActionEffect$$calcDamage'
UNIT_HAS_REDIA = 'Control$$TurnRestore'
# UNIT_HAS_CHARM = 'ModelDevil$$hasBadStatus_Charm'
UNIT_HAS_CLOSE = '_InitializeCore_c__Iterator0$$MoveNext'
UNIT_HAS_CURSE_01 = 'DevilCalc$$Curse'
UNIT_HAS_CURSE_02 = 'SkillSummoner$$CurseUp'
UNIT_HAS_POISON = 'ActionEffect$$calcConditionEffect'
UNIT_HAS_WEAK_01 = 'ActionEffect$$calcCharge'
UNIT_HAS_WEAK_02 = 'ModelDevil$$GetBadStatusProbability'
MP_COST_DOWN = 'SkillPassive$$MPCostDown'

patches = [
    (
        'Zero cheat counts',
        'DataManager$$GetCheatCount',
        '',
        0,
        '00 00 a0 e3 ' +  # MOV r0, 0x00
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'PC can penetrate repels',
        'ModelDevil$$canPenatrateAttr',
        '',
        int('4', 16),
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA('ModelDevil$$canPenatrateAttr') +
                          int('4', 16)) + ' ' +
        'f0 8b bd e8 ' +  # LDMFD sp!, {r4-r9, r11, pc}
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'PC always avoids death',
        UNIT_HAS_AVOID_DEATH,
        '',
        int('8', 16),
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA(UNIT_HAS_AVOID_DEATH) +
                          int('8', 16)) + ' ' +
        '10 4c bd e8 ' +  # LDMFD sp!, {r4, r10, r11, lr}
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'PC always barrier',
        'ModelDevil$$get_HasGoodBarrier',
        '',
        int('8', 16),
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA('ModelDevil$$get_HasGoodBarrier') +
                          int('8', 16)) + ' ' +
        '10 4c bd e8 ' +  # LDMFD sp!, {r4, r10, r11, lr}
        '1e ff 2f e1 ' +  # BX lr
        '',
    ),
    # Having charge and meditate is a huge flag for banhammer
    (
        'PC always redia',
        UNIT_HAS_REDIA,
        '',
        int('80', 16),
        '0a 00 a0 e1 ' +  # MOV r0, r10
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA(UNIT_HAS_REDIA) +
                          int('84', 16)) + ' ' +
        ''
    ),
    (
        'EN always closed',
        UNIT_HAS_CLOSE,
        '',
        int('4dc', 16),
        getARMBLHexString(UNIT_IS_ENEMY_EA,
                          getFuncEA(UNIT_HAS_CLOSE) +
                          int('4dc', 16)) + ' ' +
        '06 00 00 ea ' +  # B (to CMP r0, #1  check if enemy)
        ''
    ),
    (
        'EN always cursed 0 of 1',
        UNIT_HAS_CURSE_01,
        '',
        int('58', 16),
        getARMBLHexString(UNIT_IS_ENEMY_EA,
                          getFuncEA(UNIT_HAS_CURSE_01) +
                          int('58', 16)) + ' ' +
        '06 00 00 ea ' +  # B (to CMP r0, #1  check if enemy)
        ''
    ),
    (
        'EN always cursed 1 of 1',
        UNIT_HAS_CURSE_02,
        '',
        int('74', 16),
        getARMBLHexString(UNIT_IS_ENEMY_EA,
                          getFuncEA(UNIT_HAS_CURSE_02) +
                          int('74', 16)) + ' ' +
        '06 00 00 ea ' +  # B (to CMP r0, #1  check if enemy)
        ''
    ),
    (
        'EN always poisoned',
        UNIT_HAS_POISON,
        '',
        int('f8', 16),
        '58 00 97 e5 ' +  # LDR r0, [r7, #0x58]
        getARMBLHexString(UNIT_IS_ENEMY_EA,
                          getFuncEA(UNIT_HAS_POISON) +
                          int('fc', 16)) + ' ' +
        ''
    ),
    (
        'EN always weak 0 of 1',
        UNIT_HAS_WEAK_01,
        '',
        int('d24', 16),
        getARMBLHexString(UNIT_IS_ENEMY_EA,
                          getFuncEA(UNIT_HAS_WEAK_01) +
                          int('d24', 16)) + ' ' +
        '06 00 00 ea ' +  # B (to CMP r0, #1  check if enemy)
        ''
    ),
    (
        'EN always weak 1 of 1',
        UNIT_HAS_WEAK_02,
        '',
        int('468', 16),
        '05 00 a0 e1 ' +  # MOV r0, r5
        getARMBLHexString(UNIT_IS_ENEMY_EA,
                          getFuncEA(UNIT_HAS_WEAK_02) +
                          int('46c', 16)) + ' ' +
        ''
    ),
    (
        'Always Attack Chanting',
        'ModelDevil$$get_BuffAttackChantPlayer',
        '',
        int('c', 16),
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA('ModelDevil$$get_BuffAttackChantPlayer') +
                          int('c', 16)) + ' ' +
        '10 d0 4b e2 ' +  # SUB sp, r11, #0x10
        '70 8c bd e8 ' +  # LDMFD sp!, {r4-r6, r10, r11, pc}
        ''
    ),
    (
        'Always Agility Chanting',
        'ModelDevil$$get_BuffAgilityChantPlayer',
        '',
        int('c', 16),
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA('ModelDevil$$get_BuffAgilityChantPlayer') +
                          int('c', 16)) + ' ' +
        '10 d0 4b e2 ' +  # SUB sp, r11, #0x10
        '70 8c bd e8 ' +  # LDMFD sp!, {r4-r6, r10, r11, pc}
        ''
    ),
    (
        'Always Vitality Chanting',
        'ModelDevil$$get_BuffVitalityChantPlayer',
        '',
        int('c', 16),
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA('ModelDevil$$get_BuffVitalityChantPlayer') +
                          int('c', 16)) + ' ' +
        '10 d0 4b e2 ' +  # SUB sp, r11, #0x10
        '70 8c bd e8 ' +  # LDMFD sp!, {r4-r6, r10, r11, pc}
        ''
    ),
    (
        'Player 67% crit (0 of 4)',
        IS_CRITICAL,
        '',
        int('14', 16),
        '07 90 a0 e1 ' +  # MOV r9, r7
        ''
    ),
    (
        'Player 67% crit (1 of 4)',
        IS_CRITICAL,
        '',
        int('1c8', 16),
        '09 10 a0 e1 ' +  # MOV r1, r9
        ''
    ),
    (
        'Player 67% crit (2 of 4)',
        GET_CRITICAL_RATIO,
        '',
        int('18', 16),
        '00 f0 20 e3 ' +  # NOP (originally BL ModelDevil$$get_LUK)
        ''
    ),
    (
        'Player 67% crit (3 of 4)',
        GET_CRITICAL_RATIO,
        '',
        int('34', 16),
        '07 10 a0 e1 ' +  # MOV r1, r7
        ''
    ),
    (
        'Player 67% crit (4 of 4)',
        GET_CRITICAL,
        '',
        int('10', 16),
        '01 20 a0 e1 ' +  # MOV r2, r1
        '02 00 a0 e1 ' +  # MOV r0, r2
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA(GET_CRITICAL) +
                          int('18', 16)) + ' ' +
        '00 10 a0 e1 ' +  # MOV r1, r0
        '01 00 51 e3 ' +  # CMP r1, #1  (is src a player unit?)
        '01 00 00 1a ' +  # BNE +1 (enemies don't get restore)
        '00 f0 20 e3 00 f0 20 e3 ' +
        # '02 00 a0 e1 ' +  # MOV r0, r2
        # getARMBLHexString(getFuncEA('ModelDevil$$procAutoRestore'),
        #                   getFuncEA(GET_CRITICAL) +
        #                   int('2c', 16)) + ' ' +
        '00 40 a0 e3 ' +  # MOV r4, #0
        '01 00 51 e3 ' +  # CMP r1, #1  (is src a player unit?)
        '43 40 a0 03 ' +  # MOVEQ r4, #67
        '4a 00 00 ea ' +  # B +4a (jump to random lessthanorequal of fn)
        ''
    ),
    (
        'Always avoid dark zones',
        'Model$$SkillAvoidDarkZone',
        '',
        int('0', 16),
        '01 00 a0 e3 ' +  # MOV r0, 01
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'Damage panel immunity',
        'Model$$SkillReduceDamage',
        '',
        int('0', 16),
        '00 00 00 e3 ' +  # MOV r2, 0x0000
        'c8 02 44 e3 ' +  # MOVT r2, 0x42c8  (0x42c80000 is +100.0%)
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'PC has repel PHY',
        'ModelDevil$$get_HasGoodRepelPhy',
        '',
        int('8', 16),
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA('ModelDevil$$get_HasGoodRepelPhy') +
                          int('8', 16)) + ' ' +
        '10 4c bd e8 ' +  # LDMFD sp!, {r4, r10, r11, lr}
        '1e ff 2f e1 ' +  # BX lr
        '',
    ),
    (
        'PC has repel MAG',
        'ModelDevil$$get_HasGoodRepelMag',
        '',
        int('8', 16),
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA('ModelDevil$$get_HasGoodRepelMag') +
                          int('8', 16)) + ' ' +
        '10 4c bd e8 ' +  # LDMFD sp!, {r4, r10, r11, lr}
        '1e ff 2f e1 ' +  # BX lr
        '',
    ),
    (
        'PC has repel almighty MAG',
        'ModelDevil$$get_HasGoodRepelAlmightyMag',
        '',
        int('8', 16),
        getARMBLHexString(UNIT_IS_PLAYER_EA,
                          getFuncEA('ModelDevil$$get_HasGoodRepelAlmightyMag') +
                          int('8', 16)) + ' ' +
        '10 4c bd e8 ' +  # LDMFD sp!, {r4, r10, r11, lr}
        '1e ff 2f e1 ' +  # BX lr
        '',
    ),
    # (
    #     'harder for EN to recover from bad status (0 of 1)',
    #     'ConditionArray$$update',
    #     '',
    #     int('1e8', 16),
    #     '06 10 a0 e1 ' +  # MOV r1, r6
    #     # (use ModelDevil instead of skills for BadStatusRecoveryRatio)
    #     ''
    # ),
    # (
    #     'harder for EN to recover from bad status (0 of 1)',
    #     'SkillPassive$$BadStatusRecoveryRatio',
    #     '',
    #     int('8', 16),
    #     '00 00 51 e3 ' +  # CMP r1, #0  (does ModelDevil exist?)
    #     '01 00 a0 e1 ' +  # MOV r0, r1
    #     '05 00 00 0a ' +  # BEQ to LDMFD
    #     getARMBLHexString(getFuncEA('ModelGroup$$get_IsPlayer'),
    #                       getFuncEA('SkillPassive$$BadStatusRecoveryRatio') +
    #                       int('14', 16)) + ' ' +
    #     '00 10 a0 e1 ' +  # MOV r1, r0
    #     '00 00 a0 e3 ' +  # MOV r0, 0000
    #     '00 0f 4b e3 ' +  # MOVT r0, bf00 (0xbf000000 is -1/2 chance)
    #     '01 00 51 e3 ' +  # CMP r1, #1  (is src a player unit?)
    #     '00 00 44 13 ' +  # MOVTNE r0, 4000 (0x40000000 is 2/1 chance)
    #     'f0 88 bd e8 ' +  # LDMFD sp!, {r4-r7, r11, pc}
    #     ''
    # ),
    # (
    #     'Always proc restore for PC',
    #     'Control$$WaveEnd_Init',
    #     '',
    #     int('638', 16),
    #     getARMBLHexString(getFuncEA('ModelGroup$$get_IsPlayer'),
    #                       getFuncEA('Control$$WaveEnd_Init') +
    #                       int('638', 16)) + ' ' +
    #     ''
    # ),
    # (
    #     'Skill Cost 0',
    #     GOT_SKILL_COST_FN,
    #     '',
    #     int('8', 16),
    #     getARMBLHexString(UNIT_IS_ENEMY_EA,
    #                       getFuncEA(GOT_SKILL_COST_FN) +
    #                       int('8', 16)) + ' ' +
    #     '00 10 a0 e1 ' +  # MOV r1, r0
    #     '64 00 a0 e3 ' +  # MOV r0, #100
    #     '01 00 51 e3 ' +  # CMP r1, #1  (is src an enemy unit?)
    #     '00 00 a0 13 ' +  # MOVNE r0, #0
    #     '1c d0 4b e2 ' +  # SUB sp, r11, #0x1c
    #     'f0 4f bd e8 ' +  # LDMFD sp!, {r4-r11, lr}
    #     '1e ff 2f e1 ' +  # BX LR
    #     ''
    # )
]

patchList(patches)
