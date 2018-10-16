#! /usr/bin/env python3

import psycopg2

DBNAME = "news"


def get_most_popular_articles():
    """Compute the three most popular articles and print their title and the
    number of views

    :return: None
    """
    print("Calculating three most popular articles of all time")
    db = psycopg2.connect(database=DBNAME)

    c = db.cursor()
    c.execute("""
    SELECT articles.title, count(*) AS hit from log, articles
    WHERE '/article/' || articles.slug = log.path 
    GROUP BY articles.title
    ORDER BY hit DESC
    LIMIT 3
    """)

    articles = c.fetchall()
    for i, article in enumerate(articles):
        print("{0}. '{1}' --- {2} views".format(i + 1, article[0], article[1]))


def get_most_popular_authors():
    """Compute the most popular article authors and print their names along
    with the number of views for their articles

    :return: None
    """
    print("Calculating three most popular articles authors of all time")
    db = psycopg2.connect(database=DBNAME)

    c = db.cursor()
    c.execute("""
    SELECT authors.name, count(*) AS hit from articles, authors, log
    WHERE  articles.author = authors.id and '/article/' || articles.slug = log.path 
    GROUP BY authors.name 
    ORDER BY hit DESC
    LIMIT 3
    """)

    authors = c.fetchall()
    for i, author in enumerate(authors, 1):
        print("{0}. '{1}' --- {2} views".format(i, author[0], author[1]))


def get_high_error_days():
    """Calculate the rate of error for each days and print them if the rate is
    greater than 1%

    :return: None
    """
    # create view status_days as select status, date_part('day', time) as day from log;
    print("Finding days with more than 1% error rate")

    db = psycopg2.connect(database=DBNAME)

    c = db.cursor()
    c.execute("""
    SELECT ok_table.day, (error_table.error_count::decimal/(ok_table.ok_count+error_table.error_count))*100 
    AS rate  
    FROM (select day, count(*) AS ok_count 
    FROM status_days 
    WHERE status='200 OK' 
    GROUP BY day) AS ok_table,  
    (SELECT day, count(*) AS error_count 
    FROM status_days 
    WHERE status='404 NOT FOUND' 
    GROUP BY day) AS error_table 
    WHERE ok_table.day = error_table.day 
    ORDER BY rate DESC 
    """)

    days_errors = c.fetchall()
    for item in days_errors:
        if item[1] > 1:
            print("The error rate on July {0}, 2016 was {1:.2f}%".format(int(item[0]), item[1]))


def main():
    """Make calls to other functions in the module to prepare the report

    :return: None
    """
    get_most_popular_articles()
    print("#######################################################")
    get_most_popular_authors()
    print("#######################################################")
    get_high_error_days()


if __name__ == '__main__':
    main()
