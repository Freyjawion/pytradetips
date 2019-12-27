#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import requests
import settings
import os


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
        self.Sockets = ''
        self.Links = 0
        self.Shaped_map = False
        self.Elder_map = False
        self.Blighted_map = False
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
                    for line in content.splitlines():
                        if line.startswith('物品等级:'):
                            item.Item_level = int(line.split(':')[1].strip())
                        elif line.startswith('宝石孔:'):
                            item.Sockets = line.split(':')[1].strip()
                            item.Links = item_links(item.Sockets)
                        elif line.startswith('已合成'):
                            item.Synthesised = True
                        elif line.startswith('地图等阶:'):
                            item.Map_tier = int(line.split(':')[1].strip())
                        elif line == '已腐化':
                            item.Corrupted = True
                        elif line == '塑界之物':
                            item.Shaper_influence = True
                        elif line == '长老之物':
                            item.Elder_influence = True
                        elif line == '总督军物品':
                            item.Warlord_influence = True
                        elif line == '审判官物品':
                            item.Redeemer_influence = True
                        elif line == '狩猎者物品':
                            item.Hunter_influence = True
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
    if item.Item_level and not item.Rarity == 'Unique' and not item.Category:
        keyword.append('Item Level : {}'.format(str(item.Item_level)))
    if item.Gem_level:
        keyword.append('Gem Level : {}'.format(str(item.Gem_level)))
    if item.Map_tier:
        keyword.append('Map Tier : {}'.format(str(item.Map_tier)))
    if item.Quality:
        keyword.append('Quality : {}%'.format(str(item.Quality)))
    if item.Sockets:
        if item.Links > 4:
            keyword.append('Sockets : {} , {}Links'.format(
                item.Sockets, str(item.Links)))
    if item.Blighted_map:
        keyword.append('Blighted Map')
    if item.Shaper_influence:
        keyword.append('Shaper Item')
    if item.Elder_influence:
        keyword.append('Elder Item')
    if item.Crusader_influence:
        keyword.append('Crusader Item')
    if item.Redeemer_influence:
        keyword.append('Redeemer Item')
    if item.Hunter_influence:
        keyword.append('Hunter Item')
    if item.Warlord_influence:
        keyword.append('Warlord Item')
    if item.Corrupted:
        keyword.append('Corrupted')
    return '\n'.join(keyword)


def item_links(sockets):
    return max(len(i) for i in sockets[1::2].split(' '))+1


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
        if item.Item_level and not item.Rarity == 'Unique':
            data['query']['filters']['misc_filters']['filters']['ilvl']['min'] = item.Item_level
            data['query']['filters']['type_filters']['filters']['rarity']['option'] = 'nonunique'
    if item.Links > 4:
        data['query']['filters']['socket_filters']['filters']['links']['min'] = item.Links
    if item.Corrupted:
        data['query']['filters']['misc_filters']['filters']['corrupted']['option'] = True
    if item.Shaper_influence:
        data['query']['filters']['misc_filters']['filters']['shaper_item']['option'] = True
    if item.Elder_influence:
        data['query']['filters']['misc_filters']['filters']['elder_item']['option'] = True
    if item.Crusader_influence:
        data['query']['filters']['misc_filters']['filters']['crusader_item']['option'] = True
    if item.Redeemer_influence:
        data['query']['filters']['misc_filters']['filters']['redeemer_item']['option'] = True
    if item.Hunter_influence:
        data['query']['filters']['misc_filters']['filters']['hunter_item']['option'] = True
    if item.Warlord_influence:
        data['query']['filters']['misc_filters']['filters']['warlord_item']['option'] = True

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
    if item.Category == 'Currency':
        for i in NinjaData.Currencies['lines']:
            if i['currencyTypeName'] == item.Type:
                return '{} chaos'.format(i['chaosEquivalent'])
    elif item.Category == 'Fragment':
        for i in NinjaData.Fragments['lines']:
            if i['currencyTypeName'] == item.Type:
                return '{} chaos'.format(i['chaosEquivalent'])
    elif item.Category == 'Oil':
        return query_item_ninja_common(NinjaData.Oils['lines'], item)
    elif item.Category == 'Incubator':
        return query_item_ninja_common(NinjaData.Incubators['lines'], item)
    elif item.Category == 'Scarab':
        return query_item_ninja_common(NinjaData.Scarabs['lines'], item)
    elif item.Category == 'Fossil':
        return query_item_ninja_common(NinjaData.Fossils['lines'], item)
    elif item.Category == 'Resonator':
        return query_item_ninja_common(NinjaData.Resonators['lines'], item)
    elif item.Category == 'Essence':
        return query_item_ninja_common(NinjaData.Essences['lines'], item)
    elif item.Category == 'Card':
        return query_item_ninja_common(NinjaData.DivinationCards['lines'], item)
    elif item.Category == 'Prophecy':
        return query_item_ninja_common(NinjaData.Prophecies['lines'], item)
    elif item.Category == 'Gem':
        for i in NinjaData.SkillGems['lines']:
            if i['name'] == item.Type and i['GemLevel'] == item.Gem_level and i['gemQuality'] == item.Quality and i['Corrupted'] == item.Corrupted:
                return '{} chaos {} exalted'.format(i['chaosValue'], i['exaltedValue'])
    elif item.Category == 'BaseType':
        pass
    elif item.Category == 'HelmetEnchant':
        pass
    elif item.Category == 'Map':
        return query_item_ninja_map(NinjaData.Maps['lines'], NinjaData.UniqueMaps['lines'], item)
    elif item.Category == 'Flask':
        return query_item_ninja_common(NinjaData.UniqueFlasks['lines'], item)
    elif item.Category == 'UniqueGear':
        pass
    elif item.Category == 'Beast':
        pass
    return 'Ninja not found'


def query_item_ninja_common(data, item):
    if item.Type == 'Prophecy':
        item_name = item.Name
    else:
        item_name = item.Type
    for i in data:
        if i['name'] == item_name:
            return '{} chaos {} exalted'.format(i['chaosValue'], i['exaltedValue'])
    return 'Ninja not found'


def query_item_ninja_map(data, Udata, item):
    if item.Rarity == 'Unique':
        map_name = item.Name
        map_data = Udata
    else:
        if item.Blighted_map:
            map_name = 'Blighted {}'.format(item.Type)
        else:
            map_name = item.Type
        map_data = data
    for i in map_data:
        if i['name'] == map_name and i['mapTier'] == item.Map_tier:
            return '{} chaos {} exalted'.format(i['chaosValue'], i['exaltedValue'])
    return 'Ninja not found'


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
