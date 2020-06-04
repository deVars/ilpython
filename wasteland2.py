patches = [
  (
    'PC roll luck additive always true',
    'PCStats::RollLuckAdditive',
    '',
    0,
    '03 2a 00 ' +  #ldarg.1, ret    return the rolls needed
    '00 00 00'  #nop padding
  ),
  (
    'skill checks metered are always success [1 of 2]',
    'SkillMetered::GetRelativeChallenge',
    '',
    int('00',16),
    '16 2a'  #ldc.i4.0, ret  return Challenge.simple
  ),
  (
    'skill checks metered are always success [2 of 2]',
    'SkillMetered::ChallengeObject',
    '',
    int('44',16),
    '00 ' +  #nop  orig: ldc.i4.0
    '1f 64 ' +  #ldc.i4.s 100
    '00 00 00 00 00'  #nop padding orig: Random.Range(int, int)
  ),
  (
    'examine checks are always success [1 of 2]',
    'SkillObject_Examine::ChallengeObject',
    '',
    int('7f',16),
    '1b'  #ldc.i4.5  return ChallengeResult.CriticalSuccess
  ),
  (
    'examine checks metered are always success [2 of 2]',
    'SkillObject_Examine::ChallengeObject',
    '',
    int('92',16),
    '1b'  #ldc.i4.5,  return ChallengeResult.CriticalSuccess
  ),
  (
    'whenever the game wants a roll, we are lucky',
    'PCStats::RollLuck',
    '',
    0,
    '17 2a'  #ldc.i4.1, ret
  ),
  (
    'no overencumbered',
    'PCStats::GetMaxWeight',
    '',
    int('00',16),
    '20 e8 03 00 00 ' +  #ldc.i4 1000
    '6b 2a ' +  #ldc.i4 1000
    '00 00 00 00'  #nop padding
  ),
  (
    '100% chance to hit',
    'PCStats::GetChanceToHit',
    '',
    0,
    '20 ff 00 00 00 2a'  #ldc.i4 255, ret
  ),
  (
    'always critical hit',
    'PCStats::GetChanceToCriticalHit',
    '',
    0,
    '1f 64 2a ' +  #ldc.i4.s 100, ret
    '00 00 00'  #nop padding
  ),
  (
    'mobs have storm trooper base accuracy [-30%]',
    'NPCStats::GetChanceToHit',
    '',
    0,
    '1f e0 ' +  #ldc.i4.s 100, ret
    '00 00 00 00 ' +  #nop padding
    '00 00 00 00 00'  #nop padding
  )
]

patchList(patches)