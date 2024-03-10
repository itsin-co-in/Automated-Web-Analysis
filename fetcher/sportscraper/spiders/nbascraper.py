import scrapy
from datetime import datetime
from scrapy.http import FormRequest
import json 
import requests

class NbascraperSpider(scrapy.Spider):
    name = "nbascraper"
    allowed_domains = ["www.espn.in"]
    start_urls = ["https://www.espn.in/nba/scoreboard"+"/_/date/"+datetime.now().strftime('%Y%m%d')]


    def parse(self, response):
        # print("-"*100)
        games = response.css('.ScoreboardScoreCell')
        for game in games:

            team1_name = game.css('.ScoreCell__TeamName::text').get().strip()
            team2_name = game.css('.ScoreCell__TeamName::text').getall()[1].strip()
            score1 = "" if game.css('.ScoreCell__Score::text').get()==None else game.css('.ScoreCell__Score::text').get().strip()
            score2 = "" if game.css('.ScoreCell__Score::text').get()==None else game.css('.ScoreCell__Score::text').getall()[1].strip()

            data = {
                'team1': str(team1_name),
                'team2': str(team2_name),
                'score1': str(score1),
                'score2': str(score2)
            }
            url = 'http://localhost:8080/nba/matches'
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers)
            self.handle_post_response(response)
            
            # yield data
            
    def handle_post_response(self, response):
        print(response)# Handle the response
            