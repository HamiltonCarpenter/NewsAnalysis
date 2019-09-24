import urllib3
import re
import browsercookie
from bs4 import BeautifulSoup
import bs4
import datetime
from time import sleep
import requests 
import mysql.connector
import os
import time
import random
from urllib3.exceptions import MaxRetryError
#import constant urllib3.exceptions.MaxRetryError()

#TODO: combine constants in class 
#constants:
NewYorkTimes = "NewYorkTimes"
WashingtonPost = "WashingtonPost"
politics = "Politics"
raw = "Raw"
clean = "Clean"
standard_clean_directory = "standard_clean_directory"
standard_raw_directory = "standard_raw_directory"

outlets = {NewYorkTimes:{politics:"https://www.nytimes.com/politics"},WashingtonPost:{politics:"https://www.washingtonpost.com/politics/"}}
    #make dict for sections and their unique identifiers 
identifiers = {NewYorkTimes:{politics:"politics"},WashingtonPost:{politics:"politics"}}

#NYT has urls relative to the site's root. This function converts them to absolute addresses that python requests can access
def construct_full_url(scraped_url, outlet):
    u = scraped_url
    if outlet == "NewYorkTimes":
        u = 'https://www.nytimes.com'+ u
    return u

#converts date from db string format to object
def convert_m_d_y_to_date_object(mdy_string):
    list_date = mdy_string.split('/')
    year = list_date[2]
    month = list_date[0]
    day = list_date[1]
    obj_date = datetime.date(int(year),int(month),int(day))
    return obj_date
    
#converts date from object to db string format    
def get_date_string(): 
    d = datetime.date.today()
    return(str(d.month)+'/'+str(d.day)+'/'+str(d.year))


