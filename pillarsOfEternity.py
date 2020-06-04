# constants
BSD_IS_PARTY_MEMBER = 'isPartyMember'
BSD_OWNER_STATS = 'genericAbilityOwnerStats'
BSD_UNITY_EQUALITY_OP = 'unityEqualityOp'
BSD_UNITY_INEQUALITY_OP = 'unityInequalityOp'

# find isPartyMember patch
patchStrings = dict([
  (BSD_IS_PARTY_MEMBER, findPatchString({
      'name': 'CharacterStats::get_IsPartyMember callvirt',
      'srcFnName': 'CharacterStats::DetectUpdate',
      'patchLength': 5,
      'offset': 1,
    })
  ),
  (BSD_OWNER_STATS, findPatchString({
      'name': 'GenericAbility::m_ownerStats callvirt',
      'srcFnName': 'GenericAbility::ActivateStatusEffects',
      'patchLength': 5,
      'offset': 1,
    })
  ),
  (BSD_UNITY_EQUALITY_OP, findPatchString({
      'name': 'UnityEngine.Object::op_Equality callvirt',
      'srcFnName': 'GenericAbility::get_IsInCooldownRecovery',
      'patchLength': 5,
      'offset': 20,
    })
  ),
  (BSD_UNITY_INEQUALITY_OP, findPatchString({
      'name': 'UnityEngine.Object::op_Inequality callvirt',
      'srcFnName': 'GenericAbility::get_RadiusMultiplier',
      'patchLength': 5,
      'offset': 7,
    })
  ),
])

# Notes
#   Inn bonuses cannot be set as permanent

patches = [
  # (
  #   'fatter POTD difficulty enemies',
  #   'CharacterStats::get_DifficultyHealthStaminaMult',
  #   '',
  #   71,
  #   '22 00 00 20 41' #changes ldc.r4 1.25 to ldc.r4 10.0
  # ),
  # (
  #   'thinner POTD difficulty enemies',
  #   'CharacterStats::get_DifficultyHealthStaminaMult',
  #   '',
  #   71,
  #   '22 cd cc cc 3d' #changes ldc.r4 1.25 to ldc.r4 0.1
  # ),
  # (
  #   'base attribute stat is 20 [1 of 2]',
  #   'UICharacterCreationManager::GetRemainingAttributePoints',
  #   '',
  #   int('12', 16),
  #   '1f 14 ' +  #ldc.i4.s 20   statbase from 8 to 20
  #   '00 00 00 00'  #nop padding
  # ),
  # (
  #   'base attribute stat is 20::increase stat hard max [2 of 2]',
  #   'UICharacterCreationManager::AllowIncStat',
  #   '',
  #   0,
  #   '17 2a'  #ldc.i4.1, ret   always allow to increase stat
  # ),
  (
    'cheaper skill costs [1 of 2]',
    'CharacterStats::CalculateSkillLevelViaPoints',
    '',
    0,
    '02 2a'  #ldarg.0, ret   skill level is always num of points spent
  ),
  (
    'cheaper skill costs [2 of 2]',
    'CharacterStats::GetPointsForSkillLevel',
    '',
    0,
    '02 2a'  #ldarg.0, ret   this is the cumulative points needed to reach a certain skill level
  ),
  (
    'get 5 talents per level up',
    'UICharacterCreationManager::CalculateTalentSelectionStates',
    '',
    int('cf', 16),
    '1b 00 ' +  #ldc.i4.5
    '00 00 00 00 00 ' +  #nop padding
    '00 00 ' +  #nop padding
    '00 ' +  #nop padding
    '00 00 00 00 00'  #nop padding
  ),
  (
    'roll bonuses [Accuracy/ Defense] (for player party) +85',
    'CharacterStats::get_DifficultyStatBonus',
    '',
    0,
    '02 ' + #ld_arg.0
    patchStrings[BSD_IS_PARTY_MEMBER] + ' '
    '2c 06 ' + # br_false.s 06
    '22 00 00 00 00 2a ' + #ldc.r4 0.0, ret
    '22 00 00 aa c2 2a' #ldc.r4 -85.0, ret
  ),
  # (
  #   'always loot everything',
  #   'LootList::Evaluate',
  #   '',
  #   int('21', 16),
  #   '17'   #ldc.i4.1  always set drop flag to true
  # ),
  (
    'free camp',
    'RestZone::WhyCannotCamp',
    '',
    0,
    '16 2a' #ldc.r4 10.0, ret, nop
  ),
  (
    'stealth mastery',
    'Stealth::AddSuspicion_0',
    '',
    100,
    '16' #adds ldc.i4.0 to suspicion
  ),
  (
    'find all detectables',
    'CharacterStats::DetectionRange',
    '',
    0,
    '22 00 00 20 41 2a 00' #ldc.r4 10.0, ret, nop
  ),
  (
    'all party spells are free',
    'GenericSpell::ActivateCooldown',
    '',
    17,
    '02 ' + #ldc_arg.0
    patchStrings[BSD_OWNER_STATS] + ' ' +
    patchStrings[BSD_IS_PARTY_MEMBER] + ' ' +
    '00 00 00 00 00'
  ),
  (
    'all party abilities are free, while enemies are not so [1 of 2]',
    'GenericAbility::get_IsInCooldownAtMax',
    '',
    0,
    '02 ' + #ldc_arg.0
    patchStrings[BSD_OWNER_STATS] + ' ' +
    '14 ' + #ldnull
    patchStrings[BSD_UNITY_EQUALITY_OP] + ' ' +
    '2d 0f ' + #br_true.s 15
    '02 ' + #ldc_arg.0
    patchStrings[BSD_OWNER_STATS] + ' ' +
    patchStrings[BSD_IS_PARTY_MEMBER] + ' ' +
    '2c 02 ' + #br_false.s 04
    '16 2a' #ldc.i4.0, ret
  ),
  (
    'all party abilities are free, while enemies are not so [2 of 2]',
    'GenericAbility::ActivateCooldown',
    '',
    18,
    '16' #change the m_cooldownCounter++ to a m_cooldownCounter+0
  ),

]

patchList(patches)