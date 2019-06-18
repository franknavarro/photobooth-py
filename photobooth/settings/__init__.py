import configparser

config = configparser.SafeConfigParser()


config['Apperance'] = {
    'mainColor':'#F2AFB0',
    'secondaryColor':'#AFF2F1'
}

config['Interactions'] = {
    'imageCountdown': 5,
    'stripCountdown': 15
}

