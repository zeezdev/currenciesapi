# Currencies API

## About

Project provides an access to rates of currencies (current and historical) by means of Rest API. 

## Project structure

```
.
├── app
│   ├── create_app.py
│   ├── __init__.py
│   ├── models.py
│   ├── resources.py
│   ├── settings.py
│   └── tools.py
├── manage.py
├── populate_data.js
├── populate_data.sh
├── README.md
├── requirements.txt
└── run.sh
``` 

**manage.py** - Python interface to run project

**populate_data.js** - JS script to prepare test data in the database

**populate_data.sh** - runner for populate_data.js

**requirements.txt** - Python requirements

**run.sh** - project runner script

**app/create_app.py** - contains `create_app()` function that setups the Flask application

**app/__init__.py** - imports outside main objects of app package

**app/models.py** - definitions of database entities: `Currency, Rate, RateHistory`

**app/resources.py** - implementation of API endpoints

**app/settings.py** - configuration of the Flask application

**app/tools.py** - contains `Ticker` helper class to parse and validate of tickers 

## Database structure
 
### Collections:
 
 **currencies** - name and code of supported currencies
 
 ```
{
	"_id" : ObjectId("5ca39d5b7f90ca8269066abe"),
	"name" : "United States dollar",
	"code" : "USD"
},
{
	"_id" : ObjectId("5ca39e047f90ca8269066abf"),
	"name" : "Bitcoin",
	"code" : "BTC"
},

 ```
 
 **rates** - current rates of supported currencies. All rates persists in USD.
 
 
 ```json
 {
	"_id" : ObjectId("5ca3db31dd8286f5fc6442a1"),
	"currency" : "BTC",
	"value" : 4736
},
{
	"_id" : ObjectId("5ca3db31dd8286f5fc6442a2"),
	"currency" : "ETH",
	"value" : 156
},
```

**rates_history** - historical rates of currencies. The time step is 10 minutes.

```json
{
	"_id" : ObjectId("5ca4f4ac75eac5d066855457"),
	"currency" : "WAVES",
	"value" : 12.61,
	"ts" : ISODate("2018-01-01T07:50:00.000Z")
},
{
	"_id" : ObjectId("5ca4f4ac75eac5d066855458"),
	"currency" : "ZEC",
	"value" : 587,
	"ts" : ISODate("2018-01-01T07:50:00.000Z")
},
{
	"_id" : ObjectId("5ca4f4ac75eac5d066855459"),
	"currency" : "BTC",
	"value" : 4736,
	"ts" : ISODate("2018-01-01T08:00:00.000Z")
},
```

## API

`/api/rates` - Get value of currencies.

### Parameters

**ticker** _(required)_, string - Interested ticker, for example "BTC/USD"

**ts** (optional), string - Timestamp (YYYY-MM-DD hh:mm:ss) to get a historical value in the particular date and time

### Examples

**curl**

`curl -X GET "http://127.0.0.1:8080/api/rates?ticker=BTC%2FUSD" -H "accept: application/json"`

`curl -X GET "http://127.0.0.1:8080/api/rates?ticker=BTC%2FUSD&ts=2018-07-04%2012%3A56%3A03" -H "accept: application/json"`


**http**

`http://<hostname>/api/rates?ticker=BTC%2FUSD`

`http://<hostname>/api/rates?ticker=BTC%2FUSD&ts=2018-07-04%2012%3A56%3A03`


### Responses

**200** - Success

```json
{
  "rate": 4736,
  "ticker": "BTC/USD",
  "ts": "Wed, 04 Jul 2018 12:56:03 GMT"
}
```

**400** - Bad request. Argument “ticker” was not specified or has invalid format. Argument “ts” has an invalid format or out of range
