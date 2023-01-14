import pymongo 
import json

class JsonToMongo(object):
    def __init__(self):
        self.client = pymongo.MongoClient('127.0.0.1',8888)

        self.db = self.client.container_group30
        self.collection_outlet = self.db.Outlet
        self.collection_users = self.db.User
        self.collection_reviews = self.db.Reviews
        self.collection_menu = self.db.Menu

    def _open_file(self, filename):
        self.file = open(filename,'r')

    def _close_file(self):
        self.file.close()
    
    def process_tripadvisor_outlet(self):
        filename = 'resource/tripadvisor_outlet.json'
        self._open_file(filename)
        data = json.load(self.file)

        try:
            #delete irrelevent fileds(columns)
            for doc in data:
                del doc['cuisines']
                del doc['features']
                del doc['city']
                del doc['menu']
                del doc['lat']
                del doc['lon']
                del doc['opening_hours']
                del doc['postal_code']
                del doc['price_level']
                del doc['price_range']
                del doc['rating']
                del doc['region']
                del doc['special_diets']
                del doc['street']
                del doc['tags']
                del doc['url']
                del doc['website']
                doc['source'] = 'tripadvisor'

            self.collection_outlet.insert_many(data)
            print ('tripadvisor_out insert successfully')

        except  Exception as e:
            print (e)
        finally:
            self._close_file()

    def process_tripadvisor_user(self):
        filename = 'resource/tripadvisor_user.json'
        self._open_file(filename)
        data = json.load(self.file)

        try:
            for doc in data:
                del doc['address']
                doc['name'] = doc.pop('user')

            self.collection_users.insert_many(data)
            print ('tripadvisor_user insert successfully')

        except  Exception as e:
            print (e)
        finally:
            self._close_file()

    def process_tripadvisor_reviews(self):
        filename = 'resource/tripadvisor_reviews.json'
        self._open_file(filename)
        data = json.load(self.file)

        try:
            #delete irrelevent fileds(columns)
            for doc in data:
               doc['review'] = doc.pop('body')
               del doc['date']
               del doc['url']
               del doc['traveler_type']

               query = {'id_outlet': doc['id_outlet']}             
               outlet = list(self.collection_outlet.find(query))
               outlet_name = outlet[0]['name']
               doc['outlet'] = outlet_name

            self.collection_reviews.insert_many(data)
            print ('tripadvisor_reviews insert successfully')

        except  Exception as e:
            print (e)
        finally:
            self._close_file()


    def process_ubereats_outlet(self):
        filename = 'resource/ubereats_outlet.json'
        self._open_file(filename)
        data = json.load(self.file)

        try:
            for doc in data:
                doc['phone'] = 'NaN'
                doc['source'] = 'ubereats'
            self.collection_outlet.insert_many(data)
            print ('ubereats_out insert successfully')

        except  Exception as e:
            print (e)
        finally:
            self._close_file()

    def process_ubereats_menu(self):
        filename = 'resource/ubereats_menu.json'
        self._open_file(filename)
        data = json.load(self.file)

        try:
            self.collection_menu.insert_many(data)
            print ('ubereats_menu insert successfully')

        except  Exception as e:
            print (e)
        finally:
            self._close_file()

    def sample_to_database(self):
        self.process_tripadvisor_outlet()
        self.process_tripadvisor_user()
        self.process_tripadvisor_reviews()
        self.process_ubereats_outlet()
        self.process_ubereats_menu()

j2m = JsonToMongo()

