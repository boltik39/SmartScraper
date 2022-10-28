# Project 19635 MIEM HSE - SmartScraper
___
## Quick start
1. Make `git clone`
```
git clone <rep_link>
```
2. Go to the project dir `SmartScraper`
```
cd SmartScraper
```
3. Install all modules
```
pip install -r requirements.txt
```
4. Install DB credentials for using PostgreSQL
5. Run server
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
6. Go to `http://localhost:8000/admin`
7. Create the required number of users
8. In `scraper/bases.py` add user to the end of `DEVICE_QUERIES` dictionary and specify an empty list of devices for him 
```
DEVICE_QUERIES = {'user0' : empty_device_queries[0],
                  'user1' : empty_device_queries[1],
                  'user2' : empty_device_queries[2],
                  'user3' : empty_device_queries[3],
                  'user4' : empty_device_queries[4],
                  'user5' : empty_device_queries[5],
                  'user6' : empty_device_queries[6],
                  'user7' : empty_device_queries[7],
                  'user8' : empty_device_queries[8],
                  'user9' : empty_device_queries[9],
                  'your_user' : empty_device.quieries[10],
}

```
