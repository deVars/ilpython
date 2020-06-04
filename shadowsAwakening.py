from patchUtil import patchList, findPatchString
# TODO: Actor::DropLoot_0+df::+5bytes for '<Actor> is AIController' check
PATCH_STRING_IS_PC = 'PATCH_STRING_IS_PC'
patchStrings = dict([
    (PATCH_STRING_IS_PC,
     findPatchString({
         'name': 'player control',
         'srcFnName': 'ActiveRPGSkill::CanCast',
         'patchLength': 5,
         'offset': int('a', 16),
     })
     ),
])

patches = [
    # (
    #     'No game analytics',
    #     'GameAnalytics::get_enabled',
    #     '',
    #     int('0', 16),
    #     '16 ' +  # ldc.i4.0
    #     '2a ' +  # return
    #     ''
    # ),
    (
        'Generous Drops',
        'Actor::DropLoot_0',
        '',
        int('0', 16),
        '22 00 00 c8 42 ' +  # ldc.r4 100.0
        ''
    ),
    (
        'No mana costs',
        'PlayerController::SpendMana',
        '',
        int('1e', 16),
        '00 ' +  # ldarg.1 to nop
        '00 ' +  # sub to nop
        # this will remove the subtract instruction and
        # leave this.mana = this.mana
        ''
    ),
    (
        'Cooldowns [TriggerCooldown: 0 of 1]',
        'Actor::TriggerCooldown',
        '',
        int('d', 16),
        patchStrings[PATCH_STRING_IS_PC] + ' ' +
        ''
    ),
    (
        'Cooldowns [TriggerCooldown: 1 of 1]',
        'Actor::TriggerCooldown',
        '',
        int('1e', 16),
        '00 ' +  # nop
        '22 00 00 a9 3e ' +  # ldc.r4 0.33  (set cooldown multiplier)
        ''
    ),
    (
        'Cooldowns [TriggerCooldown+CustomCooldown: 0 of 1]',
        'Actor::TriggerCooldown_0',
        '',
        int('d', 16),
        patchStrings[PATCH_STRING_IS_PC] + ' ' +
        ''
    ),
    (
        'Cooldowns [TriggerCooldown+CustomCooldown: 1 of 1]',
        'Actor::TriggerCooldown_0',
        '',
        int('1e', 16),
        '00 ' +  # nop
        '22 00 00 a9 3e ' +  # ldc.r4 0.33  (set cooldown multiplier)
        ''
    ),
    (
        'no inventory caps',
        'InventoryContainer::get_enableInventoryCap',
        '',
        int('0', 16),
        '16 ' +  # ldc.i4.0
        '2a ' +  # return
        '00 00 00 00 ' +  # nop padding
        ''
    ),
    
]

patchList(patches)