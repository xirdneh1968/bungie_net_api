""" Bungie.net API module """

import urllib.request
import urllib.parse
import urllib.error
import json
import configparser
import os.path
import sys

# enum DestinyClass { Titan = 0, Hunter = 1, Warlock = 2, Unknown = 3 }

CONFIG_FILE_NAME = '.bungie_net_api.rc'

# API_KEY = <secret API key>

# put a BungieNet API-KEY obtained from https://www.bungie.net/en-US/User/API
# into a ini style file at $HOME/CONFIG_FILE_NAME.

CONFIG_FILE = (os.path.join(os.path.expanduser("~"), CONFIG_FILE_NAME))

config = configparser.ConfigParser()
config.read(CONFIG_FILE)
API_KEY = config.get('api', 'API-KEY')

DEBUG = int(config.get('default', 'debug'))

# Bungie-net github:
#   https://github.com/Bungie-net/api
#
# Destiny 2 API:
#   https://www.bungie.net/platform/destiny2/help/
#
# Destiny 1 API:
#  https://www.bungie.net/d1/platform/Destiny/help/
# Lowlines documentation of D1 API:
#  http://destinydevs.github.io/BungieNetPlatform/docs/Getting-Started

# getProfile https://www.bungie.net/platform/destinys/help/

def getProfile(destinyMembershipId=None, membershipType=None
  , components=None, token=None):
    """getProfile()"""

    if DEBUG:
        print(("DEBUG: getProfile(/Destiny2/" + membershipType + "/Profile/"
                + destinyMembershipId + "/" + "?components=" + components))

    if token:
        acctSummary = callOauthBungieAPI('/Destiny2/' + membershipType 
          + '/Profile/' + destinyMembershipId + '/' 
          + '?components=' + components, token = token)
    else:
        acctSummary = callBungieAPI('/Destiny2/' + membershipType + '/Profile/'
          + destinyMembershipId + '/' + '?components=' + components)

    return acctSummary

def getClanLeaderboards(clanId=None, modes=None, maxTop=None, statId=None):
    """getClanLeanderboards()"""

    if DEBUG:
        print(("DEBUG: getClanLeanderboards(/Destiny2/Stats/Leaderboards/Clans/" + clanId + "/" + "?modes=" + modes))

    if maxTop:
        top = maxTop
    else:
        top = 5

    if statId:

        leaderboards = callBungieAPI('/Destiny2/Stats/Leaderboards/Clans/'
              + str(clanId) + '?modes=' + modes + '&maxtop=' + str(top)
              + '&statId=' + statId)

    else:

        leaderboards = callBungieAPI('/Destiny2/Stats/Leaderboards/Clans/'
              + str(clanId) + '?modes=' + modes + '&maxtop=' + str(top))


    return leaderboards


def getMembershipsById(membership_id=None, membership_type=None):
    """getMembershipsById()"""

    if DEBUG:
        print(("DEBUG: getMembershipsById(/User/GetMembershipsById/"
                + membership_id + "/" + membership_type + "/"))

    accounts = callBungieAPI('/User/GetMembershipsById/' 
                 + membership_id + '/' + membership_type + '/')

    return accounts

def getMembershipDataById(membershipId=None, membershipType=None):
    """getMembershipDataById()"""

    if DEBUG:
        print(("DEBUG: getMembershipDataById(/User/GetMembershipsById/"
                + membershipId + "/" + membershipType + "/"))

    accounts = callBungieAPI('/User/GetMembershipsById/' 
                 + membershipId + '/' + membershipType + '/')

    return accounts

# get_account_summary https://www.bungie.net/platform/destiny/help/

def getActivityHistory(destiny_membership_id=None, membership_type=None
                       , character_id=None, mode=None, count=None
                       , page=None):
    """getActivityHistory()"""

    if mode is None:
        optional_arg = '?mode=None'
    else:
        optional_arg = '?mode=' + mode

    if count is not None:
        optional_arg = optional_arg + '&count=' + count
    if page is not None:
        optional_arg = optional_arg + '&page=' + page

    if DEBUG:
        print ("DEBUG: getActivityHistory()")

    activity_history_stats = callBungieAPI('/Destiny2/' + membership_type 
                              + '/Account/' + destiny_membership_id 
                              + '/Character/' + character_id
                              + '/Stats/Activities/'
                              + optional_arg)

    return activity_history_stats

def get_account_summary(destiny_membership_id=None, membership_type=None
                        , definitions=None):
    """get_account_summary()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/" + membership_type + "/Account/"
               + destiny_membership_id + "/Summary/" + optional_arg +")"))

    acct_summary = call_bungie_api('/' + membership_type + '/Account/'
                                   + destiny_membership_id + '/Summary/'
                                   + optional_arg)

    return acct_summary

# get_activity_history_stats https://www.bungie.net/platform/destiny/help/

def get_activity_history_stats(destiny_membership_id=None
                               , membership_type=None, character_id=None
                               , definitions=None, page=None
                               , mode=None, count=None):
    """get_activity_history_stats()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if mode is None:
        optional_arg = optional_arg + '&mode=None'
    else:
        optional_arg = optional_arg + '&mode=' + mode

    if count is not None:
        optional_arg = optional_arg + '&count=' + count
    if page is not None:
        optional_arg = optional_arg + '&page=' + page

    if DEBUG:
        print(("DEBUG: call_bungie_api(/Stats/ActivityHistory/"
               + membership_type + "/" + destiny_membership_id + "/"
               + character_id + "/" + optional_arg +")"))

    activity_history_stats = call_bungie_api('/Stats/ActivityHistory/'
                                             + membership_type + '/'
                                             + destiny_membership_id + '/'
                                             + character_id +'/'
                                             + optional_arg)

    return activity_history_stats

# get_account_advisors https://www.bungie.net/platform/destiny/help/

def get_account_advisors(destiny_membership_id=None, membership_type=None
                         , definitions=None):
    """get_account_advisors()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/" + membership_type + "/Account/"
               + destiny_membership_id + "/Advisors/" + optional_arg +")"))

    acct_advisors = call_bungie_api('/' + membership_type + '/Account/'
                                    + destiny_membership_id + '/Advisors/'
                                    + optional_arg)

    return acct_advisors

# get_account_advisors_v2 https://www.bungie.net/platform/destiny/help/

def get_account_advisors_v2(destiny_membership_id=None, membership_type=None
                            , character_id=None, definitions=None):
    """get_account_adviors()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/" + membership_type + "/Account/"
               + destiny_membership_id + "/Character/" + character_id
               + "/Advisors/V2/" + optional_arg +")"))

    acct_advisors_v2 = call_bungie_api('/' + membership_type + '/Account/'
                                       + destiny_membership_id + '/Character/'
                                       + character_id + '/Advisors/V2/'
                                       + optional_arg)

    return acct_advisors_v2

# get_account_items https://www.bungie.net/platform/destiny/help/

def get_account_items(destiny_membership_id=None, membership_type=None
                      , definitions=None):
    """get_account_items()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/" + membership_type + "/Account/"
               + destiny_membership_id + "/Items/" + optional_arg +")"))

    acct_items = call_bungie_api('/' + membership_type + '/Account/'
                                 + destiny_membership_id + '/items/'
                                 + optional_arg)

    return acct_items

# get_character_activities https://www.bungie.net/platform/destiny/help/

def get_character_activities(destiny_membership_id=None, membership_type=None
                             , character_id=None, definitions=None):
    """get_character_activities()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/" + membership_type + "/Account/"
               + destiny_membership_id + "/Character/"
               + character_id + "/Activities/" + optional_arg +")"))

    char_activities = call_bungie_api('/' + membership_type + '/Account/'
                                      + destiny_membership_id + '/Character/'
                                      + character_id + '/Activities/'
                                      + optional_arg)

    return char_activities

# get_character_inventory https://www.bungie.net/platform/destiny/help/
# DEPREATED use get_character_inventorySummary instead!

def get_character_inventory(destiny_membership_id=None, membership_type=None
                            , character_id=None, definitions=None):
    """get_character_inventory()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/" + membership_type + "/Account/"
               + destiny_membership_id + "/Character/"
               + character_id + "/Inventory/" + optional_arg +")"))

    char_inventory = call_bungie_api('/' + membership_type + '/Account/'
                                     + destiny_membership_id + '/Character/'
                                     + character_id + '/Inventory/'
                                     + optional_arg)

    return char_inventory

# get_character_inventory_summary https://www.bungie.net/platform/destiny/help/

def get_character_inventory_summary(destiny_membership_id=None
                                    , membership_type=None
                                    , character_id=None, definitions=None):
    """get_character_inventory_summary()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/" + membership_type + "/Account/"
               + destiny_membership_id + "/Character/"
               + character_id + "/Inventory/Summary/"
               + optional_arg +")"))

    char_inventory_summary = call_bungie_api('/' + membership_type
                                             + '/Account/'
                                             + destiny_membership_id
                                             + '/Character/'
                                             + character_id
                                             + '/Inventory/Summary/'
                                             + optional_arg)

    return char_inventory_summary

# get_character_progression https://www.bungie.net/platform/destiny/help/

def get_character_progression(destiny_membership_id=None, membership_type=None
                              , character_id=None, definitions=None):
    """get_character_progression()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/" + membership_type + "/Account/"
               + destiny_membership_id + "/Character/"
               + character_id + "/Progression/"
               + optional_arg +")"))

    char_progression = call_bungie_api('/' + membership_type + '/Account/'
                                       + destiny_membership_id + '/Character/'
                                       + character_id + '/Progression/'
                                       + optional_arg)

    return char_progression

# get_character_summary https://www.bungie.net/platform/destiny/help/

def get_character_summary(destiny_membership_id=None, membership_type=None
                          , character_id=None, definitions=None):
    """get_character_summary()"""


    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/" + membership_type + "/Account/"
               + destiny_membership_id + "/Character/"
               + character_id + "/" + optional_arg +")"))

    char_summary = call_bungie_api('/' + membership_type + '/Account/'
                                   + destiny_membership_id + '/Character/'
                                   + character_id + '/' + optional_arg)

    return char_summary

# get_character_aggregate_stats at
# https://www.bungie.net/platform/destiny/help/

def get_character_aggregate_stats(destiny_membership_id=None
                                  , membership_type=None
                                  , character_id=None
                                  , definitions=None):
    """get_character_aggregate_stats()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/Stats/AggregateActivityStats/"
               + membership_type + "/" + destiny_membership_id + "/"
               + character_id + "/" + optional_arg +")"))

    char_agg_activity_stats = call_bungie_api('/Stats/AggregateActivityStats/'
                                              + membership_type + '/'
                                              + destiny_membership_id + '/'
                                              + character_id + '/'
                                              + optional_arg)

    return char_agg_activity_stats

# get_character_stats https://www.bungie.net/platform/destiny/help/

def get_character_stats(destiny_membership_id=None, membership_type=None
                        , character_id=None, modes=None
                        , period_type=None, groups=None, monthstart=None
                        , monthend=None, daystart=None, dayend=None):
    """get_character_stats()"""

    optional_arg = ''

    if modes is None:
        optional_arg = '?modes=None'
    else:
        optional_arg = optional_arg + '?modes=' + modes

    if period_type is not None:
        optional_arg = optional_arg + '&periodType=' + period_type

    if groups is not None:
        optional_arg = optional_arg + '&groups=' + groups

    if monthstart is not None:
        optional_arg = optional_arg + '&monthstart=' + monthstart

    if monthend is not None:
        optional_arg = optional_arg + '&monthend=' + monthend

    if daystart is not None:
        optional_arg = optional_arg + '&daystart=' + daystart

    if dayend is not None:
        optional_arg = optional_arg + '&dayend=' + dayend

    if DEBUG:
        print(("DEBUG: call_bungie_api(/Stats/" + membership_type + "/"
               + destiny_membership_id + "/" + character_id + "/"
               + optional_arg + ")"))

    char_stats = call_bungie_api('/Stats/' + membership_type + '/'
                                 + destiny_membership_id + '/'
                                 + character_id + '/' + optional_arg)

    return char_stats

# get_account_stats https://www.bungie.net/platform/destiny/help/

def get_account_stats(destiny_membership_id=None, membership_type=None
                      , groups=None):
    """get_account_stats()"""

    if groups is None:
        optional_arg = ''
    else:
        optional_arg = '?groups=' + groups

    if DEBUG:
        print(("DEBUG: call_bungie_api(/Stats/Account/" + membership_type + "/"
               + destiny_membership_id + "/" + optional_arg + ")"))

    acct_stats = call_bungie_api('/Stats/Account/' + membership_type + '/'
                                 + destiny_membership_id + '/'
                                 + optional_arg)

    return acct_stats

# get_activity_stats https://www.bungie.net/platform/destiny/help/

def get_activity_stats(activity_id=None, definitions=None):
    """get_activity_stats()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/Stats/PostGameCarnageReport/"
               + activity_id + "/" + optional_arg + ")"))

    activity_pgc_report_stats = call_bungie_api('/Stats/PostGameCarnageReport/'
                                                + activity_id + '/'
                                                + optional_arg)

    return activity_pgc_report_stats

# get_char_uniq_weapon_stats at
# https://www.bungie.net/platform/destiny/help/

def get_char_uniq_weapon_stats(membership_type=None
                               , destiny_membership_id=None
                               , character_id=None
                               , definitions=None):
    """get_char_uniq_weapon_stats()"""

    if definitions is None:
        optional_arg = ''
    else:
        optional_arg = '?definitions=true'

    if DEBUG:
        print(("DEBUG: call_bungie_api(/Stats/UniqueWeapons/"
               + membership_type + "/" + destiny_membership_id + "/"
               + character_id + "/" + optional_arg + ")"))

    char_uniq_weapon_stats = call_bungie_api('/Stats/UniqueWeapons/'
                                             + membership_type + '/'
                                             + destiny_membership_id + '/'
                                             + character_id + '/'
                                             + optional_arg)

    return char_uniq_weapon_stats

# get_explorer_items at
# https://www.bungie.net/platform/destiny/help/

def get_explorer_items(count=10, page=0):
    """get_explorer_items()"""

    if DEBUG:
        print ("DEBUG: call_bungie_api(/Explorer/Items/")

    explorer_items = call_bungie_api('/Explorer/Items/')

    return explorer_items

# get_explorer_talent_node_steps at
# https://www.bungie.net/platform/destiny/help/

def get_explorer_talent_node_steps(count=10, page=0):
    """get_explorer_talent_node_steps()"""

    if DEBUG:
        print ("DEBUG: call_bungie_api(/Explorer/TalentNodeSteps/")

    explorer_talent_node_steps = call_bungie_api('/Explorer/TalentNodeSteps/')

    return explorer_talent_node_steps

# get_manifest at
# https://www.bungie.net/platform/destiny/help/

def get_manifest():
    """get_explorer_talent_node_steps()"""

    if DEBUG:
        print ("DEBUG: call_bungie_api(/Manifest/")

    manifest = call_bungie_api('/Manifest/')

    return manifest

# get_manifest_item at
# https://www.bungie.net/platform/destiny/help/

def get_manifest_item(definition_type=None, definition_id=None):
    """get_explorer_talent_node_steps()"""

    if DEBUG:
        print(("DEBUG: call_bungie_api(/Manifest/"
               + definition_type + "/"
               + definition_id + "/"))

    item = call_bungie_api('/Manifest/'
                           + definition_type + '/'
                           + definition_id + '/')

    return item

# get_account_grimoire at
# https://www.bungie.net/platform/destiny/help/

def get_account_grimoire(destiny_membership_id=None, membership_type=None):
    """get_account_grimoire()"""

    if DEBUG:
        print(("DEBUG: call_bungie_api(/Vanguard/Grimoire/"
               + membership_type + "/"
               + destiny_membership_id + "/"
               + '?definitions=true&flavour=true'))

    grimoire = call_bungie_api('/Vanguard/Grimoire/'
                           + membership_type + '/'
                           + destiny_membership_id + '/'
                           + '?definitions=true&flavour=true')

    return grimoire

# searchDestinyPlayer at
# https://www.bungie.net/platform/destiny2/help/

def searchDestinyPlayer(display_name=None,membership_type=None):
    """searchDestinyPlayer(membership_type=None,display_name=None)"""

    if DEBUG:
        print(("DEBUG: callBungieAPI(/Destiny2/SearchDestinyPlayer/"
                + membership_type + "/"
                + display_name + "/"))

    membership_info = callBungieAPI('/Destiny2/SearchDestinyPlayer/'
                                    + membership_type + '/'
                                    + display_name + '/')


    return membership_info

def callBungieAPI (method):
    """callBungieAPI()"""

    # takes a BungieNet API method as documented at
    # https://www.bungie.net/platform/destiny2/help/

##    api_base = 'https://www.bungie.net/Platform/Destiny2'
    api_base = 'https://www.bungie.net/Platform'
    call_url = api_base + method

    request = urllib.request.Request(call_url, headers={'X-API-Key':API_KEY})

    result = urllib.request.urlopen(request).read().decode('utf-8')

    parsed_result = json.loads(result)

    return parsed_result

def callOauthBungieAPI (method=None, token=None):
    """callOauthBungieAPI()"""

    # takes a BungieNet API method as documented at
    # https://www.bungie.net/platform/destiny2/help/

##    api_base = 'https://www.bungie.net/Platform/Destiny2'
    api_base = 'https://www.bungie.net/Platform'

    print(("DEBUG: ", method, "\n"))
    call_url = api_base + method

    headers = {
  'X-API-Key': API_KEY,
  'Authorization': 'Bearer ' + token
}

    encoded_headers = urllib.parse.urlencode(headers)
    request = urllib.request.Request(call_url, headers={'X-API-Key': API_KEY, 'Authorization': 'Bearer ' + token})

#    print "DEBUG: before urlopen"

    result = urllib.request.urlopen(request).read().decode('utf-8')
#    result = urllib2.urlopen(request)
#    print "DEBUG: after urlopen"

    parsed_result = json.loads(result)

    return parsed_result

def call_bungie_api(method):
    """call_bungie_api()"""

    # takes a BungieNet API method as documented at
    # https://www.bungie.net/platform/destiny/help/

    api_base = 'https://www.bungie.net/Platform/Destiny'
    #api_base = 'https://www.bungie.net/Platform/Destiny2'
    call_url = api_base + method

    request = urllib.request.Request(call_url, headers={'X-API-Key':API_KEY})

    result = urllib.request.urlopen(request).read().decode('utf-8')

    parsed_result = json.loads(result)

    return parsed_result

def getCharacters(destiny_membership_id=None, membership_type=None):
    """getCharacters()"""

    _summary = callBungieAPI('/Destiny2/' + membership_type + '/Profile/'
                               + destiny_membership_id + '?components='
                               + 'Characters')

##    print json.dumps(_summary, indent=4)

    characters = _summary['Response']['characters']['data']
    characters_array = []

##    _character_a = _summary['Response']['characters']['data'][0]\
##             ['characterId']
##    _character_a_class = _summary['Response']['characters']['data'][0]\
##             ['classType']

##    _character = [0 for i in range(3)]

##    _character_a = _summary['Response']['characters']['data'][0]\
##             ['characterId']
##    _character_a_class = _summary['Response']['characters']['data'][0]\
##             ['classType']
##    _character_b = _summary['Response']['characters']['data'][1]\
##             ['characterId']
##    _character_b_class = _summary['Response']['characters']['data'][1]\
##             ['classType']
##    _character_c = _summary['Response']['characters']['data'][2]\
##             ['characterId']
##    _character_c_class = _summary['Response']['characters']['data'][2]\
##             ['classType']

    #print _summary

##    _character_a = _summary['Response']['data']['characters'][0]\
##            ['characterBase']['characterId']
##    _character_a_class = _summary['Response']['data']['characters'][0]\
##            ['characterBase']['classType']
##    _character_b = _summary['Response']['data']['characters'][1]\
##            ['characterBase']['characterId']
##    _character_b_class = _summary['Response']['data']['characters'][1]\
##            ['characterBase']['classType']
##    _character_c = _summary['Response']['data']['characters'][2]\
##            ['characterBase']['characterId']
##    _character_c_class = _summary['Response']['data']['characters'][2]\
##            ['characterBase']['classType']

##    for guardian in range(0, 3):
##        char_id =  _summary['Response']['data']['characters'][guardian]['characterBase']['characterId']
##        class_type = _summary['Response']['data']['characters'][guardian]['characterBase']['classType']
##        _character[class_type] = char_id

##    return _character

    for guardian in characters:
        index = characters[guardian]['classType']
        characters_array.insert(index, characters[guardian]['characterId'])

    return characters_array

def get_characters(destiny_membership_id=None, membership_type=None):
    """get_characters()"""

    _summary = call_bungie_api('/' + membership_type + '/Account/'
                               + destiny_membership_id + '/Summary/')

    _character = [0 for i in range(3)]

    #print _summary

    _character_a = _summary['Response']['data']['characters'][0]\
            ['characterBase']['characterId']
    _character_a_class = _summary['Response']['data']['characters'][0]\
            ['characterBase']['classType']
    _character_b = _summary['Response']['data']['characters'][1]\
            ['characterBase']['characterId']
    _character_b_class = _summary['Response']['data']['characters'][1]\
            ['characterBase']['classType']
    _character_c = _summary['Response']['data']['characters'][2]\
            ['characterBase']['characterId']
    _character_c_class = _summary['Response']['data']['characters'][2]\
            ['characterBase']['classType']

    for guardian in range(0, 3):
        char_id =  _summary['Response']['data']['characters'][guardian]['characterBase']['characterId']
        class_type = _summary['Response']['data']['characters'][guardian]['characterBase']['classType']
        _character[class_type] = char_id

    return _character
