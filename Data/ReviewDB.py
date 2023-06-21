from pymongo import MongoClient, DESCENDING, ASCENDING
from bs4 import BeautifulSoup
import requests
from Data import Data
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import csv
import datetime
import random


class ReviewDB(Data):

    def __init__(self, *args, **kwargs):
        super(Data, self).__init__(*args, **kwargs)
        self.client_name = "ReviewDB"
        self.db_url = 'mongodb://localhost:27017'

    def EVR_data(self):

        # Launch a new Chrome browser
        driver = webdriver.Chrome()

        # Navigate to the page with the links
        driver.get('https://www.thestudent.co.il/school93_%d7%94%d7%90%d7%95%d7%a0%d7%99%d7%91%d7%a8%d7%a1%d7%99%d7%98%d7%94_%d7%94%d7%a2%d7%91%d7%a8%d7%99%d7%aa')

        # Find all <a> elements on the page
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Define a regular expression to match the desired format
        pattern = re.compile(r'https://www\.thestudent\.co\.il/Degrees/Degree_\d+\.html')

        # Loop through each link and click on it if it matches the desired format
        desired_link = ''
        for link in links:
            href = link.get_attribute('href')
            if href and 'school93-d:0-dt:1' in href:
                desired_link = href

        driver.get(desired_link)
        rElement = driver.find_element(By.CSS_SELECTOR,
            ".CatRight")
        lElement = driver.find_element(By.CSS_SELECTOR,
            ".CatLeft")  # Replace with the appropriate selector for your lElement

        # Get the HTML content of the lElement
        lHtml_content = lElement.get_attribute("innerHTML")
        rHtml_content = rElement.get_attribute("innerHTML")

        rSoup = BeautifulSoup(rHtml_content, 'html.parser')
        lSoup = BeautifulSoup(lHtml_content, 'html.parser')

        # Extract the desired values
        data = {}

        # Extract numeric values using regular expressions
        rating_count = lSoup.find(itemprop="ratingCount").text
        data['ביקורות של סטודנטים ובוגרים'] = int(rating_count)
        data['מסלולי לימוד'] = int(lSoup.find(itemprop="ratingCount").find_next_sibling("span").text)

        response_percentages = lSoup.find_all(class_="Data")
        response_values = [re.search(r'\d+', resp.text).group() for resp in response_percentages]
        response_labels = ['ענה בצורה מלאה', 'ענה בצורה חלקית', 'לא ענה על הציפיות', 'לא ממליץ לאחרים']
        data.update(dict(zip(response_labels, map(int, response_values))))

        employment_percentage = lSoup.find(class_="BarOut").div.text.strip('%')
        data['הבוגרים המועסקים בתחומם'] = int(employment_percentage)

        study_level = lSoup.find('span', style="direction:rtl").text.strip('()')
        data['רמת הלימודים'] = study_level

        overall_rating = lSoup.find(itemprop="ratingValue").text
        data['דירוג כללי'] = float(overall_rating)

        # Print the dictionary
        print(data)

        links = rSoup.select('div.Middle')
        result = {}

        for link in links:
            title_element = link.select_one('div.Title a')
            if title_element is not None:
                title = title_element.text[6:-11].strip()
                href = title_element.get('href')
                result[title] = href

        print(result)

    def BGU_data(self):

        # Launch a new Chrome browser
        driver = webdriver.Chrome()

        # Navigate to the page with the links
        driver.get('https://www.thestudent.co.il/school91_%d7%90%d7%95%d7%a0%d7%99%d7%91%d7%a8%d7%a1%d7%99%d7%98%d7%aa_%d7%91%d7%9f_%d7%92%d7%95%d7%a8%d7%99%d7%95%d7%9f')

        # Find all <a> elements on the page
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Define a regular expression to match the desired format
        pattern = re.compile(r'https://www\.thestudent\.co\.il/Degrees/Degree_\d+\.html')

        # Loop through each link and click on it if it matches the desired format
        desired_link = ''
        for link in links:
            href = link.get_attribute('href')
            if href and 'school91-d:0-dt:1' in href:
                desired_link = href

        driver.get(desired_link)
        rElement = driver.find_element(By.CSS_SELECTOR,
            ".CatRight")
        lElement = driver.find_element(By.CSS_SELECTOR,
            ".CatLeft")  # Replace with the appropriate selector for your lElement

        # Get the HTML content of the lElement
        lHtml_content = lElement.get_attribute("innerHTML")
        rHtml_content = rElement.get_attribute("innerHTML")

        rSoup = BeautifulSoup(rHtml_content, 'html.parser')
        lSoup = BeautifulSoup(lHtml_content, 'html.parser')

        # Extract the desired values
        data = {}

        # Extract numeric values using regular expressions
        rating_count = lSoup.find(itemprop="ratingCount").text
        data['ביקורות של סטודנטים ובוגרים'] = int(rating_count)
        data['מסלולי לימוד'] = int(lSoup.find(itemprop="ratingCount").find_next_sibling("span").text)

        response_percentages = lSoup.find_all(class_="Data")
        response_values = [re.search(r'\d+', resp.text).group() for resp in response_percentages]
        response_labels = ['ענה בצורה מלאה', 'ענה בצורה חלקית', 'לא ענה על הציפיות', 'לא ממליץ לאחרים']
        data.update(dict(zip(response_labels, map(int, response_values))))

        employment_percentage = lSoup.find(class_="BarOut").div.text.strip('%')
        data['הבוגרים המועסקים בתחומם'] = int(employment_percentage)

        study_level = lSoup.find('span', style="direction:rtl").text.strip('()')
        data['רמת הלימודים'] = study_level

        overall_rating = lSoup.find(itemprop="ratingValue").text
        data['דירוג כללי'] = float(overall_rating)

        # Print the dictionary
        print(data)

        links = rSoup.select('div.Middle')
        links_dict = {}

        for link in links:
            title_element = link.select_one('div.Title a')
            if title_element is not None:
                title = title_element.text[6:-11].strip()
                href = title_element.get('href')
                links_dict[title] = href

        for title, href in links_dict.items():
            url = "https://www.thestudent.co.il" + href
            response = requests.get(url)

            if response.status_code == 200:
                html = response.text
                # Process the HTML as per your requirements
                print(f"HTML for '{title}': {html}")
            else:
                print(f"Failed to retrieve HTML for '{title}'")

    def update_all(self):
        self.BGU_data()

x = ReviewDB()
x.update_all()