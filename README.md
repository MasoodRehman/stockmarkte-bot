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
Item pipeline get the item dictionary object that passed by spider and save into the store/company_profiles.json file.

### REST API
Web api expose some endpoints to the client through which clients gets data from the datastore by applying different criteria. The api endpoint and its details are given below.

#### Dumpdata:
This endpoint get the data from store/company_profiles.json and store it into database.

Method: Get
Endpoint: http://localhost:5000/dumpdata

#### Companies:
This endpoint return all the companies saved in the database.

Method: Get
Endpoint: http://localhost:5000/companies

#### Companies Filter:
This the same endpoint as companies but with query parameters. It will return you the result based on the revenue amount.

Method: Get
Endpoint: http://localhost:5000/companies?revenue_gte=10000 


Here is the postman link where all api endpoints implemented
https://www.getpostman.com/collections/a008f21bf744ed39f457
