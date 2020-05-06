# MovieTweetings

# Solutions
## Solution on Hive
```bash
create table users(
userid bigint,
twitter_id bigint
) 
row format serde 'org.apache.hadoop.hive.serde2.RegexSerDe' 
with serdeproperties('input.regex'='(.*)::(.*)','output.format.string'='%1$s %2$s')
stored as textfile;

create table t_movie(
movieid bigint,
moviename string,
movietype string) 
row format serde 'org.apache.hadoop.hive.serde2.RegexSerDe' 
with serdeproperties('input.regex'='(.*)::(.*)::(.*)','output.format.string'='%1$s %2$s %3$s')
stored as textfile;

create table movies(
movieid bigint,
movie_title string,
genre string) 
row format serde 'org.apache.hadoop.hive.serde2.RegexSerDe' 
with serdeproperties('input.regex'='(.*)::(.*)::(.*)','output.format.string'='%1$s %2$s %3$s')
stored as textfile;

create table rating(
userid bigint,
movieid bigint,
rate double,
times string) 
row format serde 'org.apache.hadoop.hive.serde2.RegexSerDe' 
with serdeproperties('input.regex'='(.*)::(.*)::(.*)::(.*)','output.format.string'='%1$s %2$s %3$s %4$s')
stored as textfile;

0: jdbc:hive2://hadoop3:10000> load data local inpath "/hadoop/users.dat" into table user;
No rows affected (0.928 seconds)
0: jdbc:hive2://hadoop3:10000> load data local inpath "/hadoop/movies.dat" into table movie;
No rows affected (0.538 seconds)
0: jdbc:hive2://hadoop3:10000> load data local inpath "/hadoop/rating.dat" into table rating;
No rows affected (0.963 seconds)
0: jdbc:hive2://hadoop3:10000> 

select  a.movie_title, a.genre, substr(a.movie_title,-5,4) as years,count(b.rate) as counts, avg(b.rate) as avgrate ,tv as type
from movies a join rating b on a.movie_id=b.movie_id 
lateral view explode(split(a.type,"\\|")) tv as type;
where substr(a.movie_title,-5,4) >= (from_unixtime(b.rating_timestamp ,"%Y")-10)  
group by a.type, a.movie_title, years
order by counts desc;

```
## Solution on mysql with docker container
```bash
docker pull mysql/mysql-server:8.0.20-1.1.16
docker run --name=momenton-mysql -p 3306:3306 -d --env="MYSQL_ROOT_PASSWORD=mypassword" mysql/mysql-server:8.0.20-1.1.16

docker exec momenton-mysql -it /bin/bash
mysql -uroot -pmypassword
GRANT ALL PRIVILEGES ON *.* TO 'root'@'%';
FLUSH PRIVILEGES;

popular_queries with two steps:

create table ans as 
select a.a.genre, 
substr(a.movie_title,-5,4) as years,count(b.rate) as counts, avg(b.rate) as avgrate 
from movies a join rating b on a.movie_id=b.movie_id where substr(a.movie_title,-5,4) >= (from_unixtime(b.rating_timestamp ,"%Y")-10)
group by a.a.genre, years 
order by counts desc;

 SELECT years, sum(a.counts) as total,avg(a.avgrate) total_rates, SUBSTRING_INDEX(SUBSTRING_INDEX(a.genre,'|',help_topic_id+1),'|',-1)
AS type  FROM  ans a join mysql.help_topic  on help_topic_id < LENGTH(a.genre)-LENGTH(REPLACE(a.genre,'|',''))+1 group by type, years order by total desc;

+-------+-------+-------------+-------------+
| years | total | total_rates | type        |
+-------+-------+-------------+-------------+
| 2013  | 17898 |  6.25867583 | Action      |
| 2013  | 15471 |  6.44092968 | Thriller    |
| 2012  | 11851 |  6.87278502 | Drama       |
| 2013  | 11233 |  5.81213421 | Sci-Fi      |
| 2013  |  9671 |  6.63285172 | Adventure   |
| 2013  |  8346 |  7.30160840 | Drama       |
| 2013  |  7337 |  6.80854902 | Comedy      |
| 2012  |  7132 |  6.02381783 | Thriller    |
| 2012  |  5952 |  6.46752952 | Comedy      |
| 2013  |  5291 |  6.46378852 | Crime       |
| 2013  |  5193 |  6.76008000 | Fantasy     |
| 2012  |  4717 |  6.30013981 | Crime       |
| 2012  |  4627 |  6.25363289 | Action      |
| 2013  |  4566 |  5.76912375 | Horror      |
| 2012  |  4275 |  6.49816667 | Adventure   |
| 2011  |  3682 |  6.79580625 | Drama       |
| 2012  |  3506 |  6.93665259 | Romance     |
| 2012  |  2363 |  6.29249672 | Sci-Fi      |
| 2011  |  2303 |  6.09786077 | Thriller    |
| 2011  |  2271 |  6.52200866 | Comedy      |
| 2013  |  2225 |  7.07281029 | Romance     |
| 2010  |  2083 |  6.96931483 | Drama       |
| 2012  |  1949 |  6.95134808 | Fantasy     |
| 2012  |  1945 |  7.36405814 | History     |
| 2013  |  1790 |  7.39269000 | Animation   |
| 2013  |  1667 |  7.23111739 | Family      |
| 2012  |  1573 |  5.29625515 | Horror      |
| 2011  |  1559 |  6.19974876 | Action      |
| 2009  |  1539 |  6.91469727 | Drama       |
| 2010  |  1503 |  6.38399123 | Thriller    |
| 2010  |  1452 |  6.72004764 | Comedy      |
| 2008  |  1365 |  6.99606604 | Drama       |
| 2007  |  1254 |  7.02276581 | Drama       |
| 2012  |  1243 |  6.51457755 | Mystery     |
| 2010  |  1237 |  6.61166875 | Action      |
| 2006  |  1181 |  7.24001019 | Drama       |
| 2004  |  1021 |  7.30965811 | Drama       |
| 2011  |  1008 |  6.25043797 | Crime       |
| 2008  |  1000 |  6.50400455 | Thriller    |
| 2007  |   979 |  6.66067660 | Thriller    |
| 2009  |   978 |  6.43355425 | Thriller    |
| 2012  |   967 |  7.07734390 | Animation   |
| 2011  |   964 |  6.56288364 | Sci-Fi      |
| 2011  |   939 |  6.74311167 | Adventure   |
| 2012  |   937 |  7.36097045 | Family      |
| 2010  |   921 |  6.66612500 | Adventure   |
| 2008  |   898 |  6.83864667 | Action      |
| 2009  |   883 |  6.62385190 | Comedy      |
| 2011  |   869 |  6.08905111 | Mystery     |
| 2012  |   857 |  6.38310000 | Western     |
| 2006  |   853 |  6.63425766 | Thriller    |
| 2012  |   849 |  7.47428571 | Biography   |
| 2009  |   840 |  6.26195978 | Action      |
| 2011  |   815 |  6.93870316 | Romance     |
| 2005  |   800 |  7.03218220 | Drama       |
| 2010  |   798 |  6.73814074 | Romance     |
| 2009  |   770 |  6.64667963 | Adventure   |
| 2009  |   756 |  6.45706981 | Sci-Fi      |
| 2010  |   730 |  6.87161081 | Crime       |
| 2013  |   705 |  7.40139130 | Biography   |
| 2012  |   691 |  7.60020743 | Documentary |
| 2010  |   684 |  6.86966875 | Mystery     |
| 2011  |   663 |  5.14792653 | Horror      |
| 2007  |   620 |  7.04426867 | Crime       |
| 2013  |   608 |  6.70840588 | Mystery     |
| 2008  |   596 |  6.94537778 | Crime       |
| 2003  |   592 |  7.29967967 | Drama       |
| 2004  |   564 |  6.59708841 | Thriller    |
| 2005  |   551 |  6.40325909 | Thriller    |
| 2007  |   546 |  6.67742016 | Comedy      |
| 2008  |   546 |  6.87299219 | Comedy      |
| 2008  |   543 |  7.08127700 | Romance     |
| 2003  |   541 |  7.03930667 | Thriller    |
| 2004  |   534 |  6.86390571 | Comedy      |
| 2007  |   520 |  6.72375077 | Action      |
| 2011  |   510 |  7.50451613 | Biography   |
| 2003  |   509 |  6.96005769 | Action      |
| 2009  |   500 |  6.97627386 | Romance     |
| 2004  |   468 |  7.02087260 | Romance     |
| 2009  |   468 |  6.47717167 | Mystery     |
| 2010  |   464 |  6.71028049 | Fantasy     |
| 2010  |   462 |  6.01090645 | Sci-Fi      |
| 2012  |   451 |  6.55704348 | War         |
| 2005  |   446 |  6.46476735 | Action      |
| 2011  |   445 |  6.11173333 | Fantasy     |
| 2006  |   438 |  6.84976947 | Comedy      |
| 2005  |   433 |  6.54007414 | Comedy      |
| 2004  |   432 |  6.65183265 | Action      |
| 2012  |   429 |  8.09586471 | Music       |
| 2009  |   429 |  6.63664070 | Crime       |
| 2011  |   418 |  7.06116923 | Family      |
| 2008  |   416 |  6.83566222 | Adventure   |
| 2012  |   411 |  6.93445000 | Musical     |
| 2006  |   411 |  6.95803208 | Crime       |
| 2010  |   404 |  6.78111471 | Family      |
| 2010  |   403 |  5.55109425 | Horror      |
| 2006  |   401 |  6.69202041 | Action      |
| 2009  |   386 |  6.34288889 | Fantasy     |
| 2005  |   384 |  7.14671667 | Crime       |
| 2003  |   384 |  7.16775604 | Comedy      |
| 2003  |   377 |  7.47423243 | Adventure   |
| 2007  |   373 |  7.03052308 | Mystery     |
| 2008  |   372 |  6.22427714 | Sci-Fi      |
| 2005  |   363 |  6.49656818 | Adventure   |
| 2006  |   359 |  7.15281556 | Adventure   |
| 2013  |   347 |  5.24250000 | Western     |
| 2010  |   346 |  7.20072647 | Biography   |
| 2006  |   343 |  7.17932105 | Romance     |
| 2010  |   332 |  6.87464286 | Animation   |
| 2006  |   331 |  7.46247941 | Fantasy     |
| 2009  |   322 |  5.86654384 | Horror      |
| 2005  |   314 |  6.91072958 | Romance     |
| 2004  |   308 |  6.71748148 | Sci-Fi      |
| 2011  |   308 |  7.82789111 | Documentary |
| 2011  |   306 |  7.42092414 | Sport       |
| 2007  |   304 |  6.36700308 | Horror      |
| 2007  |   300 |  6.79913333 | Adventure   |
| 2003  |   298 |  7.39183542 | Crime       |
| 2006  |   287 |  6.70956667 | Mystery     |
| 2004  |   286 |  7.07436563 | Adventure   |
| 2013  |   283 |  8.04375833 | Sport       |
| 2004  |   275 |  6.73503158 | Crime       |
| 2007  |   272 |  6.79578356 | Romance     |
| 2007  |   256 |  7.22358889 | Sci-Fi      |
| 2005  |   241 |  6.49941154 | Fantasy     |
| 2003  |   234 |  6.94520952 | Fantasy     |
| 2013  |   228 |  8.24394035 | Documentary |
| 2007  |   221 |  6.58726667 | Fantasy     |
| 2011  |   220 |  7.35629333 | Animation   |
| 2007  |   218 |  7.53030435 | Biography   |
| 2005  |   214 |  6.34204571 | Mystery     |
```

## Some stats

Metric | Value
--- | ---
Total number of ratings                 | 821,108
Number of unique users                  | 60,729
Number of unique items                  | 34,623
These stats were last autocalculated on Tue Dec 10 01:23:34 CET 2019  ([more stats here](./stats.md))

## A Movie Rating Dataset Collected From Twitter

MovieTweetings is a dataset consisting of ratings on movies that were contained in well-structured tweets on Twitter. This dataset is the result of research conducted by [Simon Dooms] (http://scholar.google.be/citations?user=owaD8qkAAAAJ) (Ghent University, Belgium) and has been presented on the [CrowdRec 2013 workshop](http://crowdrec2013.noahlab.com.hk) which is co-located with the [ACM RecSys 2013 conference](http://recsys.acm.org/recsys13/). Please cite the [corresponding paper](http://crowdrec2013.noahlab.com.hk/papers/crowdrec2013_Dooms.pdf) if you make use of this dataset. The presented slides can be found [on slideshare] (http://www.slideshare.net/simondooms/movie-tweetings-a-movie-rating-dataset-collected-from-twitter).

Follow us on Twitter ([@mvtweetings](https://twitter.com/mvtweetings)) for the latest news, info and fun facts about the dataset.

Bibtex: *@conference{Dooms13crowdrec, author = {Dooms, Simon and De Pessemier, Toon and Martens, Luc}, title = {MovieTweetings: a Movie Rating Dataset Collected From Twitter}, booktitle = {Workshop on Crowdsourcing and Human Computation for Recommender Systems, CrowdRec at RecSys 2013}, year = {2013} }*

An excerpt of the abstract of the paper:

> Public rating datasets, like MovieLens or Netflix, have long been popular and widely used in the recommender systems domain for experimentation and comparison. More and more however they are becoming outdated and fail to incorporate new and relevant items. In our work, we tap into the vast availability of social media and construct a new movie rating dataset 'MovieTweetings' based on public and well-structured tweets. With the addition of around 500 new ratings per day we believe this dataset can be very useful as an always up-to-date and natural rating dataset for movie recommenders.

The goal of this dataset is to provide the RecSys community with a live, natural and always up-to-date movie ratings dataset. The dataset will be updated as much as possible to incorporate rating data from the newest tweets available. The earliest rating contained in this dataset is from 28 Feb 2013, and I pledge to keep this system up and running for as long as I can. Note however that this dataset is automatically gathered and therefore depending on the continuation of the IMDb apps and Twitter API.

Don't hesitate to contact me for any comments, questions or proposals you might have.

## Ratings from Twitter

As said, this dataset consists of ratings extracted from tweets. To be able to extract the ratings, we query the Twitter API for well-structured tweets. We have found such tweets originating from the social rating widget available in IMDb apps. While rating movies, in these apps, a well-structured tweet is proposed of the form:

*"I rated The Matrix 9/10 http://www.imdb.com/title/tt0133093/ #IMDb"*

On a daily basis the Twitter API is queried for the term **"I rated #IMDb"**. Through a series of regular expressions, relevant information such as user, movie and rating is extracted, and cross-referenced with the according IMDb page to provide also genre metadata. The numeric IMDb identifier was adopted as item id to facilitate additional metadata enrichment and guarantee movie uniqueness. For example, for the above tweet the item id would be **"0133093"** which allows to infer the corresponding IMDb page link (add *http://www.imdb.com/title/tt*). The user id simply ranges from 1 to the number of users.

## The dataset

Since this dataset will be updated regularly we have structured the dataset in different folders /latest and /snapshots. The /latest folder will always contain the complete dataset as available at the time of the commit, while the /snapshots contain fixed portions of the dataset to allow experimentation and reproducibility of research. The *10K* snapshot represents the ratings from the first 10,000 collected tweets, *20K* the first 20,000, and so on.

The dataset files are modeled after the [MovieLens dataset] (http://www.grouplens.org/node/73) to make them as interchangeable as possible. There are three files: **users.dat**, **items.dat** and **ratings.dat**.

### users.dat

Contains the mapping of the users ids on their true Twitter id in the following format: *userid::twitter_id*. For example:

1::177651718

We provide the Twitter id and not the Twitter @handle (username) because while the @handle can be changed, the id will always remain the same. Conversions from Twitter id to @handle can be done by means of an online tool like [Tweeterid] (http://tweeterid.com/) or simply through the Twitter API itself. The mapping provided here again facilitates additional metadata enrichment.

### items.dat

Contains the items (i.e., movies) that were rated in the tweets, together with their genre metadata in the following format: *movie_id::movie_title (movie_year)::genre|genre|genre*. For example:

0110912::Pulp Fiction (1994)::Crime|Thriller

The file is UTF-8 encoded to deal with the many foreign movie titles contained in tweets.

### ratings.dat

In this file the extracted ratings are stored in the following format: *user_id::movie_id::rating::rating_timestamp*. For example:

14927::0110912::9::1375657563

The ratings contained in the tweets are scaled from 0 to 10, as is the norm on the IMDb platform. To prevent information loss we have chosen to not down-scale this rating value, so all rating values of this dataset are contained in the interval [0,10].

## Publications using this dataset
- [MovieTweetings: a Movie Rating Dataset Collected From Twitter](http://crowdrec2013.noahlab.com.hk/papers/crowdrec2013_Dooms.pdf)
- [Probabilistic Neighborhood Selection in Collaborative Filtering Systems] (http://people.stern.nyu.edu/padamopo/Probabilistic%20Neighborhood%20Selection%20in%20Collaborative%20Filtering%20Systems%20-%20Working%20Paper.pdf)
- [Harvesting movie ratings from structured data in social media](http://dl.acm.org/citation.cfm?id=2559862)
- [Social Popularity based SVD++ Recommender System](http://research.ijcaonline.org/volume87/number14/pxc3894033.pdf)
- [Cold-Start Active Learning with Robust Ordinal Matrix Factorization](http://jmlr.org/proceedings/papers/v32/houlsby14-supp.zip)
- [SemanticSVD++: Incorporating Semantic Taste Evolution for Predicting Ratings](http://www.lancaster.ac.uk/staff/rowem/files/mrowe-wi2014.pdf)
- [Estimating the Value of Multi-Dimensional Data Sets in Context-based Recommender Systems](http://ceur-ws.org/Vol-1247/recsys14_poster7.pdf)
- [An Extended Data Model Format for Composite Recommendation](http://ceur-ws.org/Vol-1247/recsys14_poster20.pdf)
- [Improving IMDb Movie Recommendations with Interactive Settings and Filters](http://ceur-ws.org/Vol-1247/recsys14_poster19.pdf)
- [ConcertTweets: A Multi-Dimensional Data Set for Recommender Systems Research](http://people.stern.nyu.edu/padamopo/data/ConcertTweets.pdf)
- [On over-specialization and concentration bias of recommendations: probabilistic neighborhood selection in collaborative filtering systems](http://dl.acm.org/citation.cfm?id=2645752)
- [Recommender systems challenge 2014](http://dl.acm.org/citation.cfm?id=2645779)
- [CrowdRec project](http://crowdrec.eu/)
- [Comparing a Social Robot and a Mobile Application for Movie Recommendation: A Pilot Study](http://ceur-ws.org/Vol-1382/paper5.pdf)
- [Augmenting a Feature Set of Movies Using Linked Open Data](https://www.csw.inf.fu-berlin.de/ruleml2015-ceur/paper16.pdf)
- [Adaptive User Engagement Evaluation via Multi-task Learning](http://dl.acm.org/citation.cfm?id=2767785)
- [Crowd Source Movie Ratings Based on Twitter Data Analytics](http://csus-dspace.calstate.edu/bitstream/handle/10211.3/138435/2015HolikattiPriya.pdf)
- [Combining similarity and sentiment in opinion mining for product recommendation](http://link.springer.com/article/10.1007/s10844-015-0379-y)
- [7 Relevance of Social Data in Video Recommendation](https://comcast.app.box.com/recsystv-2015-xu)
- [Positive-Unlabeled Learning in Streaming Networks](http://www.kdd.org/kdd2016/subtopic/view/positive-unlabeled-learning-in-streaming-networks)
- [Unexpectedness and Non-Obviousness in Recommendation Technologies and Their Impact on Consumer Decision Making](http://people.stern.nyu.edu/padamopo/thesis_draft.pdf)
- [Corporate Smart Content Evaluation](http://www.diss.fu-berlin.de/docs/servlets/MCRFileNodeServlet/FUDOCS_derivate_000000006523/CSCStudie2016.pdf)
- [(Book!) Mastering Python Data Analysis](https://www.packtpub.com/big-data-and-business-intelligence/mastering-python-data-analysis)
- [An Integrated Recommender Algorithm for Rating Prediction](https://arxiv.org/pdf/1608.02021.pdf)
- [Designing Human-Centered Collective Intelligence](http://epublications.marquette.edu/cgi/viewcontent.cgi?article=1678&context=dissertations_mu)


[Contact me](http://twitter.com/sidooms) if you know of any work (maybe your own?) that can be added to this list!

