# aborted due to login server checks
patches = [
    (
        'Zero cooltime for skills',
        'SAO.UI.Parts.SkillButton::get_IsCoolTime',
        '',
        0,
        '22 00 00 00 00 ' +  # ldc.r4 0.0f
        '00',  # nop padding
    ),
]

patchList(patches)