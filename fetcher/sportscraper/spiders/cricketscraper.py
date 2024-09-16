from sportscraper.spiders.gamescraper import GamescraperSpider
from datetime import datetime
import json
class Cricketscrapper(GamescraperSpider):
    game_name = "cricket"
    name = game_name + "scraper"
    def __init__(self):
        
        super().__init__()
        self.set_name()
        
    def parse(self, response):
        # print("-"*100)
        
        games = response.css('.cscore_competitors')
        
        for game in games:
            try:
                team1_name = game.css('.cscore_name--long::text').get().strip()
                team2_name = game.css('.cscore_name--long::text').getall()[1].strip()
                score1 = "" if game.css('.cscore_score::text').get()==None else game.css('.cscore_score::text').get().strip()
                score2 = "" if game.css('.cscore_score::text').get()==None else game.css('.cscore_score::text').getall()[1].strip()

                self.send_data(team1_name, team2_name, score1, score2)
            except:
                pass
            
    def set_name(self):
        self.start_urls = [f"https://www.espn.in/{self.game_name}/scores"+"/_/date/"+datetime.now().strftime('%Y%m%d')]
        