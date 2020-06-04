from patchUtil import *
from idc import GetManyBytes
# UNIT_CTRL_GET_ENERGY_FN = 'UnitCtrl$$get_Energy'
# IS_SKILL_READY_FN = 'UnitCtrl$$get_IsSkillReady'
# IS_SKILL_READY_FN_PATCH_OFFSET = int('A4', 16)
# UNIT_CHARGE_ENERGY_EA = getFuncEA('UnitCtrl$$ChargeEnergy')
# UNIT_HEAL_AMOUNT_EA = getFuncEA('UnitCtrl$$SetRecovery')
# UNIT_RECOVERY_RATE_EA = getFuncEA('UnitCtrl$$get_HpRecoveryRate')
# UNIT_IS_MY_TURN_EA = getFuncEA('UnitCtrl$$isMyTurn')
# UNIT_ANIM_SCALE = getFuncEA('BattleUnitBaseSpineController$$SetTimeScale')
# JUDGE_SKILL_READY_AND_IS_MY_TURN_EA = \
#     getFuncEA('UnitCtrl$$JudgeSkillReadyAndIsMyTurn')

ANDROID_FB_FN = 'AndroidFacebook$$CallFB'
ANDROID_FB_EA_PATCH_OFFSET = int('6c', 16)
# offset includes MOV R4, R0 code to set UnitCtrl to R4
# offset includes STMFD SP!, {R4, R10, R11, LR} which saves stack values

# this function is needed to be patched just in case we mess things up
# fn should have comments about calling UnityEngine.Application::get_genuine()
# and an il2cpp_resolve_icall_0 after
APP_GET_GENUINE_SIGNATURE = '00 00 8F E0 00 00 84 E0 80 15 80 E5'

# this function is needed to be patched just in case we mess things up
# fn should have comments about calling
# UnityEngine.Application::get_genuineCheckAvailable()
# and an il2cpp_resolve_icall_0 after
APP_GET_GENUINE_CHECK_SIGNATURE = '00 00 8F E0 00 00 84 E0 84 15 80 E5'

# the function that contains this binary uses UnitCtrl offset for
# m_fAtkRecastTime which is used for haste, set to 2.0f for max fun
# this fn should have a VLDR call and sets a float to an offset instruction
# i.e. STR [s0, r0, #<offset>]
SET_RECAST_TIME_SIGNATURE = '04 D0 4D E2 02 8B 2D ED 40 D0 4D E2 1F D0 C3 E7'
ATK_RECAST_TIME_OFFSET = int('74', 16)

# this signature +10 will have a
# MOV r1, #0; BL UnitCtrl$$JudgeSkillReadyAndIsMyTurn
UPDATE_PLAYER_SKILL_SIGNATURE = '33 00 00 1A 00 00 56 E3 3D 00 00 0A'

# this signature +30 will have a call to UnitCtrl$$JudgeSkillReadyAndIsMyTurn
UPDATE_ENEMY_SKILL_SIGNATURE = '00 70 E0 E3 00 00 50 E3 04 00 00 0A'

# this fn is used on our regen effect
# this signature -4 is UnitCtrl$$createHealNumEffect
SET_RECOVERY_SIGNATURE = '01 00 56 E3 32 FF FF 1A 10 30 9B E5'
# since IDE doesn't parse this area normally, we explicitly set the offset
# of the signature so the script can know where the start of function is
SET_RECOVERY_SIGNATURE_OFFSET = int('44c', 16)

# this fn is used on our regen effect
# change this signature +27 from BNE to B to avoid drawing energy recover vals
CHARGE_ENERGY_SIGNATURE = '07 30 A0 E1 00 0A 38 EE 10 1A 10 EE'
# since IDE doesn't parse this area normally, we explicitly set the offset
# of the signature so the script can know where the start of function is
CHARGE_ENERGY_SIGNATURE_OFFSET = int('10c', 16)

# this fn is used on our regen effect
JUDGE_SKILL_READY_AND_IS_MY_TURN_SIGNATURE = \
    '00 10 A0 E1 00 00 A0 E3 01 00 51 E3 04 00 A0 01'

# we patch this and everybody is happy
ANDROID_CALLFB_SIGNATURE = '00 00 8F E0 20 50 95 E5 00 00 91 E7 00 60 90 E5'
# since IDE doesn't parse this area normally, we explicitly set the offset
# of the signature so the script can know where the start of function is
ANDROID_CALLFB_SIGNATURE_OFFSET = int('5c', 16)


# TODO- research moveRate offset at a later time

# UNIT_UPDATE_DODGE_RATE_EA = getFuncEA('UnitCtrl$$updateDodgeRate')
# RANDOM_RANGE_EA = getFuncEA('Random$$RandomRangeInt')

# NOP sequence:: 00 f0 20 e3
# UnitCtrl::IsAbnormalState

###
# Always Genuine Patch
###
patch(get_start_ea_from_binary(APP_GET_GENUINE_SIGNATURE),
      int('38', 16),
      'Always genuine',
      '01 10 00 E3 ' +  # MOV R1, 0x0001
      '')
###
# Always genuine check available
###
patch(get_start_ea_from_binary(APP_GET_GENUINE_CHECK_SIGNATURE),
      int('38', 16),
      'Always genuine check available',
      '01 10 00 E3 ' +  # MOV R1, 0x0001
      '')

###
# Make enemy IsSkillReady differentiator
###
patch(get_start_ea_from_binary(UPDATE_ENEMY_SKILL_SIGNATURE),
      int('1bc', 16),
      'Make enemy IsSkillReady differentiator',
      '02 20 A0 E3 ' +
      # MOV R2, #2 (checking R1 in isSkillReady as 2 for enemy)
      '')

###
# No healing num effect
###
recover_health_ea = get_ea_from_binary(SET_RECOVERY_SIGNATURE) - \
                    SET_RECOVERY_SIGNATURE_OFFSET
patch(recover_health_ea + SET_RECOVERY_SIGNATURE_OFFSET,
      -int('4', 16),
      'No healing num effect',
      '00 F0 20 E3 ' +  # NOP bl call to UnitCtrl$$createHealNumEffect
      '')

###
# No TP charge effect
###
charge_energy_ea = get_ea_from_binary(CHARGE_ENERGY_SIGNATURE) - \
                   CHARGE_ENERGY_SIGNATURE_OFFSET
patch(charge_energy_ea + CHARGE_ENERGY_SIGNATURE_OFFSET,
      int('2b', 16),
      'No TP charge effect',
      'EA ' +  # change 1A (BNE) to EA(B)
      '')

###
# Redirect from UnitUiCtrl$$updatePlayerSkill
###
call_fb_start_ea = get_ea_from_binary(ANDROID_CALLFB_SIGNATURE) - \
                   ANDROID_CALLFB_SIGNATURE_OFFSET
update_player_ea = get_ea_from_binary(UPDATE_PLAYER_SKILL_SIGNATURE)
patch(update_player_ea,
      int('10', 16),
      'Redirect from UnitUiCtrl$$updatePlayerSkill',
      '01 20 A0 E3 ' +  # MOV R2, #1  flag this jump as player's
      # NOTE: Always check if this code moves.
      #       BL UnitCtrl$$JudgeSkillReadyAndIsMyTurn might move
      getARMBLHexString(call_fb_start_ea + 4,
                        update_player_ea + int('14', 16)) + ' ' +
      '')

###
# Remove FB Graph API lol v2
###
speed_offset = '{:02x}'.format(
    ord(
        GetManyBytes(
            get_ea_from_binary(SET_RECAST_TIME_SIGNATURE) +
            ATK_RECAST_TIME_OFFSET, 1
        )
    )
)
patch(call_fb_start_ea,
      int('0', 16),
      'Remove FB Graph API lol v2',
      #  Original FB code patched to exit early
      '1e ff 2f e1 ' +  # BX lr
      #
      #  UnitUiCtrl$$updatePlayerSkill redirects here
      #  Init phase to set objects we need
      'F0 4D 2D E9 ' +  # STMFD sp!, {r4-r8, r10, r11, lr}
      '04 60 A0 E1 ' +  # MOV r6, r4 (set UnitUICtrl to r6)
      '00 40 A0 E1 ' +  # MOV R4, R0 (set the unitCtrl to r4)
      '00 f0 20 e3 ' +  # NOP for now until we know how to get move rate
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
      #  replace 5% lottery code with nops
      '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
      #
      #  TP Charge by +0.125
      #
      '04 00 A0 E1 ' +  # MOV R0, R4 (unitCtrl)
      '00 20 00 e3 ' +  # MOV r2, 0x0000
      '00 2e 43 e3 ' +  # MOVT r2, 0x3e00  (0x3e800000 is +0.125 TP charge)
      '09 10 A0 E3 ' +  # MOV R1, #9 (charge energy by energy change)
      '00 30 00 e3 ' +  # MOV r3, 0x0000  (no effect)
      getARMBLHexString(charge_energy_ea,
                        call_fb_start_ea +
                        ANDROID_FB_EA_PATCH_OFFSET + 36) + ' ' +
      #
      #  HP Recover +5
      #
      '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
      # replace old +[100-200] HP lottery with nops
      '04 00 A0 E1 ' +  # MOV R0, R4 (unitCtrl)
      '05 10 A0 E3 ' +  # MOV R1, #5
      '04 20 A0 E1 ' +  # MOV R2, R4 (set R4 as recovery source)
      '00 30 A0 E3 ' +  # MOV R3, #0 (no heal circle effect)
      getARMBLHexString(recover_health_ea,
                        call_fb_start_ea +
                        ANDROID_FB_EA_PATCH_OFFSET + 68) + ' ' +
      #
      #  moveSpeed set to 2.0
      #
      '00 00 00 e3 ' +  # MOV r0, 0x0000
      '00 0f 43 e3 ' +  # MOVT r0, 0x3f00
      # (0x3f000000 is 0.5 for m_fAtkRecastTime)
      '{} 84 e5 '.format(zero_ex(speed_offset, 2)) +
      # '14 02 84 e5 ' +
      # STR r0, [r4,#0x214]  (set m_fAtkRecastTime to R0)
      '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
      '00 f0 20 e3 00 f0 20 e3 ' +
      '04 00 00 EA ' +  # B +4    (jump to cleanup)
      # 5 NOPS for padding
      '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
      #
      # Clean-up section
      #
      '04 00 A0 E1 ' +  # MOV R0, R4 (unitCtrl)
      getARMBLHexString(
          get_start_ea_from_binary(JUDGE_SKILL_READY_AND_IS_MY_TURN_SIGNATURE),
          call_fb_start_ea +
          ANDROID_FB_EA_PATCH_OFFSET + 140) + ' ' +
      'F0 8D BD E8 ' +  # LDMFD sp!, {r4-r8, r10, r11, pc}
      '1e ff 2f e1 ' +  # BX LR
      # 5 NOPS for padding
      '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
      ''
      # TODO: Call JudgeSkillReadyAndIsMyTurn and BXLR its value
      )

patches = [
    # (
    #     'Always genuine',
    #     'Application$$get_genuine',
    #     '',
    #     int('38', 16),
    #     '01 10 00 E3 ' +  # MOV R1, 0x0001
    #     ''
    # ),
    # (
    #     'Always genuine check available',
    #     'Application$$get_genuineCheckAvailable',
    #     '',
    #     int('38', 16),
    #     '01 10 00 E3 ' +  # MOV R1, 0x0001
    #     ''
    # ),
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
    # (
    #     'Remove FB Graph API lol v2',
    #     'AndroidFacebook$$CallFB',
    #     '',
    #     int('0', 16),
    #     #  Original FB code patched to exit early
    #     '1e ff 2f e1 ' +  # BX lr
    #     #
    #     #  UnitUiCtrl$$updatePlayerSkill redirects here
    #     #  Init phase to set objects we need
    #     'F0 4D 2D E9 ' +  # STMFD sp!, {r4-r8, r10, r11, lr}
    #     '04 60 A0 E1 ' +  # MOV r6, r4 (set UnitUICtrl to r6)
    #     '00 40 A0 E1 ' +  # MOV R4, R0 (set the unitCtrl to r4)
    #     'b0 21 c4 e5 ' +
    #     # STRB r2, [r4,#0x360]  (set dodge value, 0x360, as flag)
    #     # we can use move rate, 0x1b0, as flag since no one is using it
    #     # 5 NOPS for padding
    #     '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
    #     #
    #     #  Battle manager and dead frame (dying animation frames) checks
    #     #  TODO: correct clean up jump offsets
    #     '90 00 96 e5 ' +  # LDR r0, [r6, #0x90] (get battle manager)
    #     '00 00 50 E3 ' +  # CMP R0, #0 (check if battle manager is null)
    #     '2f 00 00 0A ' +  # BEQ +2f    (jump to clean-up if no battle manager)
    #     'd4 00 90 e5 ' +  # LDR r0, [r0, #0xd4]
    #     # (get battle manager battle category)
    #     '05 00 50 E3 ' +  # CMP R0, #5 (check if it's coop)
    #     '2c 00 00 0A ' +  # BEQ +2c    (... and jump to clean-up if so)
    #     '90 00 96 e5 ' +  # LDR r0, [r6, #0x90] (get battle manager)
    #     'E0 00 90 e5 ' +  # LDR r0, [r0, #0xe0]
    #     # (get battle manager server dead frame)
    #     '00 00 50 E3 ' +  # CMP R0, #0 (check if it's not)
    #     '28 00 00 1A ' +  # BNE +28    (jump to clean-up if it's a dead frame)
    #     #
    #     #  Don't apply regen to enemies
    #     #
    #     '02 00 52 E3 ' +  # CMP R2, #2 (check if isEnemy)
    #     '26 00 00 0A ' +  # BEQ +26    (... and jump to new wave check if so)
    #     # 5 NOPS for padding
    #     '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
    #     #
    #     #  Regen code
    #     #  replace 5% lottery code with nops
    #     '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
    #     #
    #     #  TP Charge by +0.125
    #     #
    #     '04 00 A0 E1 ' +  # MOV R0, R4 (unitCtrl)
    #     '00 20 00 e3 ' +  # MOV r2, 0x0000
    #     '00 2e 43 e3 ' +  # MOVT r2, 0x3e00  (0x3e800000 is +0.125 TP charge)
    #     '09 10 A0 E3 ' +  # MOV R1, #9 (charge energy by energy change)
    #     '00 30 00 e3 ' +  # MOV r3, 0x0000  (no effect)
    #     getARMBLHexString(UNIT_CHARGE_ENERGY_EA,
    #                       getFuncEA(ANDROID_FB_FN) +
    #                       ANDROID_FB_EA_PATCH_OFFSET + 36) + ' ' +
    #     #
    #     #  HP Recover +5
    #     #
    #     '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
    #     # replace old +[100-200] HP lottery with nops
    #     '04 00 A0 E1 ' +  # MOV R0, R4 (unitCtrl)
    #     '05 10 A0 E3 ' +  # MOV R1, #5
    #     '04 20 A0 E1 ' +  # MOV R2, R4 (set R4 as recovery source)
    #     '00 30 A0 E3 ' +  # MOV R3, #0 (no heal circle effect)
    #     getARMBLHexString(UNIT_HEAL_AMOUNT_EA,
    #                       getFuncEA(ANDROID_FB_FN) +
    #                       ANDROID_FB_EA_PATCH_OFFSET + 68) + ' ' +
    #     #
    #     #  moveSpeed set to 2.0
    #     #
    #     '00 00 00 e3 ' +  # MOV r0, 0x0000
    #     '00 0f 43 e3 ' +  # MOVT r0, 0x3f00
    #     # (0x3f000000 is 0.5 for m_fAtkRecastTime)
    #     '10 02 84 e5 ' +
    #     # STR r0, [r4,#0x210]  (set m_fAtkRecastTime to R0)
    #     '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
    #     '00 f0 20 e3 00 f0 20 e3 ' +
    #     '04 00 00 EA ' +  # B +4    (jump to cleanup)
    #     # 5 NOPS for padding
    #     '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
    #     #
    #     # Clean-up section
    #     #
    #     '04 00 A0 E1 ' +  # MOV R0, R4 (unitCtrl)
    #     getARMBLHexString(JUDGE_SKILL_READY_AND_IS_MY_TURN_EA,
    #                       getFuncEA(ANDROID_FB_FN) +
    #                       ANDROID_FB_EA_PATCH_OFFSET + 140) + ' ' +
    #     'F0 8D BD E8 ' +  # LDMFD sp!, {r4-r8, r10, r11, pc}
    #     '1e ff 2f e1 ' +  # BX LR
    #     # 5 NOPS for padding
    #     '00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 00 f0 20 e3 ' +
    #     ''
    #     # TODO: Call JudgeSkillReadyAndIsMyTurn and BXLR its value
    # ),
    # (
    #     'Redirect from UnitUiCtrl$$updatePlayerSkill',
    #     'UnitUiCtrl$$updatePlayerSkill',
    #     '',
    #     int('398', 16),
    #     '01 20 A0 E3 ' +  # MOV R2, #1  flag this jump as player's
    #     # NOTE: Always check if this code moves.
    #     #       BL UnitCtrl$$JudgeSkillReadyAndIsMyTurn might move
    #     getARMBLHexString(getFuncEA(ANDROID_FB_FN) + 4,
    #                       getFuncEA('UnitUiCtrl$$updatePlayerSkill') +
    #                       int('39c', 16)) + ' ' +
    #     ''
    # ),
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

# patchList(patches)
