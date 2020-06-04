from patchUtil import patchList

patches = [
    (
        'Backpack max weight',
        'InventoryBackpack::.ctor',
        '',
        int('59', 16),
        '22 00 3c 1c 46 ' +  # ldc.r4 9999.0 max weight
        ''
    ),
    (
        'Backpack main pocket grid size',
        'InventoryBackpack::Awake',
        '',
        int('13f', 16),
        '22 00 00 80 42 ' +  # ldc.r4 64.0 grid
        '22 00 00 80 42 ' +  # ldc.r4 64.0 grid
        ''
    ),
    (
        'Backpack front pocket grid size',
        'InventoryBackpack::Awake',
        '',
        int('195', 16),
        '22 00 00 80 42 ' +  # ldc.r4 64.0 grid
        '22 00 00 80 42 ' +  # ldc.r4 64.0 grid
        ''
    ),
    (
        'Nutrition Items Chance Fixed',
        'BalanceSystem20::GetRandomObject',
        '',
        int('35', 16),
        '00 ' +  # nop
        '22 00 00 80 42 ' +  # ldc.r4 64.0 num to compare 2.0 val to fail
        ''
    ),
    (
        'Fallen Items Chance Fixed',
        'FallenObjectsManager::CreateFallenObjects',
        '',
        int('5', 16),
        '22 00 00 00 00 ' +  # ldc.r4 0.0 max chance to fail
        ''
    ),
    (
        'Random loot spawn to fixed loot spawn',
        'RandomLootSpawner::Start',
        '',
        int('16', 16),
        '1f 20 ' +  # ldc.i4.s 32  default to 32 rand spawns every time
        '0a ' +  # stloc.0
        '2b 1a ' +  # br.s 0x1b
        '00 00 ' +  # nop padding
        ''
    ),
    (
        'Stacks no limit',
        'ItemSlotStack::Awake',
        '',
        int('36', 16),
        '20 e7 03 00 00 ' +  # ldc.i4 999
        '00 ' +  # nop padding
        '00 00 00 00 00 ' +  # nop padding
        ''
    ),
]

patchList(patches)
