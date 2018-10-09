def get_dial_values(parser):
    '''
    Builds a dictionary where the keys are the desired tags to look for in poems and the values are the
    acceptable values for those tags
    :param parser: a configParser object
    :return: dictionary containing poem tags and accepted values
    '''
    build_dict = {}
    for key in parser['dials']:
        build_dict[key] = parser['dials'][key].split()
    return build_dict


def get_namespace(parser):
    return parser['misc']['namespace']

def get_pins(parser):
    return parser['client']['dialPins'].split()

def get_access_key(parser):
    return parser['client']['accessKey']

def get_key_id(parser):
    return parser['client']['keyID']




