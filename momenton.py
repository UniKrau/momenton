from datetime import date
import mysql.connector
from singleton_decorator import singleton

"""
Momenton Data Challenge
Here is the Data Engineering Code Challenge:
Data Engineering Code Challenge
Problem Statement
You have been engaged to provide insights for a movie production company. 
They want to understand the most popular movie genres, year by year, for the past decade by using user rating from tweets.
Data Sources
Use may only use the following Movie Tweetings dataset: https://github.com/momenton/MovieTweetings/tree/master/snapshots/100K
Instructions
You may use any language.
Use GitHub to share you solution.
 users.dat
 format: userid::twitter_id
              1::18405182

movies.dat
*movie_id::movie_title (movie_year)::genre|genre|genre*. For example:
 0110912 ::Pulp Fiction (1994)     ::Crime|Thriller

rating.dat
*user_id::movie_id::rating::rating_timestamp*. For example:

   14927::0110912 ::  9   ::1375657563
   1    ::1074638 ::  7   ::1365029107
   1    ::1853728 ::  8   ::1366576639
select from_unixtime(1300464000,"%Y-%m-%d %h %i %s") from table;

select a.movie_title, from_unixtime(b.rating_timestamp,"%Y") as year, avg(b.rate) as avgrate from movies a join rating b on a.movie_id=b.movie_id  group by a.movie_title,  year order by avgrate desc limit 10;
"""

query = """select a.movie_title, from_unixtime(b.rating_timestamp,"%Y") as year, avg(b.rate) as avgrate 
                from movies a join rating b on a.movie_id=b.movie_id  
                group by a.movie_title,  year 
                order by avgrate desc limit 500;"""

@singleton
class Momenton:
    connection = None
    def get_connection(self):
        if self.connection is None:
            try:
                self.connection = mysql.connector.connect(host="localhost", user="root", passwd="mypassword",db="mydatabase")
                cursor = self.connection.cursor()
                cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
            except mysql.connector.Error as err:
                print( "Something went wrong: {}".format(err))
        return self.connection

    def insert_info(self,filepath,query,tablename):
        data = self.__read_data(filepath)
        records = []
        try:
            for x in data:
                datalist = x.strip("\n").split("::")
                records.append(tuple(datalist))
            cursor = self.get_connection().cursor()
            cursor.execute(tablename)
            cursor.executemany(query,records)
            self.get_connection().commit()
        except IOError as e:
            print(e)
        finally:
            data.close()
    
    def __read_data(self,filepath):
        data = None
        if filepath is not None:
           data = open(filepath,'r')
        return data

    def mm_close(self):
        if(self.get_connection().is_connected):
            self.get_connection().close()
    """
        mock test
    """
    def mockexample(a,b):
        return a+b
    
    """
    They want to understand the most popular movie genres, year by year, 
    for the past decade by using user rating from tweets.
    """

    def popular_movie(query):
        try:
            cursor = self.get_connection().cursor()
            result = cursor.execute(query)
            return result
        except mysql.connector.Error as err:
                print( "Something went wrong: {}".format(err))