from pymongo import MongoClient
from bs4 import BeautifulSoup
import requests
from .Admission import Admission
import datetime

class Data:

    def __init__(self, *args, **kwargs):
        super(Data, self).__init__(*args, **kwargs)

    def compare_dicts(self, dict1, dict2):
        for key in dict1:
            if key == '_id' or 'date' or (dict1[key] is None and dict2[key] is None):
                continue
            elif dict1[key] != dict2[key]:
                return False
        return True

    def convert_to_num(self, str_number):
        if str_number.strip() == '':
            return None
        else:
            try:
                return int(str_number.strip())
            except:
                return float(str_number.strip())

    def get_all_professions(self):
        client = MongoClient('mongodb://localhost:27017')

        # get a list of all the collection names
        collection_names = client['mydatabase'].list_collection_names()

        all_professions = []

        # iterate over each collection and get the distinct values for the name key
        for collection_name in collection_names:
            collection = client['mydatabase'][collection_name]
            names = collection.distinct('name')
            all_professions.extend(names)
        return all_professions

    def get_all_data(self, names):
        client = MongoClient('mongodb://localhost:27017')

        # initialize a list to hold all the matching documents
        matching_docs = {}

        # iterate over each collection and find all documents with a name in the list
        for collection_name in client['mydatabase'].list_collection_names():
            collection = client['mydatabase'][collection_name]
            docs = collection.find({'name': {'$in': names}})
            matching_docs[collection_name] = docs

        return matching_docs

    def insert_data(self, data, collection_name):
        # create a new MongoClient object
        client = MongoClient('mongodb://localhost:27017/')

        # access the database
        db = client['mydatabase']

        # # access a collection (table)
        collection = db[collection_name]

        for row in data:
            # check if the document with the given name already exists
            existing_doc = collection.find_one({'name': row['name']})

            if existing_doc:
                # if the document exists, check if the data is different
                if not self.compare_dicts(existing_doc, row):
                    # if the data is different, update the document
                    collection.replace_one({'name': row['name']}, row)
                    print('Document updated.')
                else:
                    print('Document already exists.')
            else:
                # if the document does not exist, insert it
                collection.insert_one(row)
                print('Document inserted.')

    def bgu_data(self):
        soup = BeautifulSoup(requests.get(
            'https://www.study.co.il/%D7%AA%D7%A0%D7%90%D7%99-%D7%A7%D7%91%D7%9C%D7%94-%D7%90%D7%95%D7%A0%D7%99%D7%91%D7%A8%D7%A1%D7%99%D7%98%D7%AA-%D7%91%D7%9F-%D7%92%D7%95%D7%A8%D7%99%D7%95%D7%9F/').content,
                             'html.parser')

        table = soup.find('tbody')
        rows = table.find_all('tr')

        data = []
        for row in rows[1:]:  # skip the header row
            cols = row.find_all('td')
            pcy_and_or = cols[2].text
            if 'או' in pcy_and_or:
                additional = False
                psychometric = pcy_and_or.replace('או', '').strip()
            elif 'ובנוסף' or 'בנוסף' in pcy_and_or:
                additional = True
                psychometric = pcy_and_or.replace('ובנוסף', '').replace('בנוסף', '').strip()
            else:
                additional = False
                psychometric = pcy_and_or.strip()
            result = Admission(name=cols[0].text.strip(), sum=self.convert_to_num(cols[1].text),
                               psychometric=self.convert_to_num(psychometric),
                               additional=additional, without=cols[3].text.strip(), notes=cols[4].text.strip(),
                               date=datetime.datetime.today().strftime('%d/%m/%Y'))

            data.append(result.get_mongo())

        self.insert_data(data, 'BGU')

    def tech_data(self):
        soup = BeautifulSoup(requests.get(
            'https://www.study.co.il/%D7%AA%D7%A0%D7%90%D7%99-%D7%A7%D7%91%D7%9C%D7%94-%D7%94%D7%98%D7%9B%D7%A0%D7%99%D7%95%D7%9F/').content,
                             'html.parser')

        table = soup.find('tbody')
        rows = table.find_all('tr')

        data = []
        for row in rows[1:]:  # skip the header row
            cols = row.find_all('td')
            try:
                result = Admission(name=cols[0].text.strip(), sum=self.convert_to_num(cols[1].text),
                                   min_final_grade_average=self.convert_to_num(cols[2].text),
                                   additional=True, psychometric=cols[3].text.strip(), notes=cols[4].text.strip(),
                                   date=datetime.datetime.today().strftime('%d/%m/%Y'))
            except:
                continue

            data.append(result.get_mongo())

        self.insert_data(data, 'TECH')

    def tlv_uni_data(self):
        soup = BeautifulSoup(requests.get(
            'https://www.study.co.il/%D7%AA%D7%A0%D7%90%D7%99-%D7%A7%D7%91%D7%9C%D7%94-%D7%90%D7%95%D7%A0%D7%99%D7%91%D7%A8%D7%A1%D7%99%D7%98%D7%AA-%D7%AA%D7%9C-%D7%90%D7%91%D7%99%D7%91/').content,
                             'html.parser')

        table = soup.find('tbody')
        rows = table.find_all('tr')

        data = []
        for row in rows[1:]:  # skip the header row
            cols = row.find_all('td')
            additional = cols[2].text
            if 'או' in additional:
                additional = False
            elif 'וגם' in additional:
                additional = True
            else:
                additional = None
            try:
                result = Admission(name=cols[0].text.strip(), sum=self.convert_to_num(cols[1].text),
                                   psychometric=self.convert_to_num(cols[3].text),
                                   additional=additional, notes=cols[4].text.strip(),
                                   date=datetime.datetime.today().strftime('%d/%m/%Y'))
            except:
                continue

            data.append(result.get_mongo())

        self.insert_data(data, 'TLV')

    def evrit_uni_data(self):
        soup = BeautifulSoup(requests.get(
            'https://www.study.co.il/%D7%AA%D7%A0%D7%90%D7%99-%D7%A7%D7%91%D7%9C%D7%94-%D7%90%D7%95%D7%A0%D7%99%D7%91%D7%A8%D7%A1%D7%99%D7%98%D7%94-%D7%94%D7%A2%D7%91%D7%A8%D7%99%D7%AA/').content,
                             'html.parser')

        table = soup.find('tbody')
        rows = table.find_all('tr')

        data = []
        for row in rows[1:]:  # skip the header row
            cols = row.find_all('td')
            additional = cols[2].text
            if 'או' in additional:
                additional = False
            elif 'וגם' in additional:
                additional = True
            else:
                additional = None
            above30 = self.convert_to_num(cols[4].text)
            if not above30 is None:
                above30 = f'מעל גיל 30 פסיכומטרי נחוץ: {above30}'

            min_final_grade_average = self.convert_to_num(cols[1].text)
            if not min_final_grade_average is None:
                min_final_grade_average *= 10

            result = Admission(name=cols[0].text.strip(), min_final_grade_average=min_final_grade_average,
                               additional=additional, psychometric=self.convert_to_num(cols[3].text),
                               notes=cols[5].text.strip() + ' ' + above30,
                               date=datetime.datetime.today().strftime('%d/%m/%Y'))

            data.append(result.get_mongo())

        self.insert_data(data, 'EVR ')

    def update_all(self):
        self.bgu_data()
        self.tech_data()
        self.tlv_uni_data()
        self.evrit_uni_data()


# client = MongoClient('mongodb://localhost:27017/')
#
# # access the database
# db = client['mydatabase']
#
# # # access a collection (table)
# collection = db['BGU']
#
# query = {'name': 'אמנויות'}
# results = collection.find(query)
#
# for doc in results:
#     print(doc)
