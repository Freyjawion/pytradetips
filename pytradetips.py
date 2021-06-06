#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
import settings
import iteminfo
import ninja
import trade


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
                item = iteminfo.item_parser(content)
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
        self.text = iteminfo.item_keyword(item)
        self.update_tooltip()

    def query_ninja(self, item):
        text = ninja.item_query_ninja(item, NinjaData)
        self.text += '\n \n'
        self.text += text
        self.update_tooltip()
        print(text)
        print()

    def query_trade(self, item):
        text,url_trade = trade.item_query_trade(item)
        self.text += '\n \n'
        self.text += text
        self.update_tooltip()
        self.last_content = url_trade
        self.parent.clipboard_clear()
        self.parent.clipboard_append(url_trade)
        print(text)
        print()
        self.parent.after(100, self.watch_clipboard)


if __name__ == '__main__':
    print('Get data from POE.Ninja...')
    NinjaData = ninja.NinjaCache()
    ninja.cache_ninja(NinjaData)
    print('CTRL + C to copy item infomation ...')
    root = tk.Tk()
    PyTooltip(root)
    root.mainloop()
