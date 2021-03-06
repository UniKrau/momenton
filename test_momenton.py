import unittest
from unittest.mock import MagicMock,Mock

from momenton  import Momenton

movies_insert = """INSERT INTO movies (movie_id,movie_title,genre) VALUE(%s,%s,%s)"""
users_insert  = """INSERT INTO users (id,twitter_id) VALUE(%s,%s)"""
rating_insert = """INSERT INTO rating (user_id,movie_id,rate,rating_timestamp)VALUE(%s,%s,%s,%s)"""

user_table = """
    CREATE TABLE IF NOT EXISTS users(
        id integer PRIMARY KEY  NOT NULL,
        twitter_id integer NOT NULL
    );
    """
movies_table = """
    CREATE TABLE IF NOT EXISTS movies(
        movie_id  integer PRIMARY KEY NOT NULL,
        movie_title text NOT NULL,
        genre text NOT NULL
    );
    """  
  
rating_table = """
    CREATE TABLE IF NOT EXISTS rating(
        id integer AUTO_INCREMENT PRIMARY KEY,
        user_id   integer NOT NULL,
        movie_id  integer NOT NULL,
        rate      integer NOT NULL,
        rating_timestamp text NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(movie_id) REFERENCES movies(movie_id)
    );
    """
popular_query = """select a.genre, substr(a.movie_title,-5,4) as years,count(b.rate) as counts, avg(b.rate) as avgrate  
                    from movies a join rating b on a.movie_id=b.movie_id where substr(a.movie_title,-5,4) >= (from_unixtime(b.rating_timestamp ,"%Y")-10)  
                    group by a.genre, years order 
                    by counts desc;"""
class TestMomenton(unittest.TestCase):

    def setUp(self):
        self.mm = Momenton()

    def test_singleton(self):
        self.assertEqual(self.mm.get_connection(),self.mm.get_connection())
    
    def test_insert_users_table(self):
        filepath = "./users.dat"
        self.mm.insert_info(filepath,users_insert,user_table)
    
    def test_insert_movies_table(self):
        filepath = "./movies.dat"
        self.mm.insert_info(filepath,movies_insert,movies_table)
    
    def test_insert_rating_table(self):
        filepath = "./rating.dat"
        self.mm.insert_info(filepath,rating_insert,rating_table)
    
    def test_popular_movie(self):
        reuslt = self.mm.popular_movie(popular_query)

    def test_mockexample(self):
            self.mm.mockexample = Mock(return_value=8)
            result = self.mm.mockexample(3,5)
            self.mm.mockexample.assert_called_with(3,5)
            self.assertEqual(result, 8)
    def tearDown(self):
        self.mm.mm_close()
        
if __name__ == "__main__":
    unittest.main()