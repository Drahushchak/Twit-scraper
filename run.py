from twit_scrap import Twit_Scraper
import json

twit_scraper = Twit_Scraper()
distribution = twit_scraper.get_freq_dist('#зе', 'зе')
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(distribution, f, indent=4, ensure_ascii=False)