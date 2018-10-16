#! /usr/bin/env python3

import psycopg2

DBNAME = "news"


def get_query_results(database_name, query):
    """A helper function to connect to a database, make a query and return the results

    :param database_name: the name of the database
    :param query: the text of the query
    :return: the query results
    """
    db = psycopg2.connect(database=database_name)

    c = db.cursor()
    c.execute(query)

    return c.fetchall()


def get_most_popular_articles():
    """Compute the three most popular articles and print their title and the
    number of views

    :return: None
    """
    print("Calculating three most popular articles of all time")

    query = """
    SELECT articles.title, count(*) AS hit from log, articles
    WHERE '/article/' || articles.slug = log.path 
    GROUP BY articles.title
    ORDER BY hit DESC
    LIMIT 3
    """
    articles = get_query_results(DBNAME, query)

    for i, (title, view) in enumerate(articles):
        print("{0}. '{1}' --- {2} views".format(i + 1, title, view))


def get_most_popular_authors():
    """Compute the most popular article authors and print their names along
    with the number of views for their articles

    :return: None
    """
    print("Calculating three most popular articles authors of all time")

    query = """
    SELECT authors.name, count(*) AS hit from articles, authors, log
    WHERE  articles.author = authors.id and '/article/' || articles.slug = log.path 
    GROUP BY authors.name 
    ORDER BY hit DESC
    LIMIT 3
    """
    authors = get_query_results(DBNAME, query)

    for i, author in enumerate(authors, 1):
        print("{0}. '{1}' --- {2} views".format(i, author[0], author[1]))


def get_high_error_days():
    """Calculate the rate of error for each days and print them if the rate is
    greater than 1%

    :return: None
    """
    # create view status_days as select status, date_part('day', time) as day from log;
    print("Finding days with more than 1% error rate")
    query = """
    SELECT date, rate FROM 
    (SELECT ok_table.date, (error_table.error_count::decimal/(ok_table.ok_count+error_table.error_count))*100 
    AS rate  
    FROM (select date, count(*) AS ok_count 
    FROM status_date 
    WHERE status='200 OK' 
    GROUP BY date) AS ok_table,  
    (SELECT date, count(*) AS error_count 
    FROM status_date 
    WHERE status='404 NOT FOUND' 
    GROUP BY date) AS error_table 
    WHERE ok_table.date = error_table.date) AS rates_table 
    WHERE rate >= 1
    """
    date_errors = get_query_results(DBNAME, query)

    for (date, error) in date_errors:
        print("The error rate on {0} was {1:.2f}%".format(date, error))


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
