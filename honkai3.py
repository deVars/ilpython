patches = [
    (
        'Always have charges',
        'AvatarActor$$HasChargesLeft',
        '',
        0,
        '01 00 a0 e3 ' +  # MOV R0, #1
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'No cooldown for skills',
        'AvatarActor$$IsSkillInCD',
        '',
        0,
        '00 00 a0 e3 ' +  # MOV R0, #1
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'No SP needed for skills',
        'AvatarActor$$IsSPEnough',
        '',
        0,
        '01 00 a0 e3 ' +  # MOV R0, #1
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'Remove trackers [1 of 5]',
        'AdTrackManager$$Init',
        '',
        0,
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'Remove trackers [2 of 5]',
        'AdWordsConversionReporter$$Init',
        '',
        0,
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'Remove trackers [3 of 5]',
        'AppsFlyer$$init',
        '',
        0,
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'Remove trackers [4 of 5]',
        'AppsFlyer$$init_cb',
        '',
        0,
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
    (
        'Remove trackers [5 of 5]',
        'FacebookTrackManager$$Start',
        '',
        0,
        '1e ff 2f e1 ' +  # BX LR
        ''
    ),
]

patchList(patches)