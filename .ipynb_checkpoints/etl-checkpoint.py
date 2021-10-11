import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *

    

def process_song_file(cur, filepath):
    """
    This function processes a songfile whose path is provided in the filepath argument.
    It extracts the song information and loads it into the songs table.
    And does the same thing for the artist's information by extracting the artist data from the file and stores it into artist table.
    
    INPUTS:
    * cur - the cursor variable
    * filepath - the path of the song file in data/song_data
    """
    # open song file
    df = pd.read_json(filepath, typ='series')

    # insert song record
    song_columns= df[['song_id','title','artist_id','year','duration']]
    song_values = song_columns.values
    song_data = song_values.tolist()
    
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_columns= df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']]
    artist_values = artist_columns.values
    artist_data = artist_values.tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This function processes the logfile, the path of which is provided in the filepath argument.
    It extracts the data from the json file and filters the data by the page that has the NextSong value.
    The timestamp from the data is processed and then stored into time table.
    Then the data of users is extracted and store in users table.
    Lastly, the song_id and artist_id is extracted from the song table and artist table based on the song title,
    artist name and duration and then stored in the songplay table.
    
    INPUTS
    * cur - the cursor variable
    * filepath - the path of the log file in data/log_data
    """
    # open log file
    df = pd.read_json(filepath, lines= True)


    # filter by NextSong action
    df = df.loc[df['page']=='NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'],unit='ms')
    
    # insert time data records
    time_data = (t.dt.time, t.dt.hour, t.dt.day, t.dt.weekofyear, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('timestamp', 'hour', 'day',' week of year', 'month', 'year', 'weekday')
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels,time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit = 'ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    This function gets the all the JSON files in from the path provided in filepath argument.
    Then the number of files found and the number files processed are printed as output.
    
    INPUTS
    * cur - the cursor variable
    * conn - connection to the database
    * filepath -  the path of the directory that contains the json files
    * func - the function variable for processing song files and log files
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    This is the main function that defines the cursor variable and connection to the database.
    It connects to the databases using the database name and credentials.
    Then it runs the functions defined above for processing the song file and the log file data.
    Lastly it closes the connection to the database.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()