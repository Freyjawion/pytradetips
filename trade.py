#!/usr/bin/python
# -*- coding: utf-8 -*-

import settings
import requests


class AutoVivification(dict):
    '''Implementation of perl's autovivification feature.'''

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value


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
        if item.Elder_Map_occupied:
            temp = AutoVivification()
            temp['id'] = 'implicit.stat_3624393862'
            temp['disable'] = False
            temp['value']['option'] = item.Elder_Map_occupied
            data['query']['stats'][0]['filters'].append(temp)
    elif item.Category == 'Flask' and item.Rarity == 'Magic':
        data['query']['term'] = item.Name
    elif item.Category == 'Gem':
        if item.Type:
            data['query']['type'] = item.Type
        if item.Gem_level:
            data['query']['filters']['misc_filters']['filters']['gem_level']['min'] = item.Gem_level
        if item.Quality:
            data['query']['filters']['misc_filters']['filters']['quality']['min'] = item.Quality
        if item.Gem_alternate_quality:
            data['query']['filters']['misc_filters']['filters']['gem_alternate_quality']['option'] = item.Gem_alternate_quality
    else:
        if item.Name:
            data['query']['name'] = item.Name
        if item.Type:
            data['query']['type'] = item.Type
        if item.Category == 'BaseType':
            data['query']['filters']['misc_filters']['filters']['ilvl']['min'] = min(
                item.Item_level, 86)
            data['query']['filters']['type_filters']['filters']['rarity']['option'] = 'nonunique'
    if item.Links > 4:
        data['query']['filters']['socket_filters']['filters']['links']['min'] = item.Links
    if item.Sockets == 6:
        data['query']['filters']['socket_filters']['filters']['sockets']['min'] = item.Sockets
    if item.AbyssalSockets:
        pass
    if item.Synthesised:
        data['query']['filters']['misc_filters']['filters']['synthesised_item']['true'] = item.Gem_alternate_quality
    if item.Influence:
        for i in item.Influence:
            data['query']['filters']['misc_filters']['filters']['{}_item'.format(
                i.lower())]['option'] = True
    if item.Corrupted:
        data['query']['filters']['misc_filters']['filters']['corrupted']['option'] = True
    return data


def item_query_trade(item):
    temp = []
    url_query = settings.SEARCH_API+settings.LEAGUE
    url_trade = ''
    headers = {'User-Agent': 'Chrome'}
    data = item_json(item)
    response_query = requests.post(
        url_query, json=data, headers=headers, proxies=settings.proxyDict)
    if response_query.status_code == 200:
        item_id = response_query.json()['id']
        url_trade = settings.TRADE_URL+item_id
        item_result = response_query.json()['result']
        total = response_query.json()['total']
        temp.append(item_id)
        temp.append('Total: {}'.format(str(total)))
        if total:
            url_fetch = settings.FETCH_URL.format(
                ','.join(item_result[:settings.MAX]), item_id)
            response_fetch = requests.get(
                url_fetch, headers=headers, proxies=settings.proxyDict)
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
    return '\n'.join(temp),url_trade


def get_price_trade(result):
    if result['listing']['price']:
        amount = result['listing']['price']['amount']
        currency = result['listing']['price']['currency']
        return '{} {}'.format(str(amount), currency)
    else:
        return 'No Price'
