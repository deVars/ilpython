import idc
import patchUtil

GET_ORIGINAL_UNIT = 'getOriginalUnit'
IS_PLAYER_CONTROLLED = 'isPlayerControlled'
NEW_INSTANCE_GEAR_RANGE = 'newInstanceGearRange'
NEW_INSTANCE_SYSTEM_TUPLE = 'newInstanceSystemTuple'
GEAR_MAX_RANGE = 'gearMaxRange'
GEAR_MAX_RANGE_VALUE = 4

patchStrings = dict([
    (GET_ORIGINAL_UNIT, findPatchString({
            'name': 'get original unit',
            'srcFnName': 'GameCore.BattleFuncs::calcDuelHeal',
            'patchLength': 5,
            'offset': 27,
        })
    ),
    (IS_PLAYER_CONTROLLED, findPatchString({
            'name': 'is player controlled',
            'srcFnName': 'GameCore.BattleFuncs::calcDuelHeal',
            'patchLength': 5,
            'offset': 32,
        })
    ),
    (NEW_INSTANCE_GEAR_RANGE, findPatchString({
            'name': 'gear range',
            'srcFnName': 'Unit::gearRange',
            'patchLength': 5,
            'offset': 159,
        })
    ),
    (NEW_INSTANCE_SYSTEM_TUPLE, findPatchString({
            'name': 'internal system tuple',
            'srcFnName': 'Panel::getEffectsAddRange',
            'patchLength': 5,
            'offset': 97,
        })
    ),
    (GEAR_MAX_RANGE, '{:02x}'.format(GEAR_MAX_RANGE_VALUE)
    ),
])

patches = [
    # ('ap consumed is 1 [1 of 2]',
    # 'QuestConverterData::SetData',
    # '',
    # int('4e', 16),
    # '17 ' +  #ldc.i4.1
    # '00'  # nop padding
    # ),
    # ('ap consumed is 1 [2 of 2]',
    # 'Quest0028Menu::get_lost_ap',
    # '',
    # int('0', 16),
    # '17 2a ' +  #ldc.i4.1, ret
    # '00 00 00 00'  # nop padding
    # ),
    # ('no battle count limitation',
    # 'QuestConverterData::SetData',
    # '',
    # int('d5', 16),
    # '16 ' +  #ldnull
    # '00 00 00 00 00 ' +  # nop padding
    # '00 00 00 00 00'  # nop padding
    # ),
    ('default weapon range',
    'Unit::gearRange',
    '',
    0,
    '02 ' +
    patchStrings[IS_PLAYER_CONTROLLED] +
    ' 2c 09 17 1f ' +
    patchStrings[GEAR_MAX_RANGE] + ' ' +
    patchStrings[NEW_INSTANCE_GEAR_RANGE] +
    ' 2a 17 17 ' +
    patchStrings[NEW_INSTANCE_GEAR_RANGE] +
    ' 2a'),

    ('bullet ranges',
    'GameCore.BattleFuncs::getAttackStatusArray',
    '',
    270,
    '11 05 07 ' +
    patchStrings[IS_PLAYER_CONTROLLED] +
    ' 2c 0a 16 1f ' +
    patchStrings[GEAR_MAX_RANGE] + ' ' +
    patchStrings[NEW_INSTANCE_SYSTEM_TUPLE] +
    ' 2b 07 16 16 ' + patchStrings[NEW_INSTANCE_SYSTEM_TUPLE] +
    ' 2b 11 00 00 00 00'),

    ('attack count',
    'GameCore.BattleFuncs::attackCount',
    '',
    0,
    '02 ' +
    patchStrings[GET_ORIGINAL_UNIT] +
    ' ' +
    patchStrings[IS_PLAYER_CONTROLLED] +
    ' 2c 02 19 2a 17 2a 00 00 00'),

    ('half multiplier for enemy ::look at GameCore.BattleFuncs::calcDuelHeal for fn addresses',
    'BeforeDuelUnitParameter::GetSkillMul',
    '',
    0,
    '02 ' +
    patchStrings[GET_ORIGINAL_UNIT] +
    ' ' +
    patchStrings[IS_PLAYER_CONTROLLED] +
    ' 2c 07 22 00 00 80 3f 2b 05 22 00 00 00 3f 2a 00 00 00 00 00'),

    ('move cost::set ignore move cost flag if pc',
    'GameCore.BattleFuncs::createMovePanels',
    '',
    38,
    '05 ' + patchStrings[IS_PLAYER_CONTROLLED] + ' 00 00 00 00 00'),
    # ('move cost::enemy movement is pinned to 1 square',
    # 'SM.PlayerUnit::FromEnemy',
    # '7d d4 1c 00 04 06',
    # 6,
    # '17 2b 12 00 00 00'),
    # ('critical calculation::from be unit',
    # 'BeforeDuelUnitParameter::FromBeUnit',
    # '7d 0d 06 00 04 11 2e 11 2e',
    # 9,
    # '7b 07 06 00 04'),
    # ('critical calculation::from colo unit',
    # 'BeforeDuelUnitParameter::FromBeColosseumUnit',
    # '7d 0d 06 00 04 11 25 11 25',
    # 9,
    # '7b 07 06 00 04'),
    # ('luck calculation::from colo unit',
    # 'BeforeDuelUnitParameter::FromBeColosseumUnit',
    # '7d 06 06 00 04 11 25',
    # 7,
    # '02 6f db 06 00 06 2c 07 20 c8 00 00 00 2b 01 16 2b 07 00 00 00'),
    ('enemyLevelFix1: calc enemy parameter -- fix growth 0.10',
    'SM.PlayerUnit::CalcEnemyParameter',
    '',
    0,
    '03 6b 02 22 cc cc cc 3d 5a 58 2b 16'),

    ('enemyLevelFix2: (enemyLevel + level correction) * 5 (1 of 2): remove add and conv.r4 from battlestageenemy.level ::check function address',
    'SM.PlayerUnit::FromEnemy',
    '',
    54,
    '00 00'),

    ('enemyLevelFix2: (enemyLevel + level correction) * 5 (2 of 2): multiply everything by 5 and conv.r4 for type compliance ::check function address',
    'SM.PlayerUnit::FromEnemy',
    '',
    67,
    '00 58 1b 5a 6b 00 00 00 00 00 00 00'),

    ('enemyLevelFix3::part1: cap enemy skill level to 1',
    '<FromEnemy>c__AnonStoreyBB4::<>m__86D',
    '',
    0,
    '17 00 00 00 00 00 00 00 00 00 00'),

    ('enemyLevelFix3::part2: cap enemy leader skill level to 1',
    '<FromEnemy>c__AnonStoreyBB4::<>m__86F',
    '',
    0,
    '17 00 00 00 00 00 00 00 00 00 00'),

    ('enemyLevelFix3::part3: always refer to level scaling method',
    'SM.PlayerUnit::FromEnemy',
    '',
    1204,
    '38 cf 00 00 00'),

    ('max items are set to cap ::change ldstr max_items to max_items_cap ::check function addresses!',
    'SM.Player::.ctor_0',
    '72 43 18 01 70',
    0,
    '72 e3 16 01 70'),

    ('max units are set to cap ::change ldstr max_units to max_units_cap ::check function addresses!',
    'SM.Player::.ctor_0',
    '72 b5 16 01 70',
    0,
    '72 dd 18 01 70'
    ),

    ('AIList threshold is set from 50 to 16',
    'GameCore.AILisp::.ctor',
    '6a',
    -1,
    '10'
    ),

    ('Disable FBUnityInit',
    'Facebook.Unity.FB::Init_0',
    '',
    0,
    '2a 00 00 00 00'
    ),

]

patchList(patches)

'''
The next rule is to patch campaign map non-table generated enemies
so they don't use the data values at all.
Stat values are:
(0)tech, (1)speed, (2)spirit, (3)strength, (4)vitality, (5)hp, (6)magic, (7)luck in order
final one is level calculation
Formula is:
attrib_value = (calculated level * 5) [from patch on top] / 16


'''

DIVIDE_CALC_LEVEL_BY_16 = '07 69 1f 10 5b 00 00 00 00 00 00'
DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT = len(DIVIDE_CALC_LEVEL_BY_16.split(' '))
USE_CALCULATED_LEVEL =    '07 69 00 00 00 00 00 00 00 00 00'
#  don't patch HP, maybe damage dealt is also a KPI for growth
#.patch(225 + 5 * (DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT + 5 + 1 + 5), DIVIDE_CALC_LEVEL_BY_16) \
# PatchRule('non-table enemy stat gen') \
#     .findFuncBinary('SM.PlayerUnit::FromEnemy', '') \
#     .patch(225, DIVIDE_CALC_LEVEL_BY_16) \
#     .patch(225 + 1 * (DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT + 5 + 1 + 5), DIVIDE_CALC_LEVEL_BY_16) \
#     .patch(225 + 2 * (DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT + 5 + 1 + 5), DIVIDE_CALC_LEVEL_BY_16) \
#     .patch(225 + 3 * (DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT + 5 + 1 + 5), DIVIDE_CALC_LEVEL_BY_16) \
#     .patch(225 + 4 * (DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT + 5 + 1 + 5), DIVIDE_CALC_LEVEL_BY_16) \
#     .patch(225 + 6 * (DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT + 5 + 1 + 5), DIVIDE_CALC_LEVEL_BY_16) \
#     .patch(225 + 7 * (DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT + 5 + 1 + 5), DIVIDE_CALC_LEVEL_BY_16) \
#     .patch(225 + 7 * (DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT + 5 + 1 + 5) + \
#       DIVIDE_CALC_LEVEL_BY_16_BYTE_COUNT + 5 + 1, USE_CALCULATED_LEVEL) \


