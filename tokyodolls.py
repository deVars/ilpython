# aborted due to signature enforcement (has to have google store signage)
patches = [
    (
        'Always best attack',
        'BaseAttack$$IsSweet',
        '',
        0,
        '03 00 a0 e3 ' +  # MOV R0,#3  Best Attack
                          # miss=0,good=1,great=2,best=3
        '1e ff 2f e1 ' +  # BX LR
        '',
    ),
    (
        'Have 10 Attacks per round',
        'PlayerManager$$get_MaxAttackPoint',
        '',
        0,
        '0a 00 a0 e3',  # MOV R0,#10
    ),
    (
        'Skills are always usable',
        'SkillContainer$$get_IsSkillUsable',
        '',
        0,
        '01 00 a0 e3 ' +  # MOV R0,#3  Best Attack
        # miss=0,good=1,great=2,best=3
        '1e ff 2f e1 ' +  # BX LR
        '',
    ),
]

patchList(patches)