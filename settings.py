SEARCH_API = 'https://www.pathofexile.com/api/trade/search/'
FETCH_URL = 'https://www.pathofexile.com/api/trade/fetch/{}?query={}'
LEAGUE = 'Ultimatum'
MAX = 10

NINJA_ITEM_API = 'https://poe.ninja/api/data/itemoverview?league={}&type={}'
NINJA_CURRENCY_API = 'https://poe.ninja/api/data/currencyoverview?league={}&type={}'

NINJA_CURRENCY = NINJA_CURRENCY_API.format(LEAGUE, 'Currency')
NINJA_FRAGMENTS = NINJA_CURRENCY_API.format(LEAGUE, 'Fragment')
NINJA_OILS = NINJA_ITEM_API.format(LEAGUE, 'Oil')
NINJA_INCUBATORS = NINJA_ITEM_API.format(LEAGUE, 'Incubator')
NINJA_SCARABS = NINJA_ITEM_API.format(LEAGUE, 'Scarab')
NINJA_FOSSILS = NINJA_ITEM_API.format(LEAGUE, 'Fossil')
NINJA_RESONATORS = NINJA_ITEM_API.format(LEAGUE, 'Resonator')
NINJA_ESSENCES = NINJA_ITEM_API.format(LEAGUE, 'Essence')
NINJA_DIVINATION_CARDS = NINJA_ITEM_API.format(LEAGUE, 'DivinationCard')
NINJA_PROPHECIES = NINJA_ITEM_API.format(LEAGUE, 'Prophecy')
NINJA_SKILL_GEMS = NINJA_ITEM_API.format(LEAGUE, 'SkillGem')
NINJA_BASE_TYPES = NINJA_ITEM_API.format(LEAGUE, 'BaseType')
NINJA_HELMET_ENCHANTS = NINJA_ITEM_API.format(LEAGUE, 'HelmetEnchant')
NINJA_UNIQUE_MAPS = NINJA_ITEM_API.format(LEAGUE, 'UniqueMap')
NINJA_DELIRIUM_ORBS = NINJA_ITEM_API.format(LEAGUE, 'DeliriumOrb')
NINJA_MAPS = NINJA_ITEM_API.format(LEAGUE, 'Map')
NINJA_BLIGHTED_MAPS = NINJA_ITEM_API.format(LEAGUE, 'BlightedMap')
NINJA_UNIQUE_JEWELS = NINJA_ITEM_API.format(LEAGUE, 'UniqueJewel')
NINJA_UNIQUE_FLASKS = NINJA_ITEM_API.format(LEAGUE, 'UniqueFlask')
NINJA_UNIQUE_WEAPONS = NINJA_ITEM_API.format(LEAGUE, 'UniqueWeapon')
NINJA_UNIQUE_ARMOURS = NINJA_ITEM_API.format(LEAGUE, 'UniqueArmour')
NINJA_UNIQUE_ACCESSORIES = NINJA_ITEM_API.format(LEAGUE, 'UniqueAccessory')
NINJA_BEASTS = NINJA_ITEM_API.format(LEAGUE, 'Beast')

TRADE_URL = 'https://www.pathofexile.com/trade/search/{}/'.format(LEAGUE)

http_proxy  = "socks5://127.0.0.1:10808"
https_proxy = "socks5://127.0.0.1:10808"
ftp_proxy   = "ftp://127.0.0.1:10809"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }

dict_rarity = {
    '传奇': 'Unique',
    '稀有': 'Rare',
    '魔法': 'Magic',
    '普通': 'Normal',
    '命运卡': 'Card',
    '通货': 'Currency',
    '宝石': 'Gem'
}
