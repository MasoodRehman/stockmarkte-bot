# Stockmarkte Crawler
This is a web crawler written in python scrapy framework which crawling stock market data and saved for analysis.

There are couple of way to crawl a website almost any language have libraries to parsing data but most of them are not efficient. Since we are crawling a website efficiently python scrapy is framework which scrap the websites fast and efficient.

## How it works
There are two parts of the application in first part we collect data from the remote server and in second part we store the data into database and expose that data to the clients through REST API.

![flow diagram](https://github.com/MasoodRehman/stockmarkte-bot/blob/master/store/flowdiagram.jpg)

The above flow diagram shows how our scrapping process should work:

### Scrapy Spider
When scrapy spider invoked it will send a request to the target website in our case it is http://stock.vietnammarkets.com/vietnam-stock-market.php after getting response from the website it will start parsing the data make it clean it will again send another request on the link but this time it will send request for getting the company detail once get the response from there it will make the response clean and assign the company detail data to the item dictionary. After assigning data to the dictionary parameters it will pass that data to the item pipeline for further processing.

### Item Pipeline
Item pipeline get the item dictionary object that passed by spider and save into the `store/company_profiles.json` file.

### REST API
Web api expose some endpoints to the client through which clients gets data from the datastore by applying different criteria. The api endpoint and its details are given below.

#### Dumpdata:
This endpoint get the data from `store/company_profiles.json` and store it into database.

Method: Get <br/>
Endpoint: http://localhost:5000/dumpdata

#### Companies:
This endpoint return all the companies saved in the database.

Method: Get<br/>
Endpoint: http://localhost:5000/companies

#### Companies Filter:
This the same endpoint as companies but with query parameters. It will return you the result based on the revenue amount.

Method: Get<br/>
Endpoint: http://localhost:5000/companies?revenue_gte=10000 


Here is the postman link where all api endpoints implemented <br/>
https://www.getpostman.com/collections/a008f21bf744ed39f457

## Directory Structure
The following is the directory structure of the project.

![flow diagram](https://github.com/MasoodRehman/stockmarkte-bot/blob/master/store/directories_structure.jpg)

### Stockmarket_bot:
This is main project directory.

### Scrapy_stock_app:
This is the scrapy project directory where scrapy spider, item dictionary, item pipeline and other scrapy framework setting and configuration files are placed.

   ##### Spider
   This is the home of spiders. All scrapy spiders are placed in this directory. 
   Currently  there is only one spider `vietnam.py` contain in the directly.
    
   ##### Items.py:
   This is the item dictionary which fill by the spider from crawled data.
    
   ##### Pipelines.py
   This is the item pipeline which get the item dictionary passed by spider and saved into the `store/company_profiles.json` file.
    
### Store:
This directory contain the json file where spider save the item dictionary.

### Venv:
This is the virtual environment folder where all the libraries of scrapy installation and flask framework files and any other dependencies libraries are stored.

### App.py
This is the flask application file where REST API code written, This create a server and listening for client requests on a port 5000 and serve the client request.

### Database.db
All the data contain in this sqlite data storage.

### Helpers.py
This helper file contain function that help flask app, such as load the data from json file and convert it into list of dictionaries, convert database result into dictionary. This file create for the separation of concern purpose so the code make clean and separate.

### Migration.py
This file contain database migration, it will create a database along companies table.

## How to run the code
First of all create a virtual environment and activate it:

```python
python -m venv venv
source venv/bin/activate
```

Then install the required dependencies with:

```python
pip install scrapy flask
```

After installation of libraries completed next task is to migrate a table into database.

```python
python migration.py
```

The above command will create a `database.db` file in the root directory and migrate a `comapnies` table.

Next task is to run the scapy spider to collect data save into `comapnies` table. First goto the `scrapy_stock_app` directory as the scrapy command only work in the scrapy app directory and run the following command to start the `vietnam` spider.

```python
scrapy crawl vietnam
```
