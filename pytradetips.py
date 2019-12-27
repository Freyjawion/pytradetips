#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import requests
import settings


class ItemInfo():
    def __init__(self):
        self.Name = ''
        self.Type = ''
        self.Category = ''
        self.Item_level = 0
        self.Rarity = ''
        self.Gem_level = 0
        self.Quality = 0
        self.Map_tier = 0
        self.GemSocket = ''
        self.Links = 0
        self.Sockets = 0
        self.Shaped_map = False
        self.Elder_map = False
        self.Blighted_map = False
        self.Influence = []
        self.Shaper_influence = False
        self.Elder_influence = False
        self.Crusader_influence = False
        self.Redeemer_influence = False
        self.Hunter_influence = False
        self.Warlord_influence = False
        self.Synthesised = False
        self.Corrupted = False


class NinjaCache():
    def __init__(self):
        self.Currencies = {}
        self.Fragments = {}
        self.Oils = {}
        self.Incubators = {}
        self.Scarabs = {}
        self.Fossils = {}
        self.Resonators = {}
        self.Essences = {}
        self.DivinationCards = {}
        self.Prophecies = {}
        self.SkillGems = {}
        self.BaseTypes = {}
        self.HelmetEnchants = {}
        self.UniqueMaps = {}
        self.Maps = {}
        self.UniqueJewels = {}
        self.UniqueFlasks = {}
        self.UniqueWeapons = {}
        self.UniqueArmours = {}
        self.UniqueAccessories = {}
        self.Beasts = {}


class AutoVivification(dict):
    '''Implementation of perl's autovivification feature.'''

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


class PyTooltip(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack(fill='both', expand=True, side='top')

        self.tooltip = tk.Label(self, text='PyTooltip', font=(
            'default', 8), fg='black', justify='left')
        self.tooltip.pack(side='top', fill='both', expand=True)
        self.tooltip.bind('<Enter>', self.hide_tooltip)

        self.last_content = ''
        self.text = ''
        self.parent.clipboard_clear()
        self.parent.clipboard_append('')
        self.parent.withdraw()
        self.parent.after(100, self.watch_clipboard)

    def show_tooltip(self, event='none'):
        self.parent.withdraw()
        self.parent.focus_set()
        self.parent.wm_attributes('-topmost', 1)
        self.parent.overrideredirect(True)
        x, y = self.get_position()
        self.parent.geometry('+{}+{}'.format(x+20, y+10))
        self.parent.update()
        self.parent.deiconify()

    def get_position(self, event=None):
        x = self.parent.winfo_pointerx()
        y = self.parent.winfo_pointery()
        return x, y

    def hide_tooltip(self, event):
        self.parent.withdraw()
        self.parent.after(100, self.watch_clipboard)

    def watch_clipboard(self):
        try:
            content = self.parent.clipboard_get()
            if content != self.last_content:
                self.last_content = content
                item = item_parser(content)
                if item:
                    self.last_content = ''
                    self.parent.clipboard_clear()
                    self.parent.clipboard_append('')
                    self.get_keyword(item)
                    self.query_ninja(item)
                    self.show_tooltip()
                    self.parent.after(5, self.query_trade, item)
                else:
                    self.parent.after(100, self.watch_clipboard)
            else:
                self.parent.after(100, self.watch_clipboard)
        except tk.TclError:
            self.parent.after(100, self.watch_clipboard)

    def update_tooltip(self):
        self.tooltip.config(text=self.text)

    def get_keyword(self, item):
        self.text = item_keyword(item)
        self.update_tooltip()

    def query_ninja(self, item):
        text = item_query_ninja(item)
        self.text += '\n \n'
        self.text += text
        self.update_tooltip()
        print(text)
        print()

    def query_trade(self, item):
        text = item_query_trade(item)
        self.text += '\n \n'
        self.text += text
        self.update_tooltip()
        print(text)
        print()
        self.parent.after(100, self.watch_clipboard)


def is_item(content):
    if content.startswith('Rarity') or content.startswith('稀有度'):
        if '--------' in content:
            if len(content.split('--------')[0].splitlines()) in [2, 3]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def item_parser(content):
    try:
        if is_item(content):
            item = ItemInfo()
            header = content.split('--------')[0].splitlines()
            if content.startswith('Rarity'):
                return ''
            elif content.startswith('稀有度'):
                rarity = item_translate(header[0].split(':')[
                                        1], settings.dict_rarity)
                if rarity in ('Rare,Unique'):
                    name_line = header[1]
                    type_line = header[2]
                else:
                    name_line = header[1]
                    type_line = header[1]

                if '(' in name_line:
                    base_name = name_line[name_line.find(
                        '(')+1:name_line.find(')')]
                else:
                    base_name = name_line

                if '未鉴定' in content.splitlines():
                    item.Category = 'unIdentified'
                elif rarity == 'Currency':
                    item.Type = base_name
                    item.Name = ''
                    if 'Fossil' in item.Type:
                        item.Category = 'Fossil'
                    elif 'Resonator' in item.Type:
                        item.Category = 'Resonator'
                    elif 'Essence' in item.Type:
                        item.Category = 'Essence'
                    else:
                        item.Category = 'Currency'
                elif rarity == 'Card':
                    item.Type = base_name
                    item.Name = ''
                    item.Category = 'Card'
                elif rarity == 'Gem':
                    item.Name = ''
                    item.Category = 'Gem'
                    for line in content.splitlines():
                        if line.startswith('【英文名：'):
                            item.Type = line[line.find(
                                '：')+1:line.find('】')].strip()
                        elif line.startswith('等级:') and not item.Gem_level:
                            item.Gem_level = int(line.split(':')[1].strip())
                        elif line.startswith('品质:'):
                            item.Quality = int(
                                line[line.find('+')+1:line.find('%')].strip())
                        elif line == '已腐化':
                            item.Corrupted = True
                else:
                    item.Rarity = rarity
                    if item.Rarity == 'Normal':
                        item.Type = base_name
                        item.Name = ''
                    elif item.Rarity == 'Magic':
                        item.Type = base_name
                        if 'Flask' in type_line:
                            temp = []
                            for i in type_line.split(' '):
                                if '(' in i:
                                    temp.append(i.split('(')[1])
                                elif ')' in i:
                                    temp.append(i.split(')')[0])
                                else:
                                    temp.append(i)
                            item.Name = ' '.join(temp)
                        else:
                            item.Name = ''
                    else:
                        if item.Rarity == 'Unique':
                            item.Name = base_name
                        else:
                            item.Name = ''
                        if '(' in type_line:
                            item.Type = type_line[type_line.find(
                                '(')+1:type_line.find(')')]
                        else:
                            item.Type = type_line

                    if '预言' in type_line:
                        item.Category = 'Prophecy'
                        item.Name = base_name
                        item.Type = 'Prophecy'
                    elif 'Scarab' in type_line:
                        item.Category = 'Scarab'
                    elif 'Flask' in type_line:
                        item.Category = 'Flask'
                    elif 'Map' in type_line:
                        item.Category = 'Map'
                        if type_line.startswith('萎灭'):
                            item.Blighted_map = True
                    elif is_fragment(type_line):
                        item.Category = 'Fragment'
                    elif item.Rarity == 'Unique':
                        item.Category = 'Unique'
                    else:
                        item.Category = 'BaseType'

                    for line in content.splitlines():
                        if line.startswith('物品等级:'):
                            item.Item_level = int(line.split(':')[1].strip())
                        elif line.startswith('宝石孔:'):
                            item.GemSocket = line.split(':')[1].strip()
                            item.Sockets = item_sockets(item.GemSocket)
                            item.Links = item_links(item.GemSocket)
                        elif line.startswith('已合成'):
                            item.Synthesised = True
                        elif line.startswith('地图等阶:'):
                            item.Map_tier = int(line.split(':')[1].strip())
                        elif line == '塑界之物':
                            item.Influence.append('Shaper')
                        elif line == '长老之物':
                            item.Influence.append('Elder')
                        elif line == '总督军物品':
                            item.Influence.append('Warlord')
                        elif line == '审判官物品':
                            item.Influence.append('Redeemer')
                        elif line == '狩猎者物品':
                            item.Influence.append('Hunter')
                        elif line == '已腐化':
                            item.Corrupted = True
            return item
        else:
            return ''
    except:
        return ''


def item_keyword(item):
    keyword = []
    if item.Name:
        keyword.append(item.Name)
    if item.Type:
        keyword.append(item.Type)
    if item.Category == 'BaseType':
        keyword.append('Item Level : {}'.format(min(item.Item_level,86)))
    if item.Gem_level:
        keyword.append('Gem Level : {}'.format(item.Gem_level))
    if item.Map_tier:
        keyword.append('Map Tier : {}'.format(item.Map_tier))
    if item.Quality:
        keyword.append('Quality : {}%'.format(item.Quality))
    if item.GemSocket:
        if item.Links > 4 or item.Sockets == 6:
            keyword.append('{} ,{}S {}L'.format(
                item.GemSocket, item.Sockets, item.Links))
    if item.Blighted_map:
        keyword.append('Blighted Map')
    if item.Influence:
        for i in item.Influence:
            keyword.append('{} Item'.format(i))
    if item.Corrupted:
        keyword.append('Corrupted')
    return '\n'.join(keyword)


def item_sockets(GemSocket):
    return len(GemSocket[::2])


def item_links(GemSocket):
    return max(len(i) for i in GemSocket[1::2].split(' '))+1


def item_translate(item_name, item_dict):
    return item_dict.get(item_name.strip())


def item_json(item):
    data = AutoVivification()
    data['query']['status']['option'] = 'online'
    data['query']['stats'][0]['type'] = 'and'
    data['query']['stats'][0]['filters'] = []
    data['sort']['price'] = 'asc'

    if item.Category == 'Map':
        data['query']['type']['option'] = item.Type
        data['query']['type']['discriminator'] = 'warfortheatlas'
        data['query']['filters']['map_filters']['filters']['map_tier']['min'] = item.Map_tier
        data['query']['filters']['map_filters']['filters']['map_tier']['max'] = item.Map_tier
        if item.Rarity == 'Unique':
            data['query']['filters']['type_filters']['filters']['rarity']['option'] = 'unique'
        if item.Blighted_map:
            data['query']['filters']['map_filters']['filters']['map_blighted']['option'] = True
    elif item.Category == 'Flask' and item.Rarity == 'Magic':
        data['query']['term'] = item.Name
    elif item.Category == 'Gem':
        if item.Type:
            data['query']['type'] = item.Type
        if item.Gem_level:
            data['query']['filters']['misc_filters']['filters']['gem_level']['min'] = item.Gem_level
        if item.Quality:
            data['query']['filters']['misc_filters']['filters']['quality']['min'] = item.Quality
    else:
        if item.Name:
            data['query']['name'] = item.Name
        if item.Type:
            data['query']['type'] = item.Type
        if item.Category == 'BaseType':
            data['query']['filters']['misc_filters']['filters']['ilvl']['min'] = min(item.Item_level,86)
            data['query']['filters']['type_filters']['filters']['rarity']['option'] = 'nonunique'
    if item.Links > 4:
        data['query']['filters']['socket_filters']['filters']['links']['min'] = item.Links
    if item.Sockets == 6:
        data['query']['filters']['socket_filters']['filters']['sockets']['min'] = item.Sockets
    if item.Influence:
        for i in item.Influence:
            data['query']['filters']['misc_filters']['filters']['{}_item'.format(i.lower())]['option'] = True
    if item.Corrupted:
        data['query']['filters']['misc_filters']['filters']['corrupted']['option'] = True
    return data


def item_query_trade(item):
    temp = []
    url_query = settings.SEARCH_API+settings.LEAGUE
    data = item_json(item)
    response_query = requests.post(url_query, json=data)
    if response_query.status_code == 200:
        item_id = response_query.json()['id']
        item_result = response_query.json()['result']
        total = response_query.json()['total']
        temp.append(item_id)
        temp.append('Total: {}'.format(str(total)))
        if total:
            url_fetch = settings.FETCH_URL.format(
                ','.join(item_result[:settings.MAX]), item_id)
            response_fetch = requests.get(url_fetch)
            if response_fetch.status_code == 200:
                for result in response_fetch.json()['result']:
                    temp.append(get_price_trade(result))
            else:
                if response_fetch.json()['error']['message']:
                    temp.append(response_fetch.json()['error']['message'])
                else:
                    temp.append('Fetch Error')
    else:
        if response_query.json()['error']['message']:
            temp.append(response_query.json()['error']['message'])
        else:
            temp.append('Query Error')
    return '\n'.join(temp)


def get_price_trade(result):
    if result['listing']['price']:
        amount = result['listing']['price']['amount']
        currency = result['listing']['price']['currency']
        return '{} {}'.format(str(amount), currency)
    else:
        return 'No Price'


def cache_ninja(ninja):
    ninja.Currencies = get_json_ninja(settings.NINJA_CURRENCY)
    ninja.Fragments = get_json_ninja(settings.NINJA_FRAGMENTS)
    ninja.Oils = get_json_ninja(settings.NINJA_OILS)
    ninja.Incubators = get_json_ninja(settings.NINJA_INCUBATORS)
    ninja.Scarabs = get_json_ninja(settings.NINJA_SCARABS)
    ninja.Fossils = get_json_ninja(settings.NINJA_FOSSILS)
    ninja.Resonators = get_json_ninja(settings.NINJA_RESONATORS)
    ninja.Essences = get_json_ninja(settings.NINJA_ESSENCES)
    ninja.DivinationCards = get_json_ninja(settings.NINJA_DIVINATION_CARDS)
    ninja.Prophecies = get_json_ninja(settings.NINJA_PROPHECIES)
    ninja.SkillGems = get_json_ninja(settings.NINJA_SKILL_GEMS)
    ninja.BaseTypes = get_json_ninja(settings.NINJA_BASE_TYPES)
    ninja.HelmetEnchants = get_json_ninja(settings.NINJA_HELMET_ENCHANTS)
    ninja.UniqueMaps = get_json_ninja(settings.NINJA_UNIQUE_MAPS)
    ninja.Maps = get_json_ninja(settings.NINJA_MAPS)
    ninja.UniqueJewels = get_json_ninja(settings.NINJA_UNIQUE_JEWELS)
    ninja.UniqueFlasks = get_json_ninja(settings.NINJA_UNIQUE_FLASKS)
    ninja.UniqueWeapons = get_json_ninja(settings.NINJA_UNIQUE_WEAPONS)
    ninja.UniqueArmours = get_json_ninja(settings.NINJA_UNIQUE_ARMOURS)
    ninja.UniqueAccessories = get_json_ninja(settings.NINJA_UNIQUE_ACCESSORIES)
    ninja.Beasts = get_json_ninja(settings.NINJA_BEASTS)


def get_json_ninja(fetch_url):
    response = requests.get(fetch_url)
    print(fetch_url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed!!!')
        return {}


def item_query_ninja(item):
    chaos_value = 0
    exalted_value = 0
    if item.Category == 'Currency':
        chaos_value = item_query_ninja_currency(NinjaData.Currencies['lines'], item)
    elif item.Category == 'Fragment':
        chaos_value = item_query_ninja_currency(NinjaData.Fragments['lines'], item)
    elif item.Category == 'Oil':
        chaos_value,exalted_value = item_query_ninja_common(NinjaData.Oils['lines'], item)
    elif item.Category == 'Incubator':
        chaos_value,exalted_value = item_query_ninja_common(NinjaData.Incubators['lines'], item)
    elif item.Category == 'Scarab':
        chaos_value,exalted_value = item_query_ninja_common(NinjaData.Scarabs['lines'], item)
    elif item.Category == 'Fossil':
        chaos_value,exalted_value = item_query_ninja_common(NinjaData.Fossils['lines'], item)
    elif item.Category == 'Resonator':
        chaos_value,exalted_value = item_query_ninja_common(NinjaData.Resonators['lines'], item)
    elif item.Category == 'Essence':
        chaos_value,exalted_value = item_query_ninja_common(NinjaData.Essences['lines'], item)
    elif item.Category == 'Card':
        chaos_value,exalted_value = item_query_ninja_common(NinjaData.DivinationCards['lines'], item)
    elif item.Category == 'Prophecy':
        chaos_value,exalted_value = item_query_ninja_common(NinjaData.Prophecies['lines'], item)
    elif item.Category == 'Gem':
        for i in NinjaData.SkillGems['lines']:
            if i['name'] == item.Type and i['GemLevel'] == item.Gem_level and i['gemQuality'] == item.Quality and i['Corrupted'] == item.Corrupted:
                return '{} chaos {} exalted'.format(i['chaosValue'], i['exaltedValue'])
    elif item.Category == 'BaseType':
        chaos_value,exalted_value = item_query_ninja_base(NinjaData.BaseTypes['lines'], item)
    elif item.Category == 'HelmetEnchant':
        pass
    elif item.Category == 'Map':
        chaos_value,exalted_value = item_query_ninja_map(NinjaData.Maps['lines'], NinjaData.UniqueMaps['lines'], item)
    elif item.Category == 'Flask':
        chaos_value,exalted_value = item_query_ninja_common(NinjaData.UniqueFlasks['lines'], item)
    elif item.Category == 'Unique':
        chaos_value,exalted_value = item_query_ninja_unique(NinjaData.UniqueWeapons['lines'], NinjaData.UniqueArmours['lines'], NinjaData.UniqueAccessories['lines'], item)
    elif item.Category == 'Beast':
        pass
    
    if chaos_value == 0:
        return 'Not Found'
    else:
        if exalted_value > 1:
            return '{} chaos {} exalted'.format(chaos_value, exalted_value)
        else:
            return '{} chaos'.format(chaos_value)


def item_query_ninja_common(data, item):
    if item.Type == 'Prophecy':
        item_name = item.Name
    else:
        item_name = item.Type
    for i in data:
        if i['name'] == item_name:
            return i['chaosValue'], i['exaltedValue']
    return 0,0


def item_query_ninja_currency(data, item):
    for i in data:
        if i['currencyTypeName'] == item.Type:
            return i['chaosEquivalent']
    return 0


def item_query_ninja_base(data, item):
    if item.Item_level < 82:
        return 0,0
    elif item.Item_level > 85:
        item_level = 86
    else:
        item_level = item.Item_level

    if item.Influence:
        if len(item.Influence)>1:
            return 0,0
        else:
            item_variant = item.Influence[0]
    else:
        item_variant = ''
        
    for i in data:
        if i['name'] == item.Type and i['levelRequired'] == item_level and i['variant'] == item_variant:
                return i['chaosValue'], i['exaltedValue']
    return 0,0


def item_query_ninja_unique(Weapon, Armour, Accessory, item):
    unique_data = [Weapon, Armour, Accessory]
    if item.Links >4:
        item_link = item.Links
    else:
        item_link = 0
    for data in unique_data:
        for i in data:
            if i['name'] == item.Name and i['links'] == item_link:
                return i['chaosValue'], i['exaltedValue']
    return 0,0


def item_query_ninja_map(Map, UniqueMap, item):
    if item.Rarity == 'Unique':
        map_name = item.Name
        map_data = UniqueMap
    else:
        if item.Blighted_map:
            map_name = 'Blighted {}'.format(item.Type)
        else:
            map_name = item.Type
        map_data = Map
    for i in map_data:
        if i['name'] == map_name and i['mapTier'] == item.Map_tier:
            return i['chaosValue'], i['exaltedValue']
    return 0,0


def is_fragment(item_type):
    if (
        'Fragment' in item_type
        or 'Timeless' in item_type
        or 'Breachstone' in item_type
        or 'Sacrifice' in item_type
        or 'Mortal' in item_type
        or 'Key' in item_type
        or 'Divine Vessel' in item_type
        or 'Offering to the Goddess' in item_type
    ):
        return True
    else:
        return False


if __name__ == '__main__':
    print('Get data from POE.Ninja...')
    NinjaData = NinjaCache()
    cache_ninja(NinjaData)
    print('CTRL + C to copy item infomation ...')
    root = tk.Tk()
    PyTooltip(root)
    root.mainloop()
