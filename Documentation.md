# Documentation

## Demo

### Introduction

<u>The Technology used in the implementation:</u>

- MongoDB : Database.
- Python : Read JSON file, process raw data, save into the database and provide the APIs .
  - flask : Python module. Can work as a server and helps to define the APIs. 
  - pymongo : Python module. Allows Python to interact with MongoDB.
- Vue.js: Frontend framework


### Data process and Database

The model design is based on the MongoDB database, so the format of each document is not restricted by the columns.

- **Outlets** from two sources are combined and a new 'source' column is added. 

- For **Reviews**, 'outlet name' is added so the client can see the outlet name for a certain review without querying between two collections.

Here is the structure of the collections in MongoDB:

```
|
--database
	|
	--Outlet
	|
	--Reviews
	|
	--User
	|
	--Menu
```



Python is used to read the five raw data sample files, deleted unwanted information such as  `{'cuisines': }` and `{'lat'}` in `tripadvisor_outlet.json` file and inserted them into the connected MongoDB database.



The following example of a documents illustrates how one piece of data from `Tripadvisor` and `Ubereats` is stored in **Outlet** collection :

```json
{
    "_id": {
        "$oid": "60bd2ef03b0d5abf11178683"
    },
    "address": "No.1 Austin Road West | International Commerce Centre,, Hong Kong, China",
    "country": "China",
    "id_outlet": "https://www.tripadvisor.com/Restaurant_Review-g294217-d2198231-Reviews-OZONE-Hong_Kong.html",
    "name": "OZONE",
    "phone": "+852 2263 2270",
    "reviews_nr": 3970,
    "source": "tripadvisor"
}

{
    "_id": {
        "$oid": "60bd2ef03b0d5abf111787b0"
    },
    "id_outlet": "49902879992629236407831306704091856908",
    "country": "NL",
    "name": "Dominos",
    "address": "Kamperfoelieweg 40, 1032 HP Amsterdam, Netherlands",
    "reviews_nr": 52,
    "source": "ubereats"
}
```

The example document from **Reviews** collection:

```json
{
    "_id": {
        "$oid": "60bd2ef03b0d5abf1117874c"
    },
    "user": "Brittaperry",
    "rating": 3,
    "id_outlet": "https://www.tripadvisor.com/Restaurant_Review-g294217-d788642-Reviews-The_Peak_Lookout-Hong_Kong.html",
    "review": "Food was nice but overpriced. Service could be better but it wasn't terrible. You won't have a bad time here but if you're looking for value for money, maybe skip this place. :)",
    "outlet": "The Peak Lookout"
}
```

The example document from **User** collection:

```json
{
    "_id": {
        "$oid": "60bd2ef03b0d5abf111786e8"
    },
    "reviews": 142,
    "likes": 136,
    "name": "rkim511"
}
```

The example document from **Menu** Collection:

```json
{
    "_id": {
        "$oid": "60bd2ef03b0d5abf111787c9"
    },
    "id_outlet": "49902879992629236407831306704091856908",
    "name": "Sprite fles",
    "brand": "Sprite",
    "price": 3.95,
    "volume": "1500"
}
```



One drawback of MongoDB is that it automatically adds an object id to each document. If no schema is defined, you can not guarantee the uniqueness of certain attributes since you can store data without defining the primary key.



### APIs

(Check how to run the APIs on `README`)



Clients can send **GET** or **POST** requests to `http://localhost:5000/` to get results in  **JSON**.



Here is the list of **API implemented** :

| API                           | Description                                      | Method | Example                                   |
| :---------------------------- | :----------------------------------------------- | :----: | :---------------------------------------- |
| /                             | Index page                                       |  GET   | localhost:5000/                           |
| /outlets/brand/[brand name]   | List outlets which have a certain brand.         |  GET   | localhost:5000/outlets/brand/fuz          |
| /outlets/source/[source name] | List outlets by their source                     |  GET   | localhost:5000/outlets/source/ubereats    |
| /menus/price/above/[price]    | List menus which the item is above certain price |  GET   | localhost:5000/menus/price/above/10       |
| /insert/outlet/[data]         | Add a new outlet into the database               |  POST  | localhost:5000/insert/outlet/?name = ''.. |

- **The root page API** : Returns a static html page. If the server runs successfully, you should be able to see "API Connected" on this page
- **List outlets by brand** : Regex is used to allow ambiguous query which allows the user to  enter only the first several letters of a brand name. Brand name get from the GET request is capitalized, so query such as 'coca' instead of 'Coca' is allowed.
- **List outlets by source** : Returns outlets by source name. If the source is not in the database,  empty set will be returned.
- **List menus by item price** : Returns menus which have items above requested price.
- **Add new outlet** :  Insert a new outlet into database `Outlet` collection. There is no scheme defined for the insertion which means the inserted document can have any attributes. 
