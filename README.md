# Reddit Sentiment Analysis Dash Application


1st command pmt type - `python Reddit_Stream.py`              
2nd command pmt type - `python app.py runserver`

Live-streaming sentiment analysis application created with Python and Dash, hosted at [**sentiment-reddit.herokuapp.com**](http://sentiment-reddit.herokuapp.com/).


## Repo Contents: 
- `app.py` - The main front-end application code. Contains the dash application layouts, logic for graphs, interfaces with the database...etc. If you want to clone this and run it locally, you will be using the `python app.py runserver`
- `reddit_stream.py` - This should run in the background of your application. This is what streams threads, comments, replies from subreddit /worldnews, storing them into the postgresql database, which is what the `app.py` file interfaces with. 
- `db-truncate.py` - A script to truncate the infinitely-growing postgresql database.

## Quick start

- Clone repo
- install `requirements.txt` using `pip install -r requirements.txt`
- Create an API on reddit.
- Fill in your Reddit API credentials to `reddit_stream.py`.
- Setup postgresql credentials. or to run locally on sqlite database, replace `psycorg2.connect(...` with `conn = sqlite3.connect("reddit.db")`.
- Run `reddit_stream.py` to build database
- You might need the latest version of sqlite. 
- Run `app.py` to run the app.
- Consider running the `db-truncate.py` from time to time (or via a cronjob), to keep the database reasonably sized. In its current state, the database really doesn't need to store more than 2-3 days of data most likely. 


## Credits

The most credit goes to [**Sentdex**](https://github.com/Sentdex/) who inspired me to create this app.
