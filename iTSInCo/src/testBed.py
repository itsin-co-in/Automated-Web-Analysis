import pandas as pd
from lighthouse import LighthouseRunner

# Set up LighthouseRunner with desired options
runner = LighthouseRunner('https://opstree.com', form_factor='desktop', quiet=False)

# Loop through list of URLs and run Lighthouse
urls = ['https://www.mygurukulam.co', 'https://opstree.com']
for url in urls:
    report = runner.run(url)
    # Store high-level ratings in dataframe
    df = pd.DataFrame({'url': [url], 'score': [report.score['performance']]})