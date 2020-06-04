# import patchUtil
'''
for version ups:
1. getFuncEALike('isCheat') and update all possible signature changes

'''

DROP_BATTLE_CRYSTAL_PER_FN = '_ZN10BattleUnit23getDropBattleCrystalPerEiPS_' + \
                             'bP14BattleUnitBuffP18BattlePassiveParamb'
DROP_HEART_CRYSTAL_PER_FN = '_ZN10BattleUnit22getDropHeartCrystalPerEiPS_' + \
                            'bP14BattleUnitBuffP18BattlePassiveParamb'
DROP_ZEL_PER_FN = '_ZN10BattleUnit13getDropZelPerEiPS_' + \
                  'bP14BattleUnitBuffP18BattlePassiveParamb'
DROP_ITEM_PER_FN = '_ZN10BattleUnit14getDropItemPerEiPS_' + \
                   'ibP14BattleUnitBuffP18BattlePassiveParamb'
BATTLE_PARTY_SET_PARTY_PASSIVE_FN = '_ZN11BattleParty19setPartyPassiveListEv'
BATTLE_UNIT_GET_ELEMENT_REVISE_FN = '_ZN10BattleUnit16getElementReviseEii'
BATTLE_UNIT_JUDGE_BAD_CONDITION_FN = '_ZN10BattleUnit17judgeBadConditionEifPS_'
BATTLE_UNIT_IS_PLAYER_EA = getFuncEA('_ZN10BattleUnit12isPlayerUnitEv')
BATTLE_UNIT_IS_GUARD_EA = getFuncEA('_ZN10BattleUnit7isGuardEv')

patches = [
    (
        'Totally not cheating here [1 of 2]',
        '_ZN21BattleUnitStatusCheck7isCheatEv',
        '',
        0,
        '00 20 ' +   # MOV R0, #1
        '70 47',     # BX LR
    ),
    (
        'Totally not cheating here [2 of 2]',
        '_ZN11MissionInfo7isCheatEv',
        '',
        0,
        '00 20 ' +   # MOV R0, #1
        '70 47',     # BX LR
    ),
    (
        'Always have element advantage',
        BATTLE_UNIT_GET_ELEMENT_REVISE_FN,
        '',
        0,
        '00 B5 ' +  # PUSH {LR}
        getBLHexString(BATTLE_UNIT_IS_PLAYER_EA,
                       getFuncEA(BATTLE_UNIT_GET_ELEMENT_REVISE_FN) +
                       int('2', 16)) + ' ' +  # battleUnit::isPlayerUnit
        'B6 EE 00 7A ' +  # VMOV.F32 S14, #0.5
        'F7 EE 08 7A ' +  # VMOV.F32 S15, #1.5
        '00 28 ' +  # CMP R0, #0
        '18 BF ' +  # IT NE (If...Then Not Equal) battleUnit here is dmg target
        'F0 EE 47 7A ' +  # VMOV.EQ S15, S14
        '17 EE 90 0A ' +  # VMOV R0, S15
        '00 BD'  # POP {PC}

    ),
    (
        'Status ailment immunity [2 of 2]',
        BATTLE_UNIT_JUDGE_BAD_CONDITION_FN,
        '',
        int('9a', 16),
        getBLHexString(BATTLE_UNIT_IS_PLAYER_EA,
                       getFuncEA(BATTLE_UNIT_JUDGE_BAD_CONDITION_FN) +
                       int('9a', 16)) + ' ' +  # battleUnit::isPlayerUnit
        '01 28 ' +  # CMP R0, #1
        '17 D0 ' +  # BEQ + 0x17 (to MOV R0, #0 target doesn't get ailment)
        'BF EE 00 8A ' +  # VMOV S16, #-1.0
        'C0 46 C0 46 '  # NOP padding
    ),
    (
        'All teammates are leaders [1 of 2]',
        BATTLE_PARTY_SET_PARTY_PASSIVE_FN,
        '',
        int('C6', 16),
        getBLHexString(BATTLE_UNIT_IS_PLAYER_EA,
                       getFuncEA(BATTLE_PARTY_SET_PARTY_PASSIVE_FN) +
                       int('C6', 16))  # battleUnit::isPlayerUnit
    ),
    (
        'All teammates are leaders [2 of 2]',
        BATTLE_PARTY_SET_PARTY_PASSIVE_FN,
        '',
        int('238', 16),
        getBLHexString(BATTLE_UNIT_IS_PLAYER_EA,
                       getFuncEA(BATTLE_PARTY_SET_PARTY_PASSIVE_FN) +
                       int('238', 16)) + ' ' +  # battleUnit::isPlayerUnit
        '01 28',  # CMP R0, R0
                  # (next line is BEQ so we want to always take that)
    ),
    (
        'Pets attack all the time',
        '_ZN7PetUnit16initActionAttackEv',
        '',
        int('18', 16),
        'C0 46',     # NOP (remove the CBZ branch decision)
    ),
    (
        'Battle crystal drops are 100% [2 of 3]',
        DROP_BATTLE_CRYSTAL_PER_FN,
        '',
        int('7E', 16),
        # battleUnit::isPlayerUnit
        getBLHexString(BATTLE_UNIT_IS_PLAYER_EA,
                       getFuncEA(DROP_BATTLE_CRYSTAL_PER_FN) + int('7E', 16)) +
        ' ' +
        '00 28 ' +  # CMP R0, #0
        'D3 D0 ' +  # BEQ <zero percent for enemy>
        '08 E0 ' +  # B <else branch to default operation>
        'C0 46'   # NOP padding
    ),
    (
        'Battle crystal drops are 100% [3 of 3]',
        DROP_BATTLE_CRYSTAL_PER_FN,
        '',
        int('168', 16),
        '17 EE 90 0A'  # VMOV.PL R0, S15
    ),
    (
        'Heart crystal drops are 100% [2 of 3]',
        DROP_HEART_CRYSTAL_PER_FN,
        '',
        int('7E', 16),
        # battleUnit::isPlayerUnit
        getBLHexString(BATTLE_UNIT_IS_PLAYER_EA,
                       getFuncEA(DROP_HEART_CRYSTAL_PER_FN) + int('7E', 16)) +
        ' ' +
        '00 28 ' +  # CMP R0, #0
        'D3 D0 ' +  # BEQ <zero percent for enemy>
        '08 E0 ' +  # B <else branch to default operation>
        'C0 46'   # NOP padding
    ),
    (
        'Heart crystal drops are 100% [3 of 3]',
        DROP_HEART_CRYSTAL_PER_FN,
        '',
        int('168', 16),
        '17 EE 90 0A'  # VMOV.PL R0, S15
    ),
    (
        'Zel drops are 100% [2 of 2]',
        DROP_ZEL_PER_FN,
        '',
        int('E6', 16),
        '17 EE 90 0A'  # VMOV.PL R0, S15
    ),
    (
        'Item drops are 100% [2 of 2]',
        DROP_ITEM_PER_FN,
        '',
        int('118', 16),
        '17 EE 90 0A'  # VMOV.PL R0, S15
    ),
]

PatchRule('Battle crystal drops are 100% [1 of 2]') \
    .findFuncBinary(DROP_BATTLE_CRYSTAL_PER_FN, '') \
    .getEA() \
    .patchFromEnd(2, '00 00 c8 42')  # flt_d99BD0 DCFS 100.0

PatchRule('Heart crystal drops are 100% [1 of 2]') \
    .findFuncBinary(DROP_HEART_CRYSTAL_PER_FN, '') \
    .getEA() \
    .patchFromEnd(2, '00 00 c8 42')  # flt_d99BD0 DCFS 100.0

PatchRule('Zel drops are 100% [1 of 2]') \
    .findFuncBinary(DROP_ZEL_PER_FN, '') \
    .getEA() \
    .patchFromEnd(2, '00 00 c8 42')  # flt_d99BD0 DCFS 100.0

PatchRule('Item drops are 100% [1 of 2]') \
    .findFuncBinary(DROP_ITEM_PER_FN, '') \
    .getEA() \
    .patchFromEnd(0, '00 00 c8 42')  # flt_d99BD0 DCFS 100.0

PatchRule('Status ailment immunity [1 of 2]') \
    .findFuncBinary(BATTLE_UNIT_JUDGE_BAD_CONDITION_FN, '') \
    .getEA() \
    .patchFromEnd(0, '00 00 aa 42')  # flt_d99BD0 DCFS 85.0


'''
Find all instances of BattleUnit::isGuard and change them to BattleUnit::isPlayer
'''
for xref in XrefsTo(BATTLE_UNIT_IS_GUARD_EA):
    ea_to_change = xref.frm
    patch_string = getBLHexString(BATTLE_UNIT_IS_PLAYER_EA, ea_to_change)
    for patch_index, val in enumerate(patch_string.strip().split(' ')):
        PatchByte(ea_to_change + patch_index, int(val, 16))
    print 'Patching all battleUnit::isGuard instances: {:x}' \
        .format(ea_to_change)
print 'Patching all battleUnit::isGuard instances: done!'


patchList(patches)
