# Python for Sharing

In this repo you will find a smattering of different Python things that I want to share. Yes, I could have created a separate repo for each of these, however they are small and it helps me stay organized. Enjoy!

# What's Here

## Government Benefits Spider (govbenefitsspider)

A group of Scrapy spiders used for scraping data from the benefits.gov website.

### Prerequisites

* Python >= 2.7.11
* Scrapy >= 1.0.5
* fake-useragent >= 0.0.8
* service_identity >= 14.0.0

### Available Spiders

1. benefitstofile: scraper to save the entire HTML response to a file
2. benefitlist: scraper to grab only the programs from the list page
3. benefitprogramspider: full on looping spider; will get the details for each program

### Instructions

Install Scrapy and fake-useragent
```
pip install scrapy
pip install fake-useragent
```

1. Change into the govbenefitsspider/govbenefitsspider directory
2. Run the following commmands replacing [NAME_OF_SPIDER] with the name of one of the spiders above:
```
scrapy crawl [NAME_OF_SPIDER]
```


## Pandas for Noobs (pandas-for-noobs)

A Jupyter notebook showing three very basic but useful ways to use Pandas for data engineering and analysis.

### Prerequisites

* Python >= 3.5.1
* Pandas >= 0.17.1
* Jupyter >= 4.0.0

### What's Covered

1. Ensuring changes you make to DataFrames stick
2. Applying a function with no arguments to a DataFrame
3. Applying a function with arguments to a DataFrame

### Instructions

1. Run the *Three Pandas Tips for Pandas Noobs* notebook and enjoy the awesome.


## PBIC Pricing Scraper (pbic-pricing-scraper)

A simple scraper used to extract the price of books from the Packt website

### Prerequisites

* Python >= 3.5.1
* BeaufifulSoup4 >= 4.4.1

### Instructions

1. Change the file path on line 80 of pbic_pricing_scraper.py or in the Jupyter notebook file
2. Run the script (or notebook)


## Practical Predictive Modeling in Python

Code and fake dataset used to show how to create and train a predictive model.

### Prerequisites

* Python >= 3.5.1
* Pandas >= 0.17.1
* scikit-learn >= 0.17
* Jupyter >= 4.0.0

### Instructions

1. Run the *TLO Validation With Logistic Regression V3* notebook to see an example of creating and training a LogisticRegression model.
2. Run the *Apply The Logistic Model To New TLO Data* notebook to see how to apply the model to new observations (data).