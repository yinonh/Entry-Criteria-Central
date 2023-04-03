from pymongo import MongoClient

class Data:

    def __init__(self, *args, **kwargs):
        super(Data, self).__init__(*args, **kwargs)
        self.client_name = ''
        self.db_url = ''

    def convert_to_num(self, str_number):
        if str_number.strip() == '':
            return None
        else:
            try:
                return int(str_number.strip())
            except:
                return float(str_number.strip())

    def insert_data(self, data, collection_name):
        # create a new MongoClient object
        client = MongoClient(self.db_url)

        # access the database
        db = client[self.client_name]

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

    def update_all(self):
        pass
