import string

from snap.game.client.models.nuverse.cube.common.deck import Deck
from snap.game.constants.enums.card_series_def_enum import CardSeriesDefEnum
from snap.game_data_cache.models.game_data_cache import GameDataCache
from snap.matches.documents.match_player_record import MatchPlayerRecord


def get_average_cost(card_ids: list[str], gdc: GameDataCache):
    costs = []
    for card_id in card_ids:
        card_def = gdc.get_card_def(card_id)
        if card_def:
            costs.append(card_def.cost)
    if len(costs) == 0:
        return 0
    return (sum(costs) * 1.0) / len(costs)


def get_ability_counts(card_ids: list[str], gdc: GameDataCache):
    counts = {}
    for card_id in card_ids:
        card_def = gdc.get_card_def(card_id)
        if card_def:
            for ability in card_def.abilities:
                if not ability in counts:
                    counts[ability] = 0
                counts[ability] = counts[ability] + 1
    return counts


def get_power_counts(card_ids: list['string'], gdc: GameDataCache):
    counts = {}
    for card_id in card_ids:
        card_def = gdc.get_card_def(card_id)
        if card_def:
            power = card_def.power
            if not power in counts:
                counts[power] = 0
            counts[power] = counts[power] + 1
    return counts


def get_cost_counts(card_ids: list[str], gdc: GameDataCache):
    counts = {}
    for card_id in card_ids:
        card_def = gdc.get_card_def(card_id)
        if card_def:
            cost = card_def.cost
            if not cost in counts:
                counts[cost] = 0
            counts[cost] = counts[cost] + 1
    return counts


def get_series_counts(card_ids: list[str], gdc: GameDataCache):
    counts = {}
    for card_id in card_ids:
        card_def = gdc.get_card_def(card_id)
        if card_def:
            series = card_def.series_def_key
            if not series in counts:
                counts[series] = 0
            counts[series] = counts[series] + 1
    return counts


def categorize_elastic_search_deck(deck: MatchPlayerRecord, gdc: GameDataCache):
    card_ids = []
    if deck:
        for card in deck.deck_cards:
            card_ids.append(card.card_def_id)

    return categorize_deck_inner(card_ids, gdc)


def categorize_sql_deck(deck, gdc: GameDataCache):
    card_ids = []
    if deck:
        for card in deck.deck_cards.all():
            card_ids.append(card.key)
    return categorize_deck_inner(card_ids, gdc)


def categorize_card_list(cards: list[str], gdc: GameDataCache):
    return categorize_deck_inner(cards, gdc)


def categorize_game_deck(deck: 'Deck', gdc: GameDataCache):
    card_ids = []
    if deck:
        for card in deck.cards:
            card_ids.append(card.card_def_id)
    return categorize_deck_inner(card_ids, gdc)


def categorize_elastic_search_deck_pool(deck: MatchPlayerRecord, gdc: GameDataCache):
    card_ids = []
    if deck:
        for card in deck.deck_cards:
            card_ids.append(card.card_def_id)

    return categorize_deck_pool_inner(card_ids, gdc)


def categorize_sql_deck_pool(deck, gdc: GameDataCache):
    card_ids = []
    if deck:
        for card in deck.deck_cards.all():
            card_ids.append(card.key)
    return categorize_deck_pool_inner(card_ids, gdc)


def categorize_game_deck_pool(deck: 'Deck', gdc: GameDataCache):
    card_ids = []
    if deck:
        for card in deck.cards:
            card_ids.append(card.card_def_id)
    return categorize_deck_pool_inner(card_ids, gdc)


def categorize_deck_pool_inner(cards: list[str], gdc: GameDataCache):
    series_counts = get_series_counts(cards, gdc)
    if CardSeriesDefEnum.SERIES5.value in series_counts:
        return CardSeriesDefEnum.SERIES5.value
    if CardSeriesDefEnum.SERIES5.value in series_counts:
        return CardSeriesDefEnum.SERIES4.value
    if CardSeriesDefEnum.SERIES3.value in series_counts:
        return CardSeriesDefEnum.SERIES3.value
    elif CardSeriesDefEnum.SERIES2.value in series_counts:
        return CardSeriesDefEnum.SERIES2.value
    else:
        return CardSeriesDefEnum.SERIES1.value

def categorize_deck_12_12_inner(cards: list[str], gdc: GameDataCache):
    ability_counts = get_ability_counts(cards, gdc)
    series_counts = get_series_counts(cards, gdc)
    power_counts = get_power_counts(cards, gdc)
    cost_counts = get_cost_counts(cards, gdc)
    average_cost = get_average_cost(cards, gdc)
    has_series_3 = CardSeriesDefEnum.SERIES3.value in series_counts
    has_series_2 = CardSeriesDefEnum.SERIES2.value in series_counts
    control_counts = 0
    for card_id in ['Killmonger','ShangChi','ShadowKing','Enchantress','Rogue']:
        if card_id in cards:
            control_counts = control_counts + 1
    has_stones = 'MindStone' in cards or 'SoulStone' in cards or 'PowerStone' in cards or 'TimeStone' in cards or 'SpaceStone' in cards  or 'RealityStone' in cards
    if 'IronMan' in cards and 'Hawkeye' in cards and 'Hulk' in cards and has_series_2 and not has_series_3:
        return 'Avengers Roleplay'
    if 'Starlord' in cards and 'Gamora' in cards and ('Groot' in cards or 'RocketRaccoon' in cards) and not has_series_2 and not has_series_3:
        return 'Guardians Roleplay'
    if 'AgathaHarkness' in cards and 'Wave' in cards and 'LadySif' in cards:
        return 'Real Agatha'
    if 'AgathaHarkness' in cards:
        return 'Agatha Farm'
    if 'Arishem' in cards and 'Loki' in cards:
        return 'Arishem Loki'
    if 'Arishem' in cards:
        return 'Arishem'
    if 'Legion' in cards and 'Storm' in cards:
        return 'Legion Control'
    if 'Ronan' in cards and 'MasterMold' in cards:
        return 'Master Mold Ronan'
    if 'Sera' in cards and 'SilverSurfer' in cards and 'MrNegative' in cards and 'Bast' in cards:
        return 'Bast Seratonin'
    if 'Sera' in cards and 'MrNegative' in cards:
        return 'Seratonin'
    if 'SilverSurfer' in cards and 'MrNegative' in cards and 'Bast' in cards:
        return 'Negative Bast'
    if 'Zabu' in cards and 'Darkhawk' in cards:
        return 'Zabu Darkhawk'
    if 'Zabu' in cards and 'ShangChi' in cards and 'Enchantress' in cards:
        return 'Zabu Control'
    if 'HighEvolutionary' in cards and ('Storm' in cards or 'SpiderMan' in cards):
        return 'High Evo Control'
    if 'HighEvolutionary' in cards and 'SheHulk' in cards and 'Infinaut' in cards:
        return 'High Evo'
    if 'HighEvolutionary' in cards:
        return 'High Evo'
    if 'ThePhoenixForce' in cards:
        return 'Phoenix Clone'
    if ('Thanos' in cards or has_stones) and 'Lockjaw' in cards:
        return 'Thanos Lockjaw'
    if ('Thanos' in cards or has_stones) and ('Beast' in cards or 'Falcon' in cards):
        return 'Thanos Bounce'
    if ('Thanos' in cards or has_stones) and ('Carnage' in cards or 'Killmonger' in cards):
        return 'Thanos Destroy'
    if ('Thanos' in cards or has_stones) and 'Spectrum' in cards:
        return 'Thanos Spectrum'
    if ('Thanos' in cards or has_stones) and 'ProfessorX' in cards:
        return 'Thanos Lockdown'
    if ('Thanos' in cards or has_stones) and 'KaZar' in cards:
        return 'Thanos Zoo'
    if ('Thanos' in cards or has_stones):
        return 'Thanos'
    if ('Sera' in cards and 'HitMonkey' in cards):
        return 'HitMonkey Sera'
    if ('KaZar' in cards and 'HitMonkey' in cards):
        return 'HitMonkey Zoo'
    if 'Sera' in cards and 'SilverSurfer' in cards:
        return 'Sera Surfer'
    if 'Sera' in cards and ('Dracula' in cards or 'StrongGuy' in cards):
        return 'Sera Discard'
    if 'Sera' in cards and control_counts >= 3:
        return 'Sera Control'
    if 'Cerebro' in cards and 'Mystique' in cards and 7 in power_counts and power_counts[7] >= 2:
        return 'Cerebro-7'
    if 'Cerebro' in cards and 'Mystique' in cards and 6 in power_counts and power_counts[6] >= 2:
        return 'Cere6ro'
    if 'Cerebro' in cards and 5 in power_counts and power_counts[5] >= 2:
        return 'Cerebro-5'
    if 'Cerebro' in cards and 'Mystique' in cards and 4 in power_counts and power_counts[4] >= 2:
        return 'Cerebro-4'
    if 'Cerebro' in cards and 'Mystique' in cards and 3 in power_counts and power_counts[3] >= 2:
        return 'Cerebro-3'
    if 'Cerebro' in cards and 'Mystique' in cards and 2 in power_counts and power_counts[2] >= 2:
        return 'Cerebro-2'
    if 'Cerebro' in cards and 'Mystique' in cards and 0 in power_counts and power_counts[0] >= 4:
        return 'Cerebr0'
    if 'Cerebro' in cards:
        return 'Generic Cerebro'
    if 'SheHulk' in cards and 'Infinaut' in cards:
        return 'Shenaut'
    if 'Patriot' in cards and 'IronLad' in cards:
        return 'Patriot Lad'
    if 'Patriot' in cards and 'Mystique' in cards and 'Ultron' in cards and 'KaZar' in cards and ('Debrii' in cards or 'GreenGoblin' in cards):
        return 'Disruptron'
    if 'Loki' in cards and 'Beast' in cards:
        return 'Loki Bounce'
    if 'Loki' in cards:
        return 'Loki'
    if ('Death' in cards or 'Knull' in cards) and 'Galactus' in cards:
        return 'Destroy Galactus'
    if 'MrNegative' in cards and 'Galactus' in cards:
        return 'Negative Galactus'
    if 'Nimrod' in cards and 'Galactus' in cards:
        return 'Nimrod Galactus'
    has_destroyer = 'Destroyer' in cards
    if has_destroyer and 'Nimrod' in cards:
        return 'Nimrod Destroyer'
    if 'ProfessorX' in cards and 'Storm' in cards:
        return 'Lockdown'
    if has_destroyer and 'Electro' in cards:
        return 'Electroyer'
    if 'Spectrum' in cards and 'Destroyer' in cards:
        return 'SpectrumDestroyer'
    if 'Daredevil' in cards and 'Destroyer' in cards:
        return 'DDDestroyer'
    if 'Venom' in cards and ('Taskmaster' in cards or 'ArnimZola' in cards):
        return 'Big Venom'
    if 'Shuri' in cards and ('ArnimZola' in cards or 'Taskmaster' in cards):
        return 'Shuri Clone'
    if 'Zero' in cards and ('RedSkull' in cards and 'TyphoidMary' in cards or 'Lizard' in cards):
        return 'Zero'
    if 'Destroyer' in cards:
        return 'Generic Destroyer'
    if 'DevilDinosaur' in cards and 'Daredevil' in cards:
        return 'DDDino'
    if 'DevilDinosaur' in cards and 'BuckyBarnes' in cards:
        return 'Death Dino'
    if 'DevilDinosaur' in cards and 'Storm' in cards:
        return 'Storm Dino'
    if 'Wong' in cards and 'DrDoom' in cards and 'Odin' in cards:
        return 'Woding'
    if 'BlackPanther' in cards and ('ArnimZola' in cards or 'Taskmaster' in cards) and ('Wong' in cards or 'Shuri' in cards):
        return 'Big Panther'
    if 'Mystique' in cards and 'Tribunal' in cards and 'IronMan' in cards and 'Onslaught' in cards:
        return 'All-In Tribunal'
    if 'Hela' in cards and 'Tribunal' in cards:
        return 'Hela Tribunal'
    if 'Hela' in cards and 'InvisibleWoman' in cards:
        return 'Invis Hela'
    if 'Killmonger' in cards and 'ShangChi' in cards and 'Enchantress' in cards:
        return 'Control'
    has_beast_falcon = 'Beast' in cards and 'Falcon' in cards
    if has_beast_falcon and 'KittyPryde' in cards:
        return 'Kitty Bounce'
    if has_beast_falcon:
        return 'Bounce'
    if 'SilverSurfer' in cards and 3 in cost_counts and cost_counts[3] >= 4:
        return 'Surfer'
    if 'DevilDinosaur' in cards and 'MoonGirl' in cards:
        return 'Big Hand'
    if 'Lockjaw' in cards and 'JaneFoster' in cards:
        return 'Janejaw'
    if 'Dracula' in cards and 'Apocalypse' in cards:
        return 'Dracula'
    if 'Heimdall' in cards and ('Vulture' in cards or 'HumanTorch' in cards or 'Kraven' in cards or 'MultipleMan' in cards):
        return 'Movement'
    if 'GreenGoblin' in cards and 'Debrii' in cards and 'Viper' in cards and ('Hood' in cards or 'BlackWidow' in cards):
        return 'Junk'
    if 'KaZar' in cards and not 'Spectrum' in cards:
        return 'KaZoo'
    if 'LukeCage' in cards and 'Hazmat' in cards:
        return 'KageMat'
    if 'Lockjaw' in cards and 'Morbius' in cards and 'Apocalypse' in cards:
        return 'DiscardJaw'
    if 'Daredevil' in cards and 'ProfessorX' in cards and ('Gamora' in cards or 'Hobgoblin' in cards or 'SpiderMan' in cards):
        return 'DDScam'
    if 'Lockjaw' in cards and 'On Reveal' in ability_counts and ability_counts['On Reveal'] >= 2:
        return 'Lockjaw On Reveal'
    if 'Odin' in cards and 'On Reveal' in ability_counts and ability_counts['On Reveal'] >= 3 and not has_series_3:
        return 'Odin Reveal'
    if 'Odin' in cards and 'On Reveal' in ability_counts and ability_counts['On Reveal'] >= 2 and not has_series_3 and not has_series_2:
        return 'Odin Reveal'
    if 'BuckyBarnes' in cards and ('Carnage' in cards or 'Deathlok' in cards or 'Venom' in cards):
        return 'Generic Self Destroy'
    has_patriot = 'Patriot' in cards
    advanced_patriot_cards = ['SquirrelGirl','Doom','Debrii','Mysterio','Ultron']
    patriot_advanced_count = 0
    for card in advanced_patriot_cards:
        if card in cards:
            patriot_advanced_count = patriot_advanced_count + 1
    if has_patriot and patriot_advanced_count >= 2:
        return 'Advanced Patriot'
    if has_patriot and 'No Ability' in ability_counts and ability_counts['No Ability'] >= 2:
        return 'Generic Patriot'
    if 'Zabu' in cards:
        return 'Generic Zabu'
    if 'Galactus' in cards:
        return 'Generic Galactus'
    if 'MrNegative' in cards:
        return 'Generic Negative'
    if 'Tribunal' in cards:
        return 'Generic Tribunal'
    if 'Wave' in cards and ('Magneto' in cards or 'Hulk' in cards or 'DrDoom' in cards):
        return 'Wave Ramp'
    if 'Discard' in ability_counts and ability_counts['Discard'] >= 3:
        return 'Generic Discard'

    return 'Uncategorized'


def categorize_deck_inner(cards: list[str], gdc: GameDataCache):
    return categorize_deck_12_12_inner(cards, gdc)

