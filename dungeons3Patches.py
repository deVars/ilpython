# constants
BSD_STORAGE_TILES = 'roomCollectionStorageTiles'
BSD_STORAGE_TILES_GET_COUNT = 'roomCollectionStorageTilesGetCount'
BSD_CAPACITY_PER_TILE = 'roomCollectionCapacityPerTile'

patchStrings = dict([
  (BSD_STORAGE_TILES, findPatchString({
      'name': 'RoomCollection::StorageTiles ldfld',
      'srcFnName': 'Realmforge.Server.RoomCollection::UpdateProblemSkillState',
      'patchLength': 5,
      'offset': int('60', 16),
    })
  ),
  (BSD_STORAGE_TILES_GET_COUNT, findPatchString({
      'name': 'RoomCollection::StorageTiles:getCount callvirt',
      'srcFnName': 'Realmforge.Server.RoomCollection::UpdateProblemSkillState',
      'patchLength': 5,
      'offset': int('65', 16),
    })
  ),
  (BSD_CAPACITY_PER_TILE, findPatchString({
      'name': 'RoomCollection::get_CapacityPerTile callvirt',
      'srcFnName': 'Realmforge.Server.StorageRoomBase::get_CapacityPerTile',
      'patchLength': 5,
      'offset': int('6', 16),
    })
  ),
])

patches=[
  # sets efficiencyBonusFactor to 5f
  # (
  # 'Gobblers max at 150 flat to avoid map slowdown',
  # 'Realmforge.Server.GuruManager::get_GuruCapacity',
  # '',
  # 0,
  # '22 00 00 80 41 2a ' + #hard set 150.0f as max cap for gobblers
  # '00 00 00 00'
  # ),

  # sets efficiencyBonusFactor to 100f
  (
  'Room Efficiency 200% [2]:Synch',
  'Synch::get_Efficiency',
  '',
  6,
  '00 22 00 00 00 40' # use 2.0f as room efficiency factor (twice prod everything)
  ),

  #using 1kf to check
  # (
  # 'Increase room capacities by 2x',
  # 'Realmforge.Server.RoomCollection::CalculateCapacity',
  # '',
  # int('b', 16),
  # '17 ' + #ldc.i4.1
  # '33 06 ' + #bne.un.s 6
  # '22 00 00 00 00 2a ' + #ldc.r4.0, ret
  # '02 ' + #ldarg.0
  # patchStrings[BSD_STORAGE_TILES] + ' ' +
  # patchStrings[BSD_STORAGE_TILES_GET_COUNT] + ' ' +
  # '6b ' + #conv.r4
  # '02 ' + #ldarg.0
  # patchStrings[BSD_CAPACITY_PER_TILE] + ' ' +
  # '5a ' + #mul
  # '22 00 00 00 40 ' + #ldc.r4 2.0
  # '5a ' + #mul
  # '2a 00' #ret, nop(padding)
  # ),

  # (
  # 'Demons have no needs',
  # 'Realmforge.Server.DemonThink::IncreaseNeeds',
  # '',
  # 0,
  # '2a'
  # ),

  # (
  # 'Horde have no needs',
  # 'Realmforge.Server.HordeHiredThink::IncreaseNeeds',
  # '',
  # 0,
  # '2a'
  # ),

  # # Force undead to be in their home region to auto heal
  # (
  # 'Undead are in their home region',
  # 'Realmforge.Server.UndeadThink::IncreaseNeeds',
  # '',
  # 54,
  # '17 00 00 00 00 00 00 00 00 00 00'
  # ),

  # # Monster common needs handling
  # (
  # 'No bath needs',
  # 'Realmforge.Server.CommonBrainData::get_BathGainPerSecond',
  # '',
  # 0,
  # '16 2a 00 00 00 00'
  # ),
  # (
  # 'No eating needs',
  # 'Realmforge.Server.CommonBrainData::get_HungerGainPerSecond',
  # '',
  # 0,
  # '16 2a 00 00 00 00'
  # ),
  # (
  # 'No sleep needs',
  # 'Realmforge.Server.CommonBrainData::get_SleepingGainPerSecond',
  # '',
  # 0,
  # '16 2a 00 00 00 00'
  # ),
  # (
  # 'No thirst needs',
  # 'Realmforge.Server.CommonBrainData::get_ThirstGainPerSecond',
  # '',
  # 0,
  # '16 2a 00 00 00 00'
  # ),
  # (
  # 'No worship needs',
  # 'Realmforge.Server.CommonBrainData::get_WorshipGainPerSecond',
  # '',
  # 0,
  # '16 2a 00 00 00 00'
  # ),
]

patchList(patches)