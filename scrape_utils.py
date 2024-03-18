import pandas as pd
import requests
from playwright.sync_api import sync_playwright
import os


stat_id_to_stat_mappings = {'24': 'Total Turnovers', '31': '3 Pointers Made', '22': 'Total Rebounds', '243': 'Points and Rebounds', '19': 'Points Scored', '244': 'Points and Assists', '21': 'Total Blocks', '20': 'Total Assists', '245': 'Rebounds and Assists', '23': 'Total Steals', '106': 'Total Points, Rebounds, and Assists', '105': 'Steals and Blocks'}
odds_to_emoji_mappings = {128: ' :neutral_face:', 130 : ':coin: :ok_hand:', 140 : ':moneybag: :cold_face:', 150 : ':money_mouth: :fire: :lock:', 'discount': ':four_leaf_clover:'}

def go_to_covers_page(page, old_player):
    page.goto('https://www.bing.com/')
    search_bar = page.wait_for_selector('#sb_form_q')
    search_bar.click()
    search_bar.type(f'{old_player} covers NBA')
    # print(old_player)
    search_bar.press("Enter")
    page.wait_for_load_state("networkidle")
    print(page)
    search_result_links = page.locator('text=Prop Bets, Odds, And Stats')
    links = search_result_links.all()
    # print(links)
    if(len(links) == 0):
        print("empty")
        print(old_player)
        print(links)
        return []
    links[0].click()
    try:
        page.wait_for_selector('.covers-CoversPlayer-Prop-Event')
    except:
        print("timed out waiting for cards")
        return []
    all_cards = page.query_selector_all('.covers-CoversPlayer-Prop-Event')
    return all_cards

def go_to_KCP(page):
    print('KCP is a bum')
    page.goto('https://www.covers.com/sport/basketball/nba/players/743/kentavious-caldwell-pope')
    try:
        page.wait_for_selector('.covers-CoversPlayer-Prop-Event')
    except:
        print("timed out waiting for cards")
        return []
    all_cards = page.query_selector_all('.covers-CoversPlayer-Prop-Event')
    return all_cards


def get_prize_picks_payload():
    so_api_key = os.getenv("SO_ACCESS_KEY")
    response = requests.get(
    url='https://proxy.scrapeops.io/v1/',
    params={
        'api_key': so_api_key,
        'url': 'https://api.prizepicks.com/projections', 
    },
    )
    return response

def parse_payload(response):
    if(response.status_code == 200):
        print(f'STATUS OK {response.status_code}')
        mappings = pd.json_normalize(response.json()['included'])
        all_projections = pd.json_normalize(response.json()['data'])

        only_nba_players = mappings[mappings['attributes.league'] == 'NBA']
        
        standard_lines = all_projections[all_projections['attributes.odds_type'] == 'standard']

        # filtering out some restarted stats no one bets on
        standard_lines = standard_lines[[int(id) < 300 for id in standard_lines['relationships.stat_type.data.id']]]
        standard_lines = standard_lines[[int(id) > 15 for id in standard_lines['relationships.stat_type.data.id']]]
        standard_lines = standard_lines[[int(id) != 68 for id in standard_lines['relationships.stat_type.data.id']]]

        nba_projected_lines = standard_lines[standard_lines['relationships.new_player.data.id'].isin(only_nba_players['id'].values)]

        id_to_name_mapping = {player['id']: player['attributes.display_name'] for index, player in only_nba_players.iterrows()}
        
        list_of_names = [id_to_name_mapping[id] for id in nba_projected_lines['relationships.new_player.data.id']]
        list_of_stats = [stat_id_to_stat_mappings[id] for id in nba_projected_lines['relationships.stat_type.data.id']]

        lines = nba_projected_lines.apply(lambda row: str(row['attributes.flash_sale_line_score']) if pd.notnull(row['attributes.flash_sale_line_score']) else str(row['attributes.line_score']), axis=1)

        df = pd.DataFrame(zip(list_of_names, list_of_stats, lines), columns=['name', 'stat', 'line'])
        print(len(df))
        print(df)
        return df
    else:
            print(f'STATUS ERROR {response.status_code}')

def find_good_lines(df):
    good_lines = []
    old_player = df.iloc[0]['name']
    with sync_playwright() as p:
        # print("launching browser")
        browser = p.chromium.launch(executable_path=os.getenv("CHROMIUM_EXECUTABLE_PATH"))
        page = browser.new_page()
        prop_cards = []
        if old_player == 'Kentavious Caldwell-Pope':
            prop_cards = go_to_KCP(page)
        else:
            prop_cards = go_to_covers_page(page, old_player)
        
        for index, projection in df.iterrows():
            # print(index)
            current_player = projection['name']
            current_line = float(projection['line'])
            current_stat = projection['stat']
            if old_player != current_player:
                # current player is now old player
                # need to change pages now.
                old_player = current_player
                if old_player == 'Kentavious Caldwell-Pope':
                    prop_cards = go_to_KCP(page)
                else:
                    prop_cards = go_to_covers_page(page, old_player)

            # can look for the stat on the page, print if its good line.
            for card in prop_cards:
                card_title = card.query_selector("h2").text_content()
                if current_stat in card_title:
                    odds = card.query_selector_all('.odds.upper-block')
                    over_odd = odds[0]
                    under_odd = odds[1]

                    over_line_and_odds = over_odd.text_content().split()
                    under_line_and_odds = under_odd.text_content().split()

                    over_line = float(over_line_and_odds[0][1:])
                    under_line = float(under_line_and_odds[0][1:])
                    over_odds = float(over_line_and_odds[1])
                    under_odds = float(under_line_and_odds[1])

                    
                    temp_line = evaluate_line(over_line, under_line, over_odds, under_odds, current_player, current_line, current_stat)
                    if len(temp_line) > 0:
                        good_lines.append(temp_line)
    print("sorting the good lines")
    sorted_lines = sorted(good_lines, key=lambda line: get_odds_from_line(line))
    return sorted_lines

def evaluate_line(over_line, under_line, over_odds, under_odds, current_player, current_line, current_stat):
    temp_line = ""
    emoji = ""
    
    if current_line <= over_line:
        if over_odds <= -128:
            emoji = odds_to_emoji_mappings[128]
            if over_odds <= -130:
                emoji = odds_to_emoji_mappings[130]
                if over_odds <= -140:
                    emoji = odds_to_emoji_mappings[140]
                    if over_odds <= -150:
                        emoji = odds_to_emoji_mappings[150]
            temp_line = f'{current_player} OVER :arrow_up_small: {current_line} {current_stat} {over_odds}  {emoji}'
        elif over_line - current_line >= 1.5 and over_odds < -100:
            emoji = odds_to_emoji_mappings['discount']
            temp_line = f'{current_player} OVER :arrow_up_small: {current_line} {current_stat} DISCOUNT Original line {over_line} {over_odds}  {emoji}'

    if current_line >= under_line:
        if under_odds <= -128:
            emoji = odds_to_emoji_mappings[128]
            if under_odds <= -130:
                emoji = odds_to_emoji_mappings[130]
                if under_odds <= -140:
                    emoji = odds_to_emoji_mappings[140]
                    if under_odds <= -150:
                        emoji = odds_to_emoji_mappings[150]
            temp_line = f'{current_player} UNDER :arrow_down_small: {current_line} {current_stat} {under_odds}  {emoji}'
        elif current_line - under_line >= 1.5 and under_odds < -100:
            emoji = odds_to_emoji_mappings['discount']
            temp_line = f'{current_player} UNDER :arrow_down_small: {current_line} {current_stat} DISCOUNT Original line {under_line} {under_odds}  {emoji}'
    if len(temp_line) > 0:
        print(temp_line)
    return temp_line

def get_odds_from_line(line):
    line_arr = line.split(' ')
    odds = 0
    for curr in reversed(line_arr):
        if(len(curr) == 0):
            continue
        if curr[0] == '-':
            odds = int(float(curr))
            # print(odds)
        elif curr == ':four_leaf_clover:':
            return -210
    return odds