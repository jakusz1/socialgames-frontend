from pytrends.request import TrendReq
from faker import Faker

pytrends = TrendReq(hl='US', tz=0)
pytrends.build_payload(['jhdksajfkjsdah', '628374687ysadfgiwq'], cat=0, timeframe='today 3-m', geo='US', gprop='')
scrapped_df = pytrends.interest_over_time()
print(scrapped_df)
print(scrapped_df.to_json(orient='records'))