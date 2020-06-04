from patchUtil import *
from idc import GetManyBytes

UNIT_CTRL_GET_ENERGY_FN = 'UnitCtrl$$get_Energy'
IS_SKILL_READY_FN = 'UnitCtrl$$get_IsSkillReady'
IS_SKILL_READY_FN_PATCH_OFFSET = int('A4', 16)
UNIT_CHARGE_ENERGY_EA = getFuncEA('UnitCtrl$$ChargeEnergy')
UNIT_HEAL_AMOUNT_EA = getFuncEA('UnitCtrl$$SetRecovery')
UNIT_RECOVERY_RATE_EA = getFuncEA('UnitCtrl$$get_HpRecoveryRate')
UNIT_IS_MY_TURN_EA = getFuncEA('UnitCtrl$$isMyTurn')
UNIT_ANIM_SCALE = getFuncEA('BattleUnitBaseSpineController$$SetTimeScale')
JUDGE_SKILL_READY_AND_IS_MY_TURN_EA = \
    getFuncEA('UnitCtrl$$JudgeSkillReadyAndIsMyTurn')

ANDROID_FB_FN = 'AndroidFacebook$$CallFB'
ANDROID_FB_EA_PATCH_OFFSET = int('6c', 16)
# offset includes MOV R4, R0 code to set UnitCtrl to R4
# offset includes STMFD SP!, {R4, R10, R11, LR} which saves stack values

# the function that contains this binary uses UnitCtrl offset for
# m_fAtkRecastTime which is used for haste, set to 2.0f for max fun
# this fn should have a VLDR call and sets a float to an offset instruction
# i.e. STR [s0, r0, #<offset>]
SET_RECAST_TIME_SIGNATURE = '04 D0 4D E2 02 8B 2D ED 40 D0 4D E2 1F D0 C3 E7'
ATK_RECAST_TIME_OFFSET = int('74', 16)

# UNIT_UPDATE_DODGE_RATE_EA = getFuncEA('UnitCtrl$$updateDodgeRate')
RANDOM_RANGE_EA = getFuncEA('Random$$RandomRangeInt')

speed_offset = '{:02x}'.format(
    ord(
        GetManyBytes(
            get_ea_from_binary(SET_RECAST_TIME_SIGNATURE) +
            ATK_RECAST_TIME_OFFSET, 1
        )
    )
)

# NOP sequence:: 00 f0 20 e3
# UnitCtrl::IsAbnormalState
patches = [
    (
        'Always genuine',
        'Application$$get_genuine',
        '',
        int('38', 16),
        '01 10 00 E3 ' +  # MOV R1, 0x0001
        ''
    ),
    (
        'Always genuine check available',
        'Application$$get_genuineCheckAvailable',
        '',
        int('38', 16),
        '01 10 00 E3 ' +  # MOV R1, 0x0001
        ''
    ),
    # (
    #     'Make enemy IsSkillReady differentiator',
    #     'UnitUiCtrl$$updateEnemySkill',
    #     '',
    #     # NOTE: Always check if this code moves.
    #     #       BL UnitCtrl$$JudgeSkillReadyAndIsMyTurn might move
    #     int('1BC', 16),
    #     '02 20 A0 E3'
    #     # MOV R2, #2 (checking R1 in isSkillReady as 2 for enemy)
    # ),
    # (
    #     'No healing num effect',
    #     'UnitCtrl$$SetRecovery',
    #     '',
    #     int('448', 16),
    #     '00 F0 20 E3'  # NOP bl call to UnitCtrl$$createHealNumEffect
    # ),
    # (
    #     'No TP charge num effect',
    #     'UnitCtrl$$ChargeEnergy',
    #     '',
    #     int('137', 16),
    #     'EA'  # change 1A (BNE) to EA(B)
    # ),
    (
        'Remove FB Graph API lol v2',
        'AndroidFacebook$$CallFB',
        '',
        int('0', 16),
        #  Original FB code patched to exit early
        '1e ff 2f e1 ' +  # BX lr
        #
        #  UnitUiCtrl$$updatePlayerSkill redirects here
        #  Init phase to set objects we need
        'F0 4D 2D E9 ' +  # STMFD sp!, {r4-r8, r10, r11, lr}
        '04 60 A0 E1 ' +  # MOV r6, r4 (set UnitUICtrl to r6)
        '00 40 A0 E1 ' +  # MOV R4, R0 (set the unitCtrl to r4)
        '00 f0 20 e3 ' +  # do not overwrite dodge for now
        # 'b0 21 c4 e5 ' +
        # STRB r2, [r4,#0x360]  (set dodge value, 0x360, as flag)
        # we can use move rate, 0x1b0, as flag since no one is using it
        # 5 NOPS for padding
        '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
        #
        #  Battle manager and dead frame (dying animation frames) checks
        #  TODO: correct clean up jump offsets
        '90 00 96 e5 ' +  # LDR r0, [r6, #0x90] (get battle manager)
        '00 00 50 E3 ' +  # CMP R0, #0 (check if battle manager is null)
        '2f 00 00 0A ' +  # BEQ +2f    (jump to clean-up if no battle manager)
        'd4 00 90 e5 ' +  # LDR r0, [r0, #0xd4]
        # (get battle manager battle category)
        '05 00 50 E3 ' +  # CMP R0, #5 (check if it's coop)
        '2c 00 00 0A ' +  # BEQ +2c    (... and jump to clean-up if so)
        '90 00 96 e5 ' +  # LDR r0, [r6, #0x90] (get battle manager)
        'E0 00 90 e5 ' +  # LDR r0, [r0, #0xe0]
        # (get battle manager server dead frame)
        '00 00 50 E3 ' +  # CMP R0, #0 (check if it's not)
        '28 00 00 1A ' +  # BNE +28    (jump to clean-up if it's a dead frame)
        #
        #  Don't apply regen to enemies
        #
        '02 00 52 E3 ' +  # CMP R2, #2 (check if isEnemy)
        '26 00 00 0A ' +  # BEQ +26    (... and jump to new wave check if so)
        # 5 NOPS for padding
        '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
        #
        #  Regen code
        #  constant regen is bad because both setEnergy and setRecovery appends
        #  it to the battle log.  reverting to the old code.
        #  reverting to 0.2% lottery to make it more random.
        '00 10 A0 E3 ' +  # MOV R1, #0
        'e7 23 00 E3 ' +  # MOV R2, #999
        #    (0-999 since randomRange is inclusive on both ends)
        getARMBLHexString(RANDOM_RANGE_EA,
                          getFuncEA(ANDROID_FB_FN) +
                          ANDROID_FB_EA_PATCH_OFFSET + 8) + ' ' +
        '02 00 50 E3 ' +  # CMP R0, #2 (check if it's we're under 0.2%)
        '05 00 00 8A ' +  # BHI +5     (... and jump if not)
        #
        #  TP Charge by +0.125
        #  +0.125 if rate is constant per frame
        #  +15.625 scaling to the 0.8% lottery
        #  +62.5 scaling to the 0.2% lottery
        #
        '04 00 A0 E1 ' +  # MOV R0, R4 (unitCtrl)
        '00 20 00 e3 ' +  # MOV r2, 0x0000
        '7a 22 44 e3 ' +  # MOVT r2, 0x427a  (0x427a0000 is +62.5 TP charge)
        '09 10 A0 E3 ' +  # MOV R1, #9 (charge energy by energy change)
        '00 30 00 e3 ' +  # MOV r3, 0x0000  (no effect)
        '00 f0 20 e3 ' +  # do not overwrite dodge for now
        # getARMBLHexString(UNIT_CHARGE_ENERGY_EA,
        #                   getFuncEA(ANDROID_FB_FN) +
        #                   ANDROID_FB_EA_PATCH_OFFSET + 40) + ' ' +
        #
        #  Another 0.2% lottery
        #
        '00 10 A0 E3 ' +  # MOV R1, #0
        'e7 23 00 E3 ' +  # MOV R2, #999
        #    (0-999 since randomRange is inclusive on both ends)
        getARMBLHexString(RANDOM_RANGE_EA,
                          getFuncEA(ANDROID_FB_FN) +
                          ANDROID_FB_EA_PATCH_OFFSET + 52) + ' ' +
        '02 00 50 E3 ' +  # CMP R0, #2 (check if it's we're under 0.2%)
        '07 00 00 8A ' +  # BHI +7     (... and jump if not)
        #
        #  HP Recover
        #  +5 ~ +6.5 if the rate is constant per frame
        #  +625 to 825 scaling to the 0.8% lottery
        #  +2500 ~ +3250 scaling to the 0.2% lottery
        #
        'c4 19 00 E3 ' +  # MOV R1, #2500
        'b2 2c 00 E3 ' +  # MOV R2, #3250
        getARMBLHexString(RANDOM_RANGE_EA,
                          getFuncEA(ANDROID_FB_FN) +
                          ANDROID_FB_EA_PATCH_OFFSET + 72) + ' ' +
        '00 10 A0 E1 ' +  # MOV R1, R0
        # replace old +[100-200] HP lottery with nops
        '04 00 A0 E1 ' +  # MOV R0, R4 (unitCtrl)
        '04 20 A0 E1 ' +  # MOV R2, R4 (set R4 as recovery source)
        '00 30 A0 E3 ' +  # MOV R3, #0 (no heal circle effect)
        '00 f0 20 e3 ' +  # do not overwrite dodge for now
        # getARMBLHexString(UNIT_HEAL_AMOUNT_EA,
        #                   getFuncEA(ANDROID_FB_FN) +
        #                   ANDROID_FB_EA_PATCH_OFFSET + 92) + ' ' +
        #
        #  moveSpeed set to 2.0
        #
        '00 00 00 e3 ' +  # MOV r0, 0x0000
        '1a 0f 43 e3 ' +  # MOVT r0, 0x3f1a (0x3f1a0000 is 0.60)
        # (0x3f000000 is 0.5 for m_fAtkRecastTime)
        '{} 84 e5 '.format(zero_ex(speed_offset, 2)) +
        # STR r0, [r4,#0x210]  (set m_fAtkRecastTime to R0)
        '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
        '00 f0 20 e3 00 f0 20 e3 ' +
        '04 00 00 EA ' +  # B +4    (jump to cleanup)
        # 5 NOPS for padding
        '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
        #
        # Clean-up section
        #
        '04 00 A0 E1 ' +  # MOV R0, R4 (unitCtrl)
        getARMBLHexString(JUDGE_SKILL_READY_AND_IS_MY_TURN_EA,
                          getFuncEA(ANDROID_FB_FN) +
                          ANDROID_FB_EA_PATCH_OFFSET + 164) + ' ' +
        'F0 8D BD E8 ' +  # LDMFD sp!, {r4-r8, r10, r11, pc}
        '1e ff 2f e1 ' +  # BX LR
        # 5 NOPS for padding
        '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
        ''
        # TODO: Call JudgeSkillReadyAndIsMyTurn and BXLR its value
    ),
    (
        'Redirect from UnitUiCtrl$$updatePlayerSkill',
        'UnitUiCtrl$$updatePlayerSkill',
        '',
        int('398', 16),
        '01 20 A0 E3 ' +  # MOV R2, #1  flag this jump as player's
        # NOTE: Always check if this code moves.
        #       BL UnitCtrl$$JudgeSkillReadyAndIsMyTurn might move
        getARMBLHexString(getFuncEA(ANDROID_FB_FN) + 4,
                          getFuncEA('UnitUiCtrl$$updatePlayerSkill') +
                          int('39c', 16)) + ' ' +
        ''
    ),
    # (
    #     # Doesn't exactly work because it is only triggered on unitctrl$$init
    #     # but it sets the enemy dodge to zero for now (as the title says)
    #     'WIP dogeFishCrit',
    #     'UnitCtrl$$get_PhysicalCriticalZero',
    #     '',
    #     int('10', 16),
    #     'b0 01 d1 e5 ' +  # LDRB R0, [R1,#0x360] (load isPlayerFlag)
    #     '00 20 a0 e3 ' +  # MOV R2, #0
    #     '01 00 50 e3 ' +  # CMP R0, #1 (check if unit already has buffs)
    #     '00 25 00 03 ' +  # MOVEQ R2, #0x2500 (1280; 5% of 2000.0 is 100)
    #     # '9b 22 00 03 ' +  # MOVEQ R2, #667 (5% of 2000.0 is 100)
    #     # 'a0 20 00 03 ' +  # MOVEQ R2, #0x160 (max in-game so far is 120)
    #     '00 10 a0 e3 ' +  # MOV R1, #0
    #     '31 00 00 ea ' +  # B +31
    #     ''
    # ),
    # (
    #     # Doesn't exactly work because it is only triggered on unitctrl$$init
    #     # but it sets the enemy dodge to zero for now (as the title says)
    #     'WIP dogeMageCrit',
    #     'UnitCtrl$$get_MagicCriticalZero',
    #     '',
    #     int('10', 16),
    #     'b0 01 d1 e5 ' +  # LDRB R0, [R1,#0x360] (load isPlayerFlag)
    #     '00 20 a0 e3 ' +  # MOV R2, #0
    #     '01 00 50 e3 ' +  # CMP R0, #1 (check if unit already has buffs)
    #     '00 25 00 03 ' +  # MOVEQ R2, #0x2500 (1280; 5% of 2000.0 is 100)
    #     # '9b 22 00 03 ' +  # MOVEQ R2, #667 (5% of 2000.0 is 100)
    #     # 'a0 20 00 03 ' +  # MOVEQ R2, #0x160 (max in-game so far is 120)
    #     '00 10 a0 e3 ' +  # MOV R1, #0
    #     '31 00 00 ea ' +  # B +31
    #     ''
    # ),
]

patchList(patches)
