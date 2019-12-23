#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import requests
import json
import settings


class PyTradeTips(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack(fill="both", expand=True, side="top")

        self.tooltip = tk.Label(self, text="Searching...", font=(
            "default", 8), fg="black", justify="left")
        self.tooltip.pack(side="top", fill="both", expand=True)
        self.tooltip.bind("<Enter>", self.hide_window)

        self.last_content = self.parent.clipboard_get()
        self.parent.after(100, self.watch_clipboard)
        self.parent.withdraw()
        self.watch_clipboard()

    def show_window(self, event="none"):
        self.parent.focus_set()
        self.parent.wm_attributes("-topmost", 1)
        self.parent.overrideredirect(True)
        x, y = self.get_position()
        self.parent.geometry("+{}+{}".format(x+10, y+10))
        self.parent.update()
        self.parent.deiconify()

    def get_position(self, event=None):
        x = self.parent.winfo_pointerx()
        y = self.parent.winfo_pointery()
        return x, y

    def hide_window(self, event):
        self.parent.withdraw()
        self.parent.after(100, self.watch_clipboard)

    def watch_clipboard(self):
        try:
            content = self.parent.clipboard_get()
            if content != self.last_content:
                self.last_content = content
                if self.is_item(content):
                    self.show_window()
                    self.item_query(self.item_json(self.item_parser(content)))
                    self.update_text('update')
                else:
                    self.parent.after(100, self.watch_clipboard)
            else:
                self.parent.after(100, self.watch_clipboard)
        except tk.TclError:
            pass

    def is_item(self, iteminfo):
        if iteminfo.startswith('Rarity') and len(iteminfo.split('--------')) == 7:
            return True
        else:
            return False

    def item_parser(self, iteminfo):
        info = iteminfo.split('--------\n')
        item_rarity = info[0].split('\n')[0].split(':')[1].strip()
        item_name = info[0].split('\n')[1]
        item_type = info[0].split('\n')[2]
        item_level = int(info[3].split('\n')[0].split(':')[1].strip())
        return {
            'Name': item_name,
            'Rarity': item_rarity,
            'Type': item_type,
            'iLevel': item_level
        }

    def item_json(self, iteminfo):
        data = {'query': {'status': {'option': 'online'}, 'stats': [
            {'type': 'and', 'filters': []}]}, 'sort': {'price': 'asc'}}
        if iteminfo['Name']:
            data['query']['name'] = iteminfo['Name']
        if iteminfo['Type']:
            data['query']['type'] = iteminfo['Type']
        return data

    def update_text(self, text):
        self.tooltip.config(text=text)

    def item_query(self, data):
        url = settings.SEARCH_API+settings.LEAGUE
        response = requests.post(url, json=data)
        if response.status_code != 200:
            print('Search Error ' + str(response.status_code))
            return

        itemid = response.json()['id']
        list = response.json()['result']
        url = settings.FETCH_URL.format(','.join(list[:settings.MAX]), itemid)

        result = requests.get(url)
        if result.status_code != 200:
            print('Fetch Error ' + str(result.status_code))
            return

        if data['query']['name']:
            title = data['query']['name'] + ' ' + data['query']['type']
        else:
            title = data['query']['type']

        title += ' Total:' + str(response.json()['total'])
        body = []
        print('')
        print('Total:' + str(response.json()['total']))
        infolist = result.json()['result']
        for info in infolist:
            tooltip = 'ID: %s Price %s' % (
                info['listing']['account']['lastCharacterName'], self.process_dict(info['listing']))
            print(tooltip)
            body.append(self.process_dict(info['listing']))

    def process_dict(self,s):
        if s['price']:
            single_price = s['price']['amount']
            unit = s['price']['currency']
            price_info = str(single_price) + ' ' + unit
            return price_info
        else:
            return 'No Price'


if __name__ == "__main__":
    print('CTRL + C to copy item infomation ...')
    root = tk.Tk()
    PyTradeTips(root)
    root.mainloop()
