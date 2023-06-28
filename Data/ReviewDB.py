from pymongo import MongoClient, DESCENDING, ASCENDING
from bs4 import BeautifulSoup
import requests
from Data import Data
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import csv
import os
import datetime
import random


class ReviewDB(Data):

    def __init__(self, *args, **kwargs):
        super(Data, self).__init__(*args, **kwargs)
        self.client_name = "ReviewDB"
        self.db_url = 'mongodb://localhost:27017'


    def collect_data(self, url, school_num, institute):

        # Launch a new Chrome browser
        driver = webdriver.Chrome()

        # Navigate to the page with the links
        driver.get(url)

        # Find all <a> elements on the page
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Define a regular expression to match the desired format
        pattern = re.compile(r'https://www\.thestudent\.co\.il/Degrees/Degree_\d+\.html')

        # Loop through each link and click on it if it matches the desired format
        desired_link = ''
        for link in links:
            href = link.get_attribute('href')
            if href and f'{school_num}-d:0-dt:1' in href:
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

        self.write_to_csv(links_dict, institute)

    def write_to_csv(self, links_dict, institute):
        file_exists = os.path.isfile('reviews.csv')

        with open('reviews.csv', 'a', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['institute', 'field', 'why', 'expectations', 'level', 'advice', 'rating_value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            for title, href in links_dict.items():
                url = "https://www.thestudent.co.il" + href
                response = requests.get(url)

                if response.status_code == 200:
                    html = response.text
                    soup = BeautifulSoup(html, 'html.parser')

                    institute = institute
                    field = title

                    reviews = soup.select('.Review')
                    for review in reviews:
                        content = review.select('.Info .M-OUT')
                        why = content[0].text
                        expectations = content[1].text
                        level = content[2].text
                        advice = content[3].text

                        try:
                            rating_element = review.select_one('.Grades div[itemprop="ratingValue"]')
                            rate = rating_element.text.strip()
                        except AttributeError:
                            rate = ""

                        writer.writerow({
                            'institute': institute,
                            'field': field,
                            'why': why,
                            'expectations': expectations,
                            'level': level,
                            'advice': advice,
                            'rating_value': rate
                        })

                    print(f"All reviews for '{title}' have been written to the CSV file.")
                else:
                    print(f"Failed to retrieve data for '{title}'.")

    def update_all(self):
        if os.path.exists('reviews.csv'):
            os.remove('reviews.csv')

        self.collect_data('https://www.thestudent.co.il/school91_%d7%90%d7%95%d7%a0%d7%99%d7%91%d7%a8%d7%a1%d7%99%d7%98%d7%aa_%d7%91%d7%9f_%d7%92%d7%95%d7%a8%d7%99%d7%95%d7%9f',
                          "school91", 'בן גוריון')
        self.collect_data(
            'https://www.thestudent.co.il/school93_%d7%94%d7%90%d7%95%d7%a0%d7%99%d7%91%d7%a8%d7%a1%d7%99%d7%98%d7%94_%d7%94%d7%a2%d7%91%d7%a8%d7%99%d7%aa',
                          "school93", 'העברית')
        self.collect_data(
            'https://www.thestudent.co.il/school90_%d7%90%d7%95%d7%a0%d7%99%d7%91%d7%a8%d7%a1%d7%99%d7%98%d7%aa_%d7%aa%d7%9c_%d7%90%d7%91%d7%99%d7%91',
            "school90", 'אוניברסיטת תל אביב')
        self.collect_data(
            'https://www.thestudent.co.il/school94_%d7%94%d7%98%d7%9b%d7%a0%d7%99%d7%95%d7%9f',
            "school94", 'הטכניון')
        self.collect_data(
            'https://www.thestudent.co.il/school102_%d7%a1%d7%9e%d7%99_%d7%a9%d7%9e%d7%a2%d7%95%d7%9f',
            "school102", 'סמי שמעון')
        self.collect_data(
            'https://www.thestudent.co.il/school69_%d7%90%d7%95%d7%a0%d7%99%d7%91%d7%a8%d7%a1%d7%99%d7%98%d7%aa_%d7%90%d7%a8%d7%99%d7%90%d7%9c',
            "school69", 'אריאל')
        self.collect_data(
            'https://www.thestudent.co.il/school106_%d7%90%d7%95%d7%a0%d7%99%d7%91%d7%a8%d7%a1%d7%99%d7%98%d7%aa_%d7%91%d7%a8_%d7%90%d7%99%d7%9c%d7%9f',
            "school106", 'בר אילן')
        self.collect_data(
            'https://www.thestudent.co.il/school83_%d7%94%d7%90%d7%95%d7%a0%d7%99%d7%91%d7%a8%d7%a1%d7%99%d7%98%d7%94_%d7%94%d7%a4%d7%aa%d7%95%d7%97%d7%94',
            "school83", 'הפתוחה')
        self.collect_data(
            'https://www.thestudent.co.il/school72_%d7%94%d7%9e%d7%a8%d7%9b%d7%96_%d7%94%d7%91%d7%99%d7%a0%d7%aa%d7%97%d7%95%d7%9e%d7%99',
            "school72", 'המרכז הבינתחומי')
        self.collect_data(
            'https://www.thestudent.co.il/school194_%d7%9e%d7%9b%d7%9c%d7%9c%d7%aa_%d7%90%d7%a4%d7%a7%d7%94',
            "school194", 'אפקה')
        self.collect_data(
            'https://www.thestudent.co.il/school200_%d7%91%d7%a6%d7%9c%d7%90%d7%9c',
            "school200", 'בצלאל')
        self.collect_data(
            'https://www.thestudent.co.il/school87_%d7%9e%d7%9b%d7%9c%d7%9c%d7%aa_%d7%90%d7%a9%d7%a7%d7%9c%d7%95%d7%9f',
            "school87", 'מכללת אשקלון')
        self.collect_data(
            'https://www.thestudent.co.il/school87_%d7%9e%d7%9b%d7%9c%d7%9c%d7%aa_%d7%90%d7%a9%d7%a7%d7%9c%d7%95%d7%9f',
            "school87", 'מכללת אשקלון')
        self.collect_data(
            'https://www.thestudent.co.il/school79_%d7%9e%d7%9b%d7%9c%d7%9c%d7%aa_%d7%a1%d7%a4%d7%99%d7%a8',
            "school79", 'ספיר')
        self.collect_data(
            'https://www.thestudent.co.il/school66_%d7%94%d7%a7%d7%a8%d7%99%d7%94_%d7%94%d7%90%d7%a7%d7%93%d7%9e%d7%99%d7%aa_%d7%90%d7%95%d7%a0%d7%95',
            "school66", 'אונו')


x = ReviewDB()
x.update_all()