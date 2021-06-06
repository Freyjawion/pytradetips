#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        self.AbyssalSockets = 0
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

def is_item(content):
    if content.startswith('Rarity') or content.startswith('物品类别'):
        if '--------' in content:
            if len(content.split('--------')[0].splitlines()) in [3, 4]:
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
            elif content.startswith('物品类别'):
                rarity = item_translate(header[1].split(':')[
                                        1], settings.dict_rarity)
                if rarity in ('Rare,Unique') and len(header) > 2:
                    name_line = header[2]
                    type_line = header[3]
                else:
                    name_line = header[2]
                    type_line = header[2]

                if '(' in name_line:
                    base_name = name_line[name_line.find(
                        '(')+1:name_line.find(')')]
                else:
                    base_name = name_line

                if content.splitlines()[-1] == '未鉴定':
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
                    elif 'Oil' in item.Type:
                        item.Category = 'Oil'
                    elif 'Delirium Orb' in item.Type:
                        item.Category = 'Delirium Orb'
                    elif is_fragment(type_line):
                        item.Category = 'Fragment'
                    else:
                        item.Category = 'Currency'
                elif rarity == 'Card':
                    item.Type = base_name
                    item.Name = ''
                    item.Category = 'Card'
                elif rarity == 'Gem':
                    item.Name = ''
                    item.Category = 'Gem'
                    item.Type = base_name
                    for line in content.splitlines():
                        if line.startswith('【英文名：') and 'Vaal' in line:
                            item.Type = line[line.find(
                                '：')+1:line.find('】')].strip()
                        elif line.startswith('等级:') and not item.Gem_level:
                            temp = line.split(':')[1].strip()
                            if '(' in temp:
                                temp = temp.split('(')[0].strip()
                            item.Gem_level = int(temp)
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
                        elif line.startswith('插槽:'):
                            item.GemSocket = line.split(':')[1].strip()
                            item.Sockets = item_sockets(item.GemSocket)
                            item.Links = item_links(item.GemSocket)
                            item.AbyssalSockets = line.count('A')
                        elif line.startswith('已合成'):
                            item.Synthesised = True
                        elif line.startswith('地图等阶:'):
                            item.Map_tier = int(line.split(':')[1].strip())
                        elif line == '塑界之物':
                            item.Influence.append('Shaper')
                        elif line == '长老之物':
                            item.Influence.append('Elder')
                        elif line == '圣战士物品':
                            item.Influence.append('Crusader')
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
        keyword.append('Item Level : {}'.format(min(item.Item_level, 86)))
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
        if item.AbyssalSockets:
            keyword.append('Abyssal Socket : {}'.format(item.AbyssalSockets))
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

def is_fragment(item_type):
    if (
        'Fragment' in item_type
        or 'Timeless' in item_type
        or 'Breachstone' in item_type
        or 'Sacrifice' in item_type
        or 'Mortal' in item_type
        or 'Key' in item_type
        or 'Divine Vessel' in item_type
        or 'to the Goddess' in item_type
        or 'Simulacrum' in item_type
        or 'Splinter' in item_type
        or "The Maven's Writ" in item_type
    ):
        return True
    else:
        return False