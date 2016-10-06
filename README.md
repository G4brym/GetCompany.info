# GetCompany Info
This is a company repository, it was online at https://www.getcompany.info/ but because it didn much trafict i shut it down.

### Company Informations
This project doen't have any company informations out of the box, you have to get it however you want and add it to the database by yourself

### Requirements

This project requires the following libraries to work:

* django
* pytz
* psycopg2
* beautifulsoup4
* django-debug-toolbar
* tweepy

### Run
To run this Django project you have to setup some enviremont vars:
Remember that this project requires a Postgresql database, or you can change the settings file for another database.

1.  export DEBUG="1 or 0"
2.  export SECRET_KEY="random string here"
3.  export DB_HOST="Postgresql db url"
4.  export DB_USER="Postgresql db Username"
5.  export DB_PASS="Postgresql db Password"
6.  export EMAIL_USER="AWS ses email user"
7.  export EMAIL_PASS="AWS ses email password"
8.  export TWITTER_CONS_KEY="Twitter connection key"
9.  export TWITTER_CONS_SEC="Twitter connection secret"
10. export TWITTER_ACESS_TOK="Twitter acess token"
11. export TWITTER_ACESS_SEC="Twitter acess secret"

To start the server run:

1. python3 manage.py runserver

### Elastic beanstalk
This project is ready to use in the amazon elastic beanstalk, just run "eb init" and "eb deloy name" and you are ready to go

### Preview
Index Page
![index page](https://github.com/G4brym/GetCompany.info/raw/master/index.png)

Company Page
![company page](https://github.com/G4brym/GetCompany.info/raw/master/company.png)

Contact Page
![company page](https://github.com/G4brym/GetCompany.info/raw/master/contact.png)

### Statistics

Clicks and impressions on Google Search
![company page](https://github.com/G4brym/GetCompany.info/raw/master/google_search.png)

Last month we where online - cloudflare stats
![company page](https://github.com/G4brym/GetCompany.info/raw/master/last_month.png)

Google Structured Data - all companies were SEO friendly with structured data
![company page](https://github.com/G4brym/GetCompany.info/raw/master/search_data.png)

Twitter page - every time we crawl a new company we publish a new tweet
![company page](https://github.com/G4brym/GetCompany.info/raw/master/twitter.png)
