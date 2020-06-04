# import patchUtil

# constants
BSD_BATTLER_TYPE_IS_ENEMY = 'battlerTypeIsEnemy'

patchStrings = dict([
  (
    BSD_BATTLER_TYPE_IS_ENEMY, findPatchString({
        'name': 'battler type is enemy',
        'srcFnName': 'Legrand.battle.ItemController::ExecBuffOnHittedAndAttack',
        'patchLength': 5,
        'offset': int('21', 16),
    })
  ),
])

patches = [
  (
    '100% loot chance',
    'Legrand.battle.Formula::GetCharacterLootLuck',
    '',
    0,
    '22 00 00 c8 42',  # ldc.r4 100
  ),
  (
    '100% perfect chance',
    'Legrand.battle.TimedHitController::startTimedHit',
    '',
    int('bd', 16),
    '02 ' +  # ld.arg 0
    '22 00 00 80 3f ' +  # ldc.r4 100
    '2b 35 ' +  # br.s 35
    '00 00 00 00',  # nop padding
  ),
  (
    'always in guard stealing buff [1 of 2]',
    'Legrand.battle.ItemController::ExecBuffOnHittedAndAttack',
    '',
    int('f2', 16),
    '17 ' +  # ld.c.i4.1
    '00 00 00 00 00',  # nop padding
  ),
  (
    'always trigger guard stealing [2 of 2]',
    'Legrand.battle.ItemController::ExecBuffOnHittedAndAttack',
    '',
    int('110', 16),
    '19',  # ldc.i4.3
  ),
  (
    'Always draining attacks for PC [1 of 2]',
    'Legrand.battle.ItemController::ExecBuffOnHittedAndAttack',
    '',
    int('a5', 16),
    patchStrings[BSD_BATTLER_TYPE_IS_ENEMY] + ' ' +
    '16 00 00 00 00 ' +  # ldc.r4 0.0
    '40',  # beq
  ),
  (
    'Always draining attacks for PC [2 of 3]',
    'Legrand.battle.ItemController::ExecBuffOnHittedAndAttack',
    '',
    int('c1', 16),
    '00 ' +  # nop
    '22 00 00 c8 42',  # ldc.r4 100.0
  ),
  # (
  #   'Always draining attacks for PC [3 of 3]',
  #   'Legrand.battle.ItemController::ExecBuffOnHittedAndAttack',
  #   '',
  #   int('182', 16),
  #   '1e ' +  # ldc.i4.8
  #   '00 00 00 00 00',  # nop padding
  # ),
]


patchList(patches)
