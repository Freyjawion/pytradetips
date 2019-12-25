#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import requests
import settings


dict_rarity = {
    '传奇': 'Unique',
    '稀有': 'Rare',
    '魔法': 'Magic',
    '普通': 'Normal',
    '命运卡': 'Card',
    '通货': 'Currency',
    '宝石': 'Gem'
}


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


class AutoVivification(dict):
    """Implementation of perl's autovivification feature."""

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
        self.pack(fill="both", expand=True, side="top")

        self.tooltip = tk.Label(self, text="PyTooltip", font=(
            "default", 8), fg="black", justify="left")
        self.tooltip.pack(side="top", fill="both", expand=True)
        self.tooltip.bind("<Enter>", self.hide_tooltip)

        self.last_content = ''
        self.text = ''
        self.parent.clipboard_clear()
        self.parent.clipboard_append('')
        self.parent.withdraw()
        self.parent.after(100, self.watch_clipboard)

    def show_tooltip(self, event="none"):
        self.parent.withdraw()
        self.parent.focus_set()
        self.parent.wm_attributes("-topmost", 1)
        self.parent.overrideredirect(True)
        x, y = self.get_position()
        self.parent.geometry("+{}+{}".format(x+15, y+15))
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
                    self.text = item_keyword(item)
                    self.update_tooltip()
                    self.show_tooltip()
                    self.parent.after(5, self.update_text, item)
                else:
                    self.parent.after(100, self.watch_clipboard)
            else:
                self.parent.after(100, self.watch_clipboard)
        except tk.TclError:
            self.parent.after(100, self.watch_clipboard)

    def update_tooltip(self):
        self.tooltip.config(text=self.text)

    def update_text(self, item):
        self.text += item_query(item)
        self.update_tooltip()
        print(self.text)
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
                rarity = item_translate(header[0].split(':')[1], dict_rarity)
                if rarity in ('Rare,Unique'):
                    name_line = header[1]
                    type_line = header[2]
                else:
                    name_line = header[1]
                    type_line = header[1]

                if '(' in name_line:
                    base_name = name_line[name_line.find(
                        "(")+1:name_line.find(")")]
                else:
                    base_name = name_line

                if '未鉴定' in content.splitlines():
                    item.Category = 'unIdentified'
                elif rarity == 'Currency':
                    item.Type = base_name
                    item.Name = ''
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
                                "(")+1:type_line.find(")")]
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
                    elif '' in name_line:
                        pass
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
            data['query']['filters']['type_filters']['rarity']['option'] = 'unique'
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
            data['query']['filters']['type_filters']['rarity']['option'] = 'nonunique'
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


def item_query(item):
    temp = ['\n']
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
                    temp.append(get_price(result))
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


def get_price(result):
    if result['listing']['price']:
        amount = result['listing']['price']['amount']
        currency = result['listing']['price']['currency']
        return '{} {}'.format(str(amount), currency)
    else:
        return 'No Price'


if __name__ == "__main__":
    print('CTRL + C to copy item infomation ...')
    root = tk.Tk()
    PyTooltip(root)
    root.mainloop()
