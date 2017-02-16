PARENT_TO_CHILD_AREAS = {
    'DIS': ['DIW',],
    'MTD': ['MTW',],
    'CTY': ['CED',],
    'LBO': ['LBW',],
    'CED': ['CPC',],
    'UTA': ['UTW', 'UTE'],
    'NIA': ['NIE',],
    'COI': ['COP',],
}
CHILD_TO_PARENT_AREAS = {
    'DIW': 'DIS',
    'MTW': 'MTD',
    'UTW': 'UTA',
    'UTE': 'UTA',
    'CED': 'CTY',
    'LBW': 'LBO',
    'CPC': 'CED',
    'COP': 'COI',
}

AREAS_WITHOUT_PCCS = [
    "metropolitan",
    "city-of-london",
    "northern-ireland",
]

AREAS_IN_WALES = [
    'south-wales',
    'north-wales',
    'gwent',
    'dyfed-powys',
]


POLICE_AREA_NAME_TO_GSS = {
    'avon-and-somerset': [
        'E10000027', 'E06000022', 'E06000023', 'E06000024', 'E06000025'],

    'bedfordshire': ['E06000055', 'E06000056', 'E06000032'],

    'cambridgeshire': ['E10000003', 'E06000031'],

    'cheshire': ['E06000049', 'E06000050', 'E06000006', 'E06000007'],

    'cleveland': ['E06000001', 'E06000002', 'E06000003', 'E06000004'],

    'cumbria': ['E10000006'],

    'derbyshire': ['E10000007', 'E06000015'],

    'devon-and-cornwall': [
        'E10000008', 'E06000052', 'E06000026', 'E06000027', 'E06000053'],

    'dorset': ['E10000009', 'E06000028', 'E06000029'],

    'durham': ['E06000005', 'E06000047'],

    'dyfed-powys': ['W06000008', 'W06000010', 'W06000009', 'W06000023'],

    'essex': ['E10000012', 'E06000033', 'E06000034'],
    'gloucestershire': ['E10000013'], 'warwickshire': ['E10000031'],
    'greater-manchester': [
        'E08000001', 'E08000002', 'E08000003', 'E08000004', 'E08000005',
        'E08000006', 'E08000007', 'E08000008', 'E08000009', 'E08000010'],
    'gwent': ['W06000021', 'W06000019', 'W06000018', 'W06000022', 'W06000020'],
    'hampshire': ['E10000014', 'E06000046', 'E06000044', 'E06000045'],
    'hertfordshire': ['E10000015'],
    'humberside': ['E06000011', 'E06000012', 'E06000013', 'E06000010'],
    'kent': ['E10000016', 'E06000035'],
    'lancashire': ['E10000017', 'E06000008', 'E06000009'],
    'leicestershire': ['E10000018', 'E06000016', 'E06000017'],
    'lincolnshire': ['E10000019'],
    'merseyside': [
            'E08000011', 'E08000012', 'E08000014', 'E08000015', 'E08000013'],
    'norfolk': ['E10000020'],
    'north-wales': ['W06000001', 'W06000002', 'W06000004',
                    'W06000005', 'W06000003', 'W06000006'],
    'north-yorkshire': ['E10000023', 'E06000014'],
    'northamptonshire': ['E10000021'],
    'northumbria': ['E06000057', 'E08000037', 'E08000021',
                    'E08000022', 'E08000023', 'E08000024'],
    'nottinghamshire': ['E10000024', 'E06000018'],
    'south-wales': ['W06000015', 'W06000011', 'W06000013', 'W06000024',
                    'W06000012', 'W06000016', 'W06000014'],
    'south-yorkshire': ['E08000016', 'E08000017', 'E08000018', 'E08000019'],
    'staffordshire': ['E10000028', 'E06000021'],
    'suffolk': ['E10000029'],
    'surrey': ['E10000030'],
    'sussex': ['E10000011', 'E10000032', 'E06000043'],
    'thames-valley': ['E06000036', 'E06000038', 'E06000039', 'E06000037',
                      'E06000040', 'E06000041', 'E10000002', 'E10000025',
                      'E06000042'],
    'west-mercia': ['E06000051', 'E10000034', 'E06000019', 'E06000020'],
    'west-midlands': ['E08000025', 'E08000026', 'E08000027', 'E08000028',
                      'E08000029', 'E08000030', 'E08000031'],
    'west-yorkshire': [
        'E08000032', 'E08000033', 'E08000034', 'E08000035', 'E08000036'],
    'wiltshire': ['E06000054', 'E06000030'],
}




