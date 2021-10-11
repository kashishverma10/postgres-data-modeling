
# **What is the purpose of this Project?**

The purpose of this Database is to have a well-designed schema that helps Sparkify to make use of the JSON metadata of their user activity logs and songs in their music streaming app. Having a dataset in form of a Postgres database tables will allow Sparkify to analyze their users’ activity on their app and to get data reports relevant to their business initiatives. Another purpose of this database is to have an ETL pipeline that helps inserting new data to the tables so that we have an updated table with new user’s activity and songs each time, to run analytical queries.

# **How are we going to do it?**

Database schema design is a Star-Schema; here we have one fact-table called songplay and four dimension tables which are users, songs, artists and time. This allows us to have denormalized tables to run simplified queries that require aggregation of data. Also, the steps developed in the ETL pipeline help to process the JSON metadata of the user activity logs and songs, and to replicate it into our fact and dimension tables. As the new user activity logs get generated frequently, the need of an ETL pipeline is extremely important in our case as it enables us to have accurate data every time when we run queries.

# **ETL Process:**

The ETL process is defined in the etl.py file. The process involves the following steps:

## For Song and artist table (from data/song_file)
- The first step processes JSON files in data/song_data and converts the data itno pandas dataframe.
- The data frame is then labelled with the collumn names as per the song table.
- Now the values are extracted from the collumns and are turned into a list of values.
- These values are then loaded to the song table.
- The same data frame is also labelled with the collumn name as per the artist table.
- And the values extracted from the artist collumns are loaded to the artist table.

## For Songplay, user and time tables (from data/log_file)
- Then the JSON log files in data/log_data are processesed and the data is extracted from it in a new pandas dataframe.
- The dataframe is then filtered with Nextsong action in the page collumn
- The ts timestamp collumn is converted into a date time format, and the data is extracted from it as per the time table collumns.
- The extracted date time data is then loaded to the time table.
- The data is extracted from log files dataframe for users as per the table collunse and then loaded to the users table.
- For songplay table, we fetch the song_id and artist_id from the song and artist tables created above and match it to log file dataframe rows.
- The song id and artisid is then inserted to the songplay table along with the other data needed from the log file dataframe defined for songplay table.


# **Project Repository Files**

- ## *sql_queries.py*
This file has all the sql queries needed to define our fact and dimension tables and inserting data records into those tables.

- ## *create_tables.py*
This file helps us to reset and create our tables in the databse and imports the queries from the sql_queries.py file.

- ## *etl.ipynb*
This jupyter notebook provides a step by step break down of our etl process.

- ## *etl.py*
This file is derived from the etl.ipynb file and is run to to extract data from all the JSON files in data folder and load them into the tables.

- ## *test.ipynb*
This jupyter notebook shows tables with all the data loaded in them and allows us to run analytical queries on the data.


# **_How to Run this Project?_**
#### - Open **Terminal**.
#### - Run *"python create_tables.py"* to reset our tables - clearing any pre-existing data.
#### - Run *"python etl.py"* to extract and load data in our tables from data directory.
#### - Open **test.ipynb** and run the cells to view data in the table and run queries to analyse data.


# **Some Sample Queries:** 

1. Finding the day of the month with most no. of sessions.

Query: 
SELECT DATE_PART('DAY', start_time), COUNT(*) total_sessions FROM songplays GROUP BY 1 ORDER BY 2 DESC LIMIT 1;

Result:
date_part| total_sessions
---------|----------------
15.0     |   479

2. Finding the most recently active user: 

Query:
SELECT users.first_name, users.last_name, songplays.start_time from songplays join users on users.user_id = songplays.user_id order by 2 LIMIT 1;

Result:
first_name|   last_name | start_time 
----------|-------------|------------
Kevin     |    Arellano | 2018-11-23 00:07:25.796000