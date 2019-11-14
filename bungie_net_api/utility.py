def handleArgs():

    parser = argparse.ArgumentParser(description='Place your application description here.')

#    parser.add_argument('-n','--name', help='display name from www.bungie.net',required=True)
#    parser.add_argument('-c','--character_class', help='Destiny character class [titan|warlock|hunter]',required=True)
#    parser.add_argument('-m','--month', help='Month YYYY-MM',required=False)
#    parser.add_argument('-s','--start', help='Month Start YYYY-MM',required=False)
#    parser.add_argument('-e','--end', help='Month End YYYY-MM',required=False)

    _args = parser.parse_args()

    return _args
