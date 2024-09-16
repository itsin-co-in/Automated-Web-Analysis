import scrapy
from datetime import datetime
from scrapy.http import FormRequest
import json 
import requests
import re

class GamescraperSpider(scrapy.Spider):
    game_name = "game"
    name = game_name + "scraper"
    allowed_domains = ["www.espn.in"]
    start_urls = [f"https://www.espn.in/{game_name}/scoreboard"+"/_/date/"+datetime.now().strftime('%Y%m%d')]

    def parse(self, response):
        # print("-"*100)
        games = response.css('.ScoreboardScoreCell')
        for game in games:
            try:
                
                team1_name = game.css('.ScoreCell__TeamName::text').get().strip()
                team2_name = game.css('.ScoreCell__TeamName::text').getall()[1].strip()
                score1 = "" if game.css('.ScoreCell__Score::text').get()==None else game.css('.ScoreCell__Score::text').get().strip()
                score2 = "" if game.css('.ScoreCell__Score::text').get()==None else game.css('.ScoreCell__Score::text').getall()[1].strip()

                self.send_data(team1_name, team2_name, score1, score2)
            except:
                pass
    def send_data(self, team1_name, team2_name, score1, score2):
        data = {
                "game": str(self.get_game()),
                'team1': ''.join([i for i in team1_name if i.isalpha()]),
                'team2': ''.join([i for i in team2_name if i.isalpha()]),
                'score1': str(score1),
                'score2': str(score2)
            }
        # self.print_data(data)
        url = 'http://localhost:8080/games/matches'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        self.handle_post_response(response)
            
            # yield data
    def get_game(self):
        return self.game_name
    def handle_post_response(self, response):
        print(response)# Handle the response
        
    def print_data(self, data):
        print("_______________------------------------_____________________________\n", data)
            