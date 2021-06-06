#!/usr/bin/python
# -*- coding: utf-8 -*-

import settings
import requests


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
        self.DeliriumOrbs = {}
        self.Maps = {}
        self.BlightedMaps = {}
        self.UniqueJewels = {}
        self.UniqueFlasks = {}
        self.UniqueWeapons = {}
        self.UniqueArmours = {}
        self.UniqueAccessories = {}
        self.Beasts = {}


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
    ninja.DeliriumOrbs = get_json_ninja(settings.NINJA_DELIRIUM_ORBS)
    ninja.Maps = get_json_ninja(settings.NINJA_MAPS)
    ninja.BlightedMaps = get_json_ninja(settings.NINJA_BLIGHTED_MAPS)
    ninja.UniqueJewels = get_json_ninja(settings.NINJA_UNIQUE_JEWELS)
    ninja.UniqueFlasks = get_json_ninja(settings.NINJA_UNIQUE_FLASKS)
    ninja.UniqueWeapons = get_json_ninja(settings.NINJA_UNIQUE_WEAPONS)
    ninja.UniqueArmours = get_json_ninja(settings.NINJA_UNIQUE_ARMOURS)
    ninja.UniqueAccessories = get_json_ninja(settings.NINJA_UNIQUE_ACCESSORIES)
    ninja.Beasts = get_json_ninja(settings.NINJA_BEASTS)


def get_json_ninja(fetch_url):
    response = requests.get(fetch_url, proxies=settings.proxyDict)
    print(fetch_url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed!!!')
        return {}


def item_query_ninja(item, NinjaData):
    chaos_value = 0
    exalted_value = 0
    if item.Category == 'Currency':
        chaos_value = item_query_ninja_currency(
            NinjaData.Currencies['lines'], item)
    elif item.Category == 'Fragment':
        chaos_value = item_query_ninja_currency(
            NinjaData.Fragments['lines'], item)
    elif item.Category == 'Oil':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.Oils['lines'], item)
    elif item.Category == 'Incubator':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.Incubators['lines'], item)
    elif item.Category == 'Scarab':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.Scarabs['lines'], item)
    elif item.Category == 'Fossil':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.Fossils['lines'], item)
    elif item.Category == 'Resonator':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.Resonators['lines'], item)
    elif item.Category == 'Essence':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.Essences['lines'], item)
    elif item.Category == 'Delirium Orb':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.DeliriumOrbs['lines'], item)
    elif item.Category == 'Card':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.DivinationCards['lines'], item)
    elif item.Category == 'Prophecy':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.Prophecies['lines'], item)
    elif item.Category == 'Gem':
        chaos_value, exalted_value = item_query_ninja_gem(
            NinjaData.SkillGems['lines'], item)
    elif item.Category == 'BaseType':
        chaos_value, exalted_value = item_query_ninja_base(
            NinjaData.BaseTypes['lines'], item)
    elif item.Category == 'HelmetEnchant':
        pass
    elif item.Category == 'Map':
        chaos_value, exalted_value = item_query_ninja_map(
            NinjaData.Maps['lines'], NinjaData.UniqueMaps['lines'], NinjaData.BlightedMaps['lines'], item)
    elif item.Category == 'Flask':
        chaos_value, exalted_value = item_query_ninja_common(
            NinjaData.UniqueFlasks['lines'], item)
    elif item.Category == 'Unique':
        unique_data = [NinjaData.UniqueWeapons['lines'], NinjaData.UniqueArmours['lines'],
                       NinjaData.UniqueAccessories['lines'], NinjaData.UniqueJewels['lines']]
        chaos_value, exalted_value = item_query_ninja_unique(unique_data, item)
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
    if item.Category in ['Prophecy','Flask']:
        item_name = item.Name
    else:
        item_name = item.Type
    for i in data:
        if i['name'] == item_name:
            return i['chaosValue'], i['exaltedValue']
    return 0, 0


def item_query_ninja_currency(data, item):
    for i in data:
        if i['currencyTypeName'] == item.Type:
            return i['chaosEquivalent']
    return 0


def item_query_ninja_gem(data, item):
    if item.Quality < 20:
        gem_quality = 0
    else:
        gem_quality = item.Quality
    for i in data:
        try:
            if i['name'] == item.Type and i['gemLevel'] == item.Gem_level and i['gemQuality'] == gem_quality and i['corrupted'] == item.Corrupted:
                return i['chaosValue'], i['exaltedValue']
        except KeyError:
            pass
    return 0, 0


def item_query_ninja_base(data, item):
    if item.Item_level < 82:
        return 0, 0
    elif item.Item_level > 85:
        item_level = 86
    else:
        item_level = item.Item_level
    if item.Influence:
        if len(item.Influence) > 1:
            return 0, 0
        else:
            item_variant = item.Influence[0]
    else:
        item_variant = ''
    for i in data:
        try:
            if i['name'] == item.Type and i['levelRequired'] == item_level and i['variant'] == item_variant:
                return i['chaosValue'], i['exaltedValue']
        except KeyError:
            pass
    return 0, 0


def item_query_ninja_unique(UniqueData, item):
    if item.Links > 4:
        item_link = item.Links
    else:
        item_link = 0
    for data in UniqueData:
        for i in data:
            try:
                if i['name'] == item.Name and i['links'] == item_link:
                    return i['chaosValue'], i['exaltedValue']
            except KeyError:
                pass
    return 0, 0


def item_query_ninja_map(Map, UniqueMap, BlightedMap, item):
    if item.Rarity == 'Unique':
        map_name = item.Name
        map_data = UniqueMap
    else:
        if item.Blighted_map:
            map_name = 'Blighted {}'.format(item.Type)
            map_data = BlightedMap
        else:
            map_name = item.Type
            map_data = Map
    for i in map_data:
        if i['name'] == map_name and i['mapTier'] == item.Map_tier:
            return i['chaosValue'], i['exaltedValue']
    return 0, 0
