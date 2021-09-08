import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3
from request_tokens import get_access_token


DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
DATABASE_NAME= "my_played_tracks.sqlite"
USER_ID = "119842596"
TOKEN = "BQBCIindfQQZH63GmfYNnBkdMOcklL7tLWFM3OO_ifol7smd7E8e6JBsAcy0NzNh1cNfkffLlobf08-dLq_WOl3Mhj5XydKvVqw2ubrzUQtxFhIrrlo8VDbQ3haX-J-fYVdoHurX_A6Dbpn2MMqHcHfRH9chSR2mUI3ZJyL54Eg"

def check_if_valid_data(df: pd.DataFrame):
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False

    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary key check is violated")

    if df.isnull().values.any():
        raise Exception("Null value found")

#    today = datetime.datetime.now()
#    lastweek = datetime.datetime.now() - datetime.timedelta(days=7)
#    today = datetime.datetime.

#    timestamps = df["timestamp"].tolist()
#    for timestamp in timestamps:
#        if lastweek <= datetime.datetime.strptime(timestamp, "%Y-%m-%d") <= today:
#            pass
#        else:
#            print("problem with follow date: " + timestamp)
#            raise Exception("At least one of the returned songs does not come from within the last 7 days")

    return True
    

if __name__ == "__main__":

    print("My token is" + TOKEN)

    headers = {
        "Accept" : "application/json",
        "Content-type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }

    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    lastweek = today - datetime.timedelta(days=7)
    lastweek_unix_timestamp = int(lastweek.timestamp()) * 1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time = lastweek_unix_timestamp), headers=headers)

    data = r.json()

    print(json.dumps(data, indent = 2))

    song_names = []
    artist_names = []
    played_at = []
    timestamps = []

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

    song_dict = {
        "song_name" : song_names,
        "artist_name" : artist_names,
        "played_at" : played_at,
        "timestamp" : timestamps 
    }

    song_df = pd.DataFrame(song_dict, columns= ["song_name", "artist_name", "played_at", "timestamp"])

    #Validation
    if check_if_valid_data(song_df):
        print("Dates are valided")

    #Load
    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Opened database successfully")

    try:
        song_df.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print('Data already exists in the database')

    conn.close()
    print("Closed the database succesfully")