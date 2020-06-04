from patchUtil import patchList, get_ea_from_binary, zero_ex, patch
from patchUtil import getARMBLHexString, getFuncEA
from idc import GetManyBytes

###
#  fix wait times
#  always make one of our players have the next turn
#  by making sure each enemy has a wait time of 100
#  and our units get a wait time of 1
###
# GET_UNIT_TYPES_SIGNATURE = 'A0 01 1E FF 2F E1 ? ? 90 E5'
GET_UNIT_TYPES_SIGNATURE = 'AC 00 90 E5 1E FF 2F E1 70 4C 2D E9'
GET_UNIT_TYPES_EA_OFFSET = 0
UNIT_TYPE_BYTES = ['{:02x}'.format(ord(char))
                   for char in GetManyBytes(
        get_ea_from_binary(GET_UNIT_TYPES_SIGNATURE) +
        GET_UNIT_TYPES_EA_OFFSET,
        1
    )]
# FIX_WAIT_TIMES_SIGNATURE = '10 4A 00 EE 00 60 A0 E1 00 00 56 E3 C0 8A B8 EE'
# 1.4.2 changes moved the target function as a separate name
# "BattleManager:calcWaitValue"
"""
FIX_WAIT_TIMES_SIGNATURE = '00 A0 A0 E3 00 00 A0 E3 07 10 A0 E1 05 20 A0 E1'
FIX_WAIT_TIMES_OFFSET = int('-84', 16)
patch(
    get_ea_from_binary(FIX_WAIT_TIMES_SIGNATURE),
    FIX_WAIT_TIMES_OFFSET,
    'fix wait times',
    '{} 50 90 e5 '.format(' '.join(UNIT_TYPE_BYTES)) +
    # example: 'a4 50 90 e5'
    # LDR r5, [r0, 0xa4]  (check battleUnit.getUnitType)
    '05 00 00 e3 ' +  # MOV r0, 0x5
    '02 00 55 e3 ' +  # CMP r5, 0x2  (unitType is enemy)
    '00 02 00 03 ' +  # MOVEQ r0, 0x200
    '1e ff 2f e1 ' +  # BX LR
    # '* * * EA ' +  # B + 52  (change from BEQ to B)
    ''
    )
"""


###
#  set start wait time to 0
###
"""
ADD_WAIT_SIGNATURE = '08 70 84 E5 0C 00 84 E5 ? ? ? EA ? ? ? EB'
patch(
    get_ea_from_binary(ADD_WAIT_SIGNATURE),
    int('-4', 16),
    'zero init wait time',
    '00 00 00 e3 ' +  # MOV r0, 0x0
    ''
)
"""

BATTLE_MANAGER_GET_ACTIVE_UNIT_EA = getFuncEA('BattleManager$$get_ActiveUnit')
BATTLE_UNIT_GET_UNIT_TYPE_EA = getFuncEA('BattleUnit$$get_unitType')
CALC_WAIT_VALUE_FN_NAME = 'BattleManager$$calcWaitValue'
CALC_WAIT_VALUE_FN_OFFSET = int('4', 16)
patches = [
    (
        'deactivate fox tracking',
        'Fox$$activate',
        '',
        0,
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    # (
    #     'player wait times are faster',
    #     CALC_WAIT_VALUE_FN_NAME,
    #     '',
    #     CALC_WAIT_VALUE_FN_OFFSET,
    #     '00 40 a0 e1 ' +  # MOV r4, r0
    #     getARMBLHexString(BATTLE_MANAGER_GET_ACTIVE_UNIT_EA,
    #                       getFuncEA(CALC_WAIT_VALUE_FN_NAME) +
    #                       CALC_WAIT_VALUE_FN_OFFSET + 4) + ' ' +
    #     getARMBLHexString(BATTLE_UNIT_GET_UNIT_TYPE_EA,
    #                       getFuncEA(CALC_WAIT_VALUE_FN_NAME) +
    #                       CALC_WAIT_VALUE_FN_OFFSET + 8) + ' ' +
    #     '00 50 a0 e1 ' +  # MOV r5, r0
    #     '05 00 00 e3 ' +  # MOV r0, 0x5
    #     '02 00 55 e3 ' +  # CMP r5, 0x2  (unitType is enemy)
    #     '00 02 00 03 ' +  # MOVEQ r0, 0x200
    #     'F0 8F BD E8 ' +  # LDMFD SP!, {R4-R11, PC}
    #     '1e ff 2f e1 ' +  # BX LR
    #     ''
    # )
    # (
    #     'player battle units are fast',
    #     'BattleUnit$$get_Agi',
    #     '',
    #     8,
    #     'a4 40 90 e5 ' +  # load unit type
    #     '64 00 00 e3 ' +  # set r0 to 100 agi
    #     '02 00 54 e3 ' +  # compare r4 to 2 (UnitType.enemy)
    #     '01 00 00 03 ' +  # set r0 to 1 agi if equal
    #     '10 4c bd e8 ' +  # LDMFD sp!, {R4, R10, R11, LR}
    #     '1e ff 2f e1 ' +  # BX LR
    #     ''
    # ),
    # (
    #     'player battle units are tough',
    #     'BattleUnit$$get_Pdef',
    #     '',
    #     8,
    #     'a4 40 90 e5 ' +  # load unit type
    #     'e8 03 00 e3 ' +  # set r0 to 1000 pdef
    #     '02 00 54 e3 ' +  # compare r4 to 2 (UnitType.enemy)
    #     '01 00 00 03 ' +  # set r0 to 1 agi if equal
    #     '10 4c bd e8 ' +  # LDMFD sp!, {R4, R10, R11, LR}
    #     '1e ff 2f e1 ' +  # BX LR
    #     ''
    # ),
    # (
    #     'player battle units are resistant',
    #     'BattleUnit$$get_Mdef',
    #     '',
    #     8,
    #     'a4 40 90 e5 ' +  # load unit type
    #     'e8 03 00 e3 ' +  # set r0 to 1000 mdef
    #     '02 00 54 e3 ' +  # compare r4 to 2 (UnitType.enemy)
    #     '01 00 00 03 ' +  # set r0 to 1 agi if equal
    #     '10 4c bd e8 ' +  # LDMFD sp!, {R4, R10, R11, LR}
    #     '1e ff 2f e1 ' +  # BX LR
    #     ''
    # ),
]

patchList(patches)