from pymongo import MongoClient, DESCENDING, ASCENDING
from bs4 import BeautifulSoup
import requests
from Data import Data
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import datetime
import random


class ReviewDB(Data):

    def __init__(self, *args, **kwargs):
        super(Data, self).__init__(*args, **kwargs)
        self.client_name = "ReviewDB"
        self.db_url = 'mongodb://localhost:27017'

    def bgu_data(self):

        # Launch a new Chrome browser
        driver = webdriver.Chrome()

        # Navigate to the page with the links
        driver.get('https://www.thestudent.co.il/school91_%d7%90%d7%95%d7%a0%d7%99%d7%91%d7%a8%d7%a1%d7%99%d7%98%d7%aa_%d7%91%d7%9f_%d7%92%d7%95%d7%a8%d7%99%d7%95%d7%9f')

        # Find all <a> elements on the page
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Define a regular expression to match the desired format
        pattern = re.compile(r'https://www\.thestudent\.co\.il/Degrees/Degree_\d+\.html')

        # Loop through each link and click on it if it matches the desired format
        for link in links:
            href = link.get_attribute('href')
            if not (href is None):
                print(href)
                if pattern.match(href):
                    driver.get(href)
                    break

    def update_all(self):
        self.bgu_data()

x = ReviewDB()
x.update_all()