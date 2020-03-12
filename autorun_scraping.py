from database_interactions import *  
#%run 'Scraping_RAWtext.ipynb'
from scraping_interactions import *
from misc_helper_funcs_and_constants import *

db = DatabaseManager()

nyt_urls_temp = scrape_section_for_urls(NewYorkTimes,politics,outlets)
db.write_urls_to_db(nyt_urls_temp, NewYorkTimes, politics, get_date_string())
wapo_urls_temp = scrape_section_for_urls(WashingtonPost,politics,outlets)
db.write_urls_to_db(wapo_urls_temp, WashingtonPost, politics, get_date_string())

