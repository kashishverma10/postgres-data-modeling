What is the purpose of this Database?

The purpose of this Database is to have a well-designed schema that helps Sparkify to make use of the JSON metadata of their user activity logs and songs in their music streaming app. Having a dataset in form of a Postgres database tables will allow Sparkify to analyze their users’ activity on their app and to get data reports relevant to their business initiatives. Another purpose of this database is to have an ETL pipeline that helps inserting new data to the tables so that we have an updated table with new user’s activity and songs each time, to run analytical queries.

How are we going to do it?

Database schema design is a Star-Schema; here we have one fact-table called songplay and four dimension tables which are users, songs, artists and time. This allows us to have denormalized tables to run simplified queries that require aggregation of data. Also, the steps developed in the ETL pipeline help to process the JSON metadata of the user activity logs and songs, and to replicate it into our fact and dimension tables. As the new user activity logs get generated frequently, the need of an ETL pipeline is extremely important in our case as it enables us to have accurate data every time when we run queries.


Some Sample Queries: 

1. Finding the day of the month with most no. of sessions.

Query: 
SELECT DATE_PART('DAY', start_time), COUNT(*) total_sessions FROM songplays GROUP BY 1 ORDER BY 2 DESC LIMIT 1;

Result:
date_part total_sessions
15.0         479

2. Finding the most recently active user: 

Query:
SELECT users.first_name, users.last_name, songplays.start_time from songplays join users on users.user_id = songplays.user_id order by 2 LIMIT 1;

Result:
first_name   last_name  start_time 
Kevin        Arellano   2018-11-23 00:07:25.796000