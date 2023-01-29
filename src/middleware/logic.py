from client import mongo_client
import json

class Logic(object):
    def __init__(self):
        self.client = mongo_client

        self.db = self.client.container_group30
        self.collection_outlet = self.db.Outlet
        self.collection_users = self.db.User
        self.collection_reviews = self.db.Reviews
        self.collection_menu = self.db.Menu

    def get_outlet_by_brand(self, brand):
        query = {'brand': {'$regex': '^'+brand.capitalize()+'.*'}}             
        menus = list(self.collection_menu.find(query))
        outlets = []
        for menu_doc in menus:
            outlet_query = {'id_outlet' : menu_doc['id_outlet']}
            outlet = list(self.collection_outlet.find(outlet_query, {'_id':0, 'country':0, 'address':0, 'reviews_nr':0, 'phone':0}))
            for outlet_doc in outlet:
                outlet_doc['brand'] = menu_doc['brand']
                outlet_doc['menu_name'] = menu_doc['name']
            outlets.extend(outlet)
        
        outlets = json.dumps(outlets, indent=2, ensure_ascii=False)

        return outlets
    
    def get_outlet_by_source(self,source):
            query = {'source': source.lower()}
            if source == 'tripadvisor':
                outlets =  list(self.collection_outlet.find(query, {'_id':0}))
            elif source == 'ubereats':
                outlets =  list(self.collection_outlet.find(query, {'_id':0, 'phone':0}))
            else:
                outlets = [{'message': 'no data from ' + source}]
                
            outlets = json.dumps(outlets, indent=2, ensure_ascii=False)

            return outlets

    def get_menu_item_by_price(self, price):
        price = int(price)
        menu_query = {'price' : {'$gt':price}}
        menus = list(self.collection_menu.find(menu_query,{'_id':0, 'id_outlet':0,'volume':0}))
        menus = json.dumps(menus, indent=2, ensure_ascii=False)
        print(menus)

        return menus
    
    def create_outlet(self,data):
        data['reviews_nr'] = int(data['reviews_nr'])
        self.collection_outlet.insert_one(data)

