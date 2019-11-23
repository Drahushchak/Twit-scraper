from main import Twit_Scraper
import json

twit_scraper = Twit_Scraper()
distribution = twit_scraper.get_freq_dist('#зе', 'зе')
with open('data.json', 'w', indent=4, encoding='utf-8') as f:
    json.dump(distribution, f, ensure_ascii=False)