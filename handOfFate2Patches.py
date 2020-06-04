patches = [
  (
  'Do not hide cards on card chance game 01',
  'ChanceCardTask::HideChoiceCards',
  '',
  38,
  '16'
  ),

  (
  'Do not hide cards on card chance game 02',
  'ChanceCardTask::OnChanceCardClicked',
  '',
  86,
  '17'
  ),

  (
  'No card shuffling 01',
  'CardContainer::Shuffle',
  '',
  0,
  '2a'
  ),

  (
  'Always roll 6 on dii',
  'Die::GetSideValue',
  '',
  0,
  '1c 2a',
  ),

  (
  'Always huge success on pendulum',
  'Pendulum::Evaluate',
  '',
  0,
  '16 2a',
  ),

  (
  'Wheel of Fortune is always easy',
  'Dungeon::GetWheelSpin',
  '',
  9,
  '16',
  ),

  (
  'Wheel of Fortune finish duration is 0s',
  'WheelOfFortune::.ctor',
  '',
  74,
  '22 00 00 00 00',
  ),

  (
  'Wheel of Fortune turn duration is 12s',
  'WheelOfFortune::Update',
  '',
  169,
  '00 22 00 00 40 41',
  ),

  (
  'Companion Ability cooldown is 0f',
  'Controller::CalculateCompanionCooldown',
  '',
  0,
  '16 2a 00 00 00 00',
  ),

  (
  'Finishers are easier @ 50% HP',
  'Controller::CalculateFinisherHealthThreshold',
  '',
  0,
  '22 00 00 48 42 2a 00',
  ),

  (
  'No ability cooldowns',
  'Ability::Use',
  '',
  31,
  '22 00 00 00 3f 00',
  ),

  # change decrease number from 1 to 0
  (
  'Infinite usage for artifacts',
  'Ability::Use',
  '',
  238,
  '16',
  ),




  # (
  # 'free abilities [1]',
  # 'Ability::get_GoldCost',
  # '',
  # 0,
  # '17 2a 00 00 00 00',
  # ),
  # (
  # 'free abilities [2]',
  # 'Ability::get_HealthCost',
  # '',
  # 0,
  # '17 2a 00 00 00 00',
  # ),
  (
  'Easy weapon abilities 01',
  'PlayerCombatAttack::Hit',
  '',
  28,
  '1e'
  ),
  (
  'Easy weapon abilities 02',
  'PlayerCombatAttack::Hit',
  '',
  58,
  '1e'
  ),
]

patchList(patches)