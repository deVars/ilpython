from patchUtil import *

# constants
BSD_CHECK_PLAYER = 'checkPlayer'
BSD_ACTOR_GET_ATTRI = 'actorGetAttri'

patchStrings = dict([
    (BSD_CHECK_PLAYER,
     findPatchString({
         'name': 'player control',
         'srcFnName': 'BattleLogicNomal::createCommandBattle',
         'patchLength': 5,
         'offset': 181,
     })
     ),
    (BSD_ACTOR_GET_ATTRI,
     findPatchString({
         'name': 'actor.getAttri',
         'srcFnName': 'BattleLogic::getCommandData',
         'patchLength': 5,
         'offset': 63,
     })
     ),
])

patches = [
    (
        '64 crit stars',
        'BattleData::getCriticalPoint',
        '',
        0,
        '1f 40 2a 00 00 00'
    ),

    # 3fc00000 -> 00 00 c0 3f is 1.5x
    # 3f800000 -> 00 00 c0 3f is 1.0x
    # 3f000000 -> 00 00 c0 3f is 0.5x
    # 19/11/2017 trying to set both as 0.5x, sucks for farming
    # first number is player's rate
    (
        'attribute damage [de-]buff',
        'AttriRelationMaster::getRate',
        '',
        0,
        '02 2c 06 22 00 00 c0 3f 2a 22 00 00 00 3f 2a'
    ),

    # change actor.getAttri() to actor.isPlayer()
    (
        'attribute damage check player',
        'BattleLogic::getDamagelist_0',
        '03 ' + patchStrings[BSD_ACTOR_GET_ATTRI],
        1,
        patchStrings[BSD_CHECK_PLAYER]
    ),

    (
        'non friends can gain np gauge',
        'BattleServantData::isAddNpGauge',
        '',
        0,
        '02 ' +
        patchStrings[BSD_CHECK_PLAYER] +
        ' 2a'
    ),

    (
        'non friends can gain use np',
        'Follower::isUseTreasure',
        '',
        0,
        '17 2a'
    ),

    # goal is if max effect duration is 3 or more,
    # it will NOT get decreased
    # this sets turn limit to 3,
    (
        'no turn limited buffs: [0] only turn-end 1-turn buffs',
        'BuffData::checkProgressTurn',
        '',
        int('c', 16),
        '19'
    ),

    # this switches clt to cgt.un, making the condition 3 > buffTurns
    (
        'no turn limited buffs: [1] only turn-end 1-turn buffs',
        'BuffData::checkProgressTurn',
        '',
        int('13', 16),
        'FE 03'
    ),

    # this removes checks that prevent certain buffs from stacking
    (
        'no buff group checks',
        'BuffEntity::isCheckGroup',
        '',
        0,
        '16 ' +  # ldc.i4.0
        '2a ' +  # ret
        '00 00 00 00'
    ),

    # ('no skill cooldown for servants',
    # 'BattleServantData::useSkill',
    # '',
    # 0,
    # '03 1f 0a 7d 7d 1f 00 04 03 16 7d 7e 1f 00 04 2a'),
    # ('no skill cooldown for masters',
    # 'BattleData::useMasterSkill',
    # '',
    # 0,
    # '03 1f 0a 7d 7d 1f 00 04 03 16 7d 7e 1f 00 04 2a'),

    (
        'animation speed tweak:: base frame rate is now 1.375',
        'BattleLogic::setTimeAcceleration',
        '',
        128,
        '22 00 00 b0 3f'
    ),
]

patchList(patches)
