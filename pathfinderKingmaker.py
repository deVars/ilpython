from enum import Enum
from patchUtil import patchList, findPatchString

calls = Enum('callvirt', (
        'IS_PLAYER_FACTION',
        'IS_PLAYERS_ENEMY',
        'IS_IN_COMBAT',
        'RULEBOOK_INITIATOR',
        'RULEBOOK_TARGET',
        'SKILLCHECK_GETDC',
        'SKILLCHECK_SETDC',
        'TARGET_IS_FLATFOOTED',
        'UNIT_DESCRIPTOR__UNIT',
        'ENTITY_DB_IS_REVEALED',
        'UNIT_DESCRIPTOR',
        'UNIT_DESCRIPTOR_STATE',
        'UNIT_STATUS_ADD_CONDITION',
        'UNIT_STATUS_HAS_CONDITION',
        'UNIT_STATUS_REMOVE_CONDITION',
        'UNIT_DESCRIPTOR_GET_DAMAGE',
        'UNIT_DESCRIPTOR_SET_DAMAGE',
        'D100',
        'GET_MODIFIABLE_ATTRIB_STAT_BONUS',
        'NULLABLE_HAS_VALUE',
        'NULLABLE_GET_VALUE',
        'SAVINGTHROW_SET_STAT_VALUE',
    )
)

patchStrings = dict([
    (
        calls.IS_PLAYER_FACTION,
        findPatchString({
            'name': 'player control',
            'srcFnName': ('Kingmaker.Controllers.AutoPauseController::'
                          'HandleUnitMakeOffensiveAction'),
            'patchLength': 5,
            'offset': int('1', 16),
        })
    ),
    (
        calls.IS_PLAYERS_ENEMY,
        findPatchString({
            'name': 'player enemy',
            'srcFnName': ('Kingmaker.Controllers.AutoPauseController::'
                          'HandleEntityRevealed'),
            'patchLength': 5,
            'offset': int('E', 16),
         })
    ),
    (
        calls.IS_IN_COMBAT,
        findPatchString({
            'name': 'unit is in combat',
            'srcFnName': ('Kingmaker.Controllers.Units.UnitActionController::'
                          'UpdateCooldowns'),
            'patchLength': 5,
            'offset': int('6', 16),
        })
    ),
    (
        calls.RULEBOOK_INITIATOR,
        findPatchString({
            'name': 'initiator for rules',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleAttackRoll::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('3b', 16),
        })
    ),
    (
        calls.RULEBOOK_TARGET,
        findPatchString({
            'name': 'target for rules',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleAttackRoll::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('1d', 16),
        })
    ),
    (
        calls.UNIT_DESCRIPTOR,
        findPatchString({
            'name': 'target for rules',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleAttackRoll::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('22', 16),
        })
    ),
    (
        calls.UNIT_DESCRIPTOR_STATE,
        findPatchString({
            'name': 'target for rules',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleAttackRoll::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('27', 16),
        })
    ),
    (
        calls.TARGET_IS_FLATFOOTED,
        findPatchString({
            'name': 'is the event target flatfooted',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleAttackRoll::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('19b', 16),
        })
    ),
    (
        calls.SKILLCHECK_GETDC,
        findPatchString({
            'name': 'RuleSkillCheck::get_DC',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleSkillCheck::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('a9', 16),
        })
    ),
    (
        calls.SKILLCHECK_SETDC,
        findPatchString({
            'name': 'RuleSkillCheck::set_DC',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleSkillCheck::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('b5', 16),
        })
    ),
    (
        calls.UNIT_STATUS_HAS_CONDITION,
        findPatchString({
            'name': 'UnitStatus::HasCondition',
            'srcFnName': (
                'Kingmaker.Controllers.Units.UnitHelplessController::'
                'UpdateUnit'),
            'patchLength': 5,
            'offset': int('1e', 16),
        })
    ),
    (
        calls.UNIT_STATUS_ADD_CONDITION,
        findPatchString({
            'name': 'UnitStatus::AddCondition',
            'srcFnName': (
                'Kingmaker.Designers.Mechanics.Buffs.BuffStatusCondition::'
                'OnTurnOn'),
            'patchLength': 5,
            'offset': int('17', 16),
        })
    ),
    (
        calls.UNIT_STATUS_REMOVE_CONDITION,
        findPatchString({
            'name': 'UnitStatus::RemoveConditionAll',
            'srcFnName': (
                'Kingmaker.UnitLogic.Buffs.Components.ResurrectionLogic::'
                'OnFactDeactivate'),
            'patchLength': 5,
            'offset': int('37', 16),
        })
    ),
    (
        calls.UNIT_DESCRIPTOR__UNIT,
        findPatchString({
            'name': 'UnitStatus::AddCondition',
            'srcFnName': (
                'Kingmaker.UnitLogic.FactLogic.AddLocalMapMarker::'
                'IsVisible'),
            'patchLength': 5,
            'offset': int('1b', 16),
        })
    ),
    (
        calls.ENTITY_DB_IS_REVEALED,
        findPatchString({
            'name': 'UnitStatus::AddCondition',
            'srcFnName': (
                'Kingmaker.UnitLogic.FactLogic.AddLocalMapMarker::'
                'IsVisible'),
            'patchLength': 5,
            'offset': int('20', 16),
        })
    ),
    (
        calls.UNIT_DESCRIPTOR_GET_DAMAGE,
        findPatchString({
            'name': 'Get damage count from unit descriptor',
            'srcFnName': (
                'Kingmaker.UnitLogic.UnitDescriptor::'
                'get_HPLeft'),
            'patchLength': 5,
            'offset': int('11', 16),
        })
    ),
    (
        calls.UNIT_DESCRIPTOR_SET_DAMAGE,
        findPatchString({
            'name': 'Set damage count from unit descriptor',
            'srcFnName': (
                'Kingmaker.UnitLogic.UnitDescriptor::'
                'Resurrect_0'),
            'patchLength': 5,
            'offset': int('38', 16),
        })
    ),
    (
        calls.D100,
        findPatchString({
            'name': '<static>::D100 <randomInt(1,100)>',
            'srcFnName': (
                'Kingmaker.RuleSystem.Rules.RuleAttackRoll::'
                'TryOvercomeTargetConcealmentAndMissChance'),
            'patchLength': 5,
            'offset': int('59', 16),
        })
    ),
    (
        calls.GET_MODIFIABLE_ATTRIB_STAT_BONUS,
        findPatchString({
            'name': 'callvirt to get modified value for savingthrow',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleSavingThrow::'
                          'OnTrigger'),
            'patchLength': 13,
            'offset': int('9c', 16)
        })
    ),
    (
        calls.NULLABLE_HAS_VALUE,
        findPatchString({
            'name': 'callvirt to get modified value for savingthrow',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleSavingThrow::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('ab', 16)
        })
    ),
    (
        calls.NULLABLE_GET_VALUE,
        findPatchString({
            'name': 'callvirt to get modified value for savingthrow',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleSavingThrow::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('b7', 16)
        })
    ),
    (
        calls.SAVINGTHROW_SET_STAT_VALUE,
        findPatchString({
            'name': 'call to set stat value for savingthrow',
            'srcFnName': ('Kingmaker.RuleSystem.Rules.RuleSavingThrow::'
                          'OnTrigger'),
            'patchLength': 5,
            'offset': int('c2', 16)
        })
    ),
])

patches = [
    (
        'Always light encumbrance (no-arity fn)',
        'CarryingCapacity::GetEncumbrance_0',
        '',
        int('0', 16),
        '16 ' +  # ldc.i4.0
        '2a ' +  # ret
        '00 00 00 00 00 ' +  # nop padding
        '00 00 00 00 00 ' +  # nop padding
        '00 ' +  # nop padding
        ''
    ),
    (
        'Always light encumbrance (carry-weight arity)',
        'CarryingCapacity::GetEncumbrance',
        '',
        int('1c', 16),
        '00 ' +  # nop
        '20 ff ff ff 7f ' +  # 0x7fffffff for light encumbrance weight
        '00 ' +  # nop
        ''
    ),
    (
        'Only need 1 for camp rations',
        'Kingmaker.Controllers.Rest.RestController::CalculateNeededRations',
        '',
        int('0', 16),
        '17 ' +  # ldc.i4.1
        '2a ' +  # ret
        '00 00 00 00 ' +  # nop padding
        '00 00 00 00 00 ' +  # nop padding
        '00 00 00 00 00 ' +  # nop padding
        ''
    ),
    (
        'No time-induced fatigue',
        'Kingmaker.UnitLogic.Parts.UnitPartWeariness::ApplyBuff',
        '',
        int('0', 16),
        '16 ' +  # ldc.i4.0
        '00 00 00 00 00 ' +  # nop padding
        ''
    ),
    (
        'Dialog skill check success',
        'Kingmaker.DialogSystem.Blueprints.BlueprintCheck::GetDC',
        '',
        int('6', 16),
        '1b ' +  # ldarg.5
        '59 ' +  # sub
        '18 ' +  # ldarg.2
        '5b ' +  # div
        '2a ' +  # ret
        '00 00 ' +  # nop padding
        ''
    ),
    (
        'Always show kingdom button',
        'Kingmaker.Kingdom.KingdomState::get_CanSeeKingdomFromGlobalMap',
        '',
        int('0', 16),
        '17 ' +  # ldc.i4.1
        '2a ' +  # ret
        '00 00 00 00 ' +  # nop padding
        ''
    ),
    (
        'Always great success on Kingdom events',
        'Kingmaker.Kingdom.Tasks.KingdomTaskEvent::MakeResolutionRoll',
        '',
        int('2b', 16),
        '1e ' +  # ldc.i4.8  for triumph-type results
        '2b 03 ' +  # br.s 0x4
        '00 00 00 ' +  # nop padding
        ''
    ),
    (
        'Kingdom events resolve fast',
        'Kingmaker.Kingdom.Tasks.KingdomEvent::CalculateResolutionTime',
        '',
        int('81', 16),
        '1f 0a ' +  # ldc.i4.s 10
        '5c ' +  # div.un  integer division from resolution time
        '17 ' +  # ldc.i4.1
        '58 ' +  # add
        '2a ' +  # ret
        '00 00 ' +  # nop padding
        '00 ' +  # nop padding
        ''
    ),
    (
        'Kingdom events resolve fast for ruler too',
        'Kingmaker.Kingdom.Tasks.KingdomEvent::CalculateRulerTime',
        '',
        int('42', 16),
        '06 ' +  # ldloc.0
        '16 ' +  # ldc.i4.0
        'fe 03 ' +  # cgt.un  check if resolution time is greater than 0
        '2d 02 ' +  # beq.s 0x02
        '06 ' +  # ldloc.0
        '2a ' +  # ret
        '06 ' +  # ldloc.0
        '1f 0a ' +  # ldc.i4.s 10
        '5c ' +  # div.un  integer division from resolution time
        '17 ' +  # ldc.i4.1
        '58 ' +  # add
        '2a ' +  # ret
        '00 00 ' +  # nop padding
        ''
    ),
    (
        'Run Speed',
        'Kingmaker.EntitySystem.Entities.UnitEntityData::CalculateSpeedModifier',
        '',
        int('1a', 16),
        '22 00 00 00 40 ' +  # ldc.r4 2.0
        ''
    ),
    (
        'Skill checks are half-difficult',
        'Kingmaker.RuleSystem.Rules.RuleSkillCheck::OnTrigger',
        '',
        int('6d', 16),
        patchStrings[calls.RULEBOOK_INITIATOR] + ' ' +
        patchStrings[calls.IS_PLAYERS_ENEMY] + ' ' +
        '3a 12 00 00 00 ' +  # br.true 12
        '02 ' +  # ldarg.0
        '25 ' +  # dup
        patchStrings[calls.SKILLCHECK_GETDC] + ' ' +
        '1b ' +  # ldarg.5
        '59 ' +  # sub
        '18 ' +  # ldarg.2
        '5b ' +  # div
        patchStrings[calls.SKILLCHECK_SETDC] + ' ' +
        '2b 19 ' +  # br.s 19
        '02 ' +  # ldarg.0
        '25 ' +  # dup
        patchStrings[calls.SKILLCHECK_GETDC] + ' ' +
        '1b ' +  # ldarg.5
        '58 ' +  # add
        '18 ' +  # ldarg.2
        '5a ' +  # mul
        patchStrings[calls.SKILLCHECK_SETDC] + ' ' +
        '2b 07 ' +  # nop padding
        '00 00 ' +  # nop padding
        ''
    ),
    # (
    #     'No ability costs',
    #     'Kingmaker.UnitLogic.UnitAbilityResourceCollection::Spend',
    #     '',
    #     int('7b', 16),
    #     '16 ' +  # ldc.i4.0
    #     ''
    # ),
    # (
    #     'Scrolls do not get used',
    #     'Kingmaker.UnitLogic.Abilities.AbilityData::Spend',
    #     '',
    #     int('0', 16),
    #     '2a ' +  # ldc.i4.0
    #     '2b 03 ' +  # br.s 03
    #     '00 00 00 ' +  # nop padding
    #     ''
    # ),
    (
        'Mass confusion revamp: debuff on enemies',
        ('Kingmaker.Controllers.Units.UnitConfusionController::'
         'TickOnUnit'),
        '',
        int('1', 16),
        patchStrings[calls.IS_PLAYER_FACTION] + ' ' +
        '2c 29 ' +  # brfalse.s 29

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 12 ' +  # ldc.i4.s 0x12  true-seeing
        patchStrings[calls.UNIT_STATUS_HAS_CONDITION] + ' ' +
        '2c 01 ' +  # brfalse.s 1
        '2a ' +  # ret

        # NOTE: every add condition block is a +13
        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 12 ' +  # ldc.i4.s 0x12  true-seeing
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '2a ' +  # ret

        '03 ' +  # ldarg.1
        patchStrings[calls.IS_PLAYERS_ENEMY] + ' ' +
        '2d 01 ' +  # br.true.s 0x01
        '2a ' +  # ret

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 01 ' +  # ldc.i4.s 0x01  blind
        patchStrings[calls.UNIT_STATUS_HAS_CONDITION] + ' ' +
        '2c 02 ' +  # brfalse.s 2
        '2b 5f ' +  # br.s 5f

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 01 ' +  # ldc.i4.s 0x01  blind
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 0f ' +  # ldc.i4.s 0xf  sickened
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 14 ' +  # ldc.i4.s 0x14  shaken
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 16 ' +  # ldc.i4.s 0x16  dazzled
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 1a ' +  # ldc.i4.s 0x1a  spell casting is difficult
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR__UNIT] + ' ' +
        patchStrings[calls.ENTITY_DB_IS_REVEALED] + ' ' +
        '2d 01 ' +  # br.true.s 0x01
        '2a ' +  # ret

        patchStrings[calls.D100] + ' ' +
        '17 ' +  # ldc.i4.1  1% to trigger random conditions
        '42 ee 00 00 00 ' +  # bgt.un ee  skip random conditions if greater

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        '25 ' +  # dup
        patchStrings[calls.UNIT_DESCRIPTOR_GET_DAMAGE] + ' ' +
        '18 ' +  # ldc.i4.2
        '58 ' +  # add
        patchStrings[calls.UNIT_DESCRIPTOR_SET_DAMAGE] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 17 ' +  # ldc.i4.s 0x17  stunned
        patchStrings[calls.UNIT_STATUS_HAS_CONDITION] + ' ' +
        '0b ' +  # stloc.1

        patchStrings[calls.D100] + ' ' +
        '1F 20 ' +  # ldc.i4.s 32 percent chance of stunned
        '35 18 ' +  # bgt.un.s 18  skip stunned if greater
        '07 ' +  # ldloc.1
        '2d 13 ' +  # brtrue.s 0x13

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 17 ' +  # ldc.i4.s 0x17  stunned
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '2b 15 ' +  # br.s 15 skip release stunned state

        '07 ' +  # ldloc.1  we got a higher number than our stunned chance
        '2c 12 ' +  # brfalse.s 0x12

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 17 ' +  # ldc.i4.s 0x17  stunned
        patchStrings[calls.UNIT_STATUS_REMOVE_CONDITION] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 0d ' +  # ldc.i4.s 0x0d  frightened
        patchStrings[calls.UNIT_STATUS_HAS_CONDITION] + ' ' +
        '0b ' +  # stloc.1

        patchStrings[calls.D100] + ' ' +
        '1F 10 ' +  # ldc.i4.s 16 percent chance of frightened
        '35 18 ' +  # bgt.un.s 18  skip frightened if greater
        '07 ' +  # ldloc.1
        '2d 13 ' +  # brtrue.s 0x13

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 0d ' +  # ldc.i4.s 0x0d  frightened
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '2b 15 ' +  # br.s 15 skip release frightened state

        '07 ' +  # ldloc.1  we got a higher number than our stunned chance
        '2c 12 ' +  # brfalse.s 0x12

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 0d ' +  # ldc.i4.s 0x0d  frightened
        patchStrings[calls.UNIT_STATUS_REMOVE_CONDITION] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 1f ' +  # ldc.i4.s 0x1f  unconscious
        patchStrings[calls.UNIT_STATUS_HAS_CONDITION] + ' ' +
        '0b ' +  # stloc.1

        patchStrings[calls.D100] + ' ' +
        '1F 08 ' +  # ldc.i4.s 08 percent chance of unconscious
        '35 18 ' +  # bgt.un.s 18  skip unconscious if greater
        '07 ' +  # ldloc.1
        '2d 13 ' +  # brtrue.s 0x13

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 1f ' +  # ldc.i4.s 0x1f  unconscious
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '2b 15 ' +  # br.s 15 skip release unconscious state

        '07 ' +  # ldloc.1  we got a higher number than our unconscious chance
        '2c 12 ' +  # brfalse.s 0x12

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 1f ' +  # ldc.i4.s 0x1f  unconscious
        patchStrings[calls.UNIT_STATUS_REMOVE_CONDITION] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 0B ' +  # ldc.i4.s 0xb  entangled
        patchStrings[calls.UNIT_STATUS_HAS_CONDITION] + ' ' +
        '2c 01 ' +  # brfalse.s 1
        '2a ' +  # ret
        #
        # '03 ' +  # ld.arg 1
        # patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        # patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        # '1F 06 ' +  # ldc.i4.s 0x06  staggered
        # '14 ' +  # ldnull
        # patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +
        #
        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 0B ' +  # ldc.i4.s 0xb  entangled
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '03 ' +  # ld.arg 1
        patchStrings[calls.UNIT_DESCRIPTOR] + ' ' +
        patchStrings[calls.UNIT_DESCRIPTOR_STATE] + ' ' +
        '1F 06 ' +  # ldc.i4.s 0x06  staggered
        # '1F 2a ' +  # ldc.i4.s 0x2a
        # looks like exhausted is not implemented on enemies
        '14 ' +  # ldnull
        patchStrings[calls.UNIT_STATUS_ADD_CONDITION] + ' ' +

        '2a ' +  # ret
        '00 00 00 00 00 ' +  # nop padding
        '00 00 00 00 00 ' +  # nop padding
        '00 00 ' +  # nop padding
        # '00 00 00 00 00 ' +  # nop padding
        ''
    ),
    (
        'AC, Perception and Attack Bonus debuffs for Insane',
        ('Kingmaker.Designers.Mechanics.Buffs.'
            'DifficultyStatAdvancement::OnTurnOn'),
        '',
        int('19', 16),
        '16 ' +  # ldc.i4.0
        '0c ' +  # stloc.2
        '16 ' +  # ldc.i4.0
        '0d ' +  # stloc.3
        '16 ' +  # ldc.i4.0
        '13 04 ' +  # stloc.4
        '16 ' +  # ldc.i4.0
        '13 05 ' +  # stloc.5
        '2b 48 ' +  # br.s 48
        '00 00 ' +  # nop padding
        ''
    ),
    (
        'Enemies are flat-footed',
        ('Kingmaker.RuleSystem.Rules.RuleCheckTargetFlatFooted::'
         'OnTrigger'),
        '',
        int('0', 16),
        '02 ' +  # ldarg.0
        '25 ' +  # dup
        patchStrings[calls.RULEBOOK_TARGET] + ' ' +
        patchStrings[calls.IS_PLAYERS_ENEMY] + ' ' +
        '17 ' +  # ldarg.0f
        'fe 01 ' +  # ceq
        '38 0d 01 00 00 ' +  # br -> <set IsFlatFooted>
        '00 00 00 ' +  # nop padding
        ''
    ),
    (
        'Enemies only have single attacks but pc has min 4 [0 of 2]',
        ('Kingmaker.RuleSystem.Rules.RuleCalculateAttacksCount::'
         'OnTrigger'),
        '',
        int('15', 16),
        '19 ' +  # ldc.i4.3
        '5c ' +  # div.un => BAB div 3 - 1 == num attacks bonus
        '17 ' +  # ldc.14.1
        '58 ' +  # add
        '0b ' +  # stloc.1
        '02 ' +  # ld.arg 0
        patchStrings[calls.RULEBOOK_INITIATOR] + ' ' +
        patchStrings[calls.IS_PLAYERS_ENEMY] + ' ' +
        '2c 06 ' +  # brfalse.s 0x06
        '16 ' +  # ldc.i4.0 default non-penalized attack for enemy
        '0a ' +  # stloc.0
        '17 ' +  # ldc.i4.1 default attack bonus for enemy
        '0b ' +  # stloc.1
        '2b 08 ' +  # br.s 0x09
        '07 ' +  # ldloc.1
        '0a ' +  # stloc.0
        '2b 04 ' +  # br.s 0x08
        '00 00 00 00 00 ' +  # nop padding
        ''
    ),
    (
        'Enemies only have single attacks but pc has min 4 [1 of 2]',
        ('Kingmaker.RuleSystem.Rules.RuleCalculateAttacksCount::'
         'OnTrigger'),
        '',
        int('153', 16),
        '06 ' +  # ldloc.1  to use val earlier for primary attack
        ''
    ),
    (
        'Enemies only have single attacks but pc has min 4 [2 of 2]',
        ('Kingmaker.RuleSystem.Rules.RuleCalculateAttacksCount::'
         'OnTrigger'),
        '',
        int('1f1', 16),
        '07 ' +  # ldloc.1  to use val earlier for secondary attack
        ''
    ),
    (
        'Saving throws advantage',
        ('Kingmaker.RuleSystem.Rules.RuleSavingThrow::'
         'get_IsPassed'),
        '',
        int('12', 16),
        '1f 0a ' +  # ldc.i4 10
        '02 ' +  # ldarg.0
        patchStrings[calls.RULEBOOK_INITIATOR] + ' ' +
        patchStrings[calls.IS_PLAYERS_ENEMY] + ' ' +
        '2c 02 ' +  # brfalse.s 0x02
        '15 ' +  # ldc.i4.m1
        '5a ' +  # mul
        '00 00 ' +  # br.s 05
        '00 00 00 00 ' +  # nop padding
        ''
    ),
    (
        'Random loots are not random',
        ('Kingmaker.Blueprints.Loot.LootRandomItem::'
         'AddItemsTo'),
        '',
        int('2f', 16),
        '06 ' +  # ldloc.0, which is the total weight so we always
                 # get the last item
        ''
    ),
    (
        'Variable loot packs have more items',
        ('Kingmaker.Blueprints.Loot.LootItemsPackVariable::'
         'AddItemsTo'),
        '',
        int('c', 16),
        '1e ' +  # ldc.i4.1
        ''
    ),
    (
        'Lots of trash loot',
        ('Kingmaker.Blueprints.Loot.RandomTrashLootConfig::'
         'FillLootComponent'),
        '',
        int('42', 16),
        '17 ' +  # ldc.i4.1
        '2b 03 ' +  # br.s 03
        '00 00 00 ' +  # nop padding
        ''
    ),
    (
        'After first game -- 125% base chance encounter on map',
        ('Kingmaker.Blueprints.Root.RandomEncountersRoot::'
         '.ctor'),
        '',
        int('08', 16),
        '22 00 00 a0 3f ' +  # ldc.r4 2.0  new encounter within 2 miles
        ''
    ),
    (
        'After first game -- 125% base chance encounter on camp',
        ('Kingmaker.Blueprints.Root.RandomEncountersRoot::'
         '.ctor'),
        '',
        int('13', 16),
        '22 00 00 a0 3f ' +  # ldc.r4 2.0  new encounter within 2 miles
        ''
    ),
    (
        'After first game -- 125% base chance encounter on camp 2nd time',
        ('Kingmaker.Blueprints.Root.RandomEncountersRoot::'
         '.ctor'),
        '',
        int('1e', 16),
        '22 00 00 a0 3f ' +  # ldc.r4 2.0  new encounter within 2 miles
        ''
    ),
    (
        'After first game -- do super yakuza common encounters',
        ('Kingmaker.Blueprints.Root.RandomEncountersRoot::'
         '.ctor'),
        '',
        int('4a', 16),
        '22 00 00 00 3f ' +  # ldc.r4 2.0  new encounter within 0.5 miles
        ''
    ),
    (
        'After first game -- no safe miles after encounter',
        ('Kingmaker.Blueprints.Root.RandomEncountersRoot::'
         '.ctor'),
        '',
        int('55', 16),
        '22 00 00 00 00 ' +  # ldc.r4 0.0  roll immediately after 0.5 miles
        ''
    ),
]

patchList(patches)
