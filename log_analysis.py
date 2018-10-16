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
    c.execute("select articles.title, count(*) as hit from log, articles "
              "where substring(log.path, 10) = articles.slug "
              "group by articles.title order by hit desc limit 3")

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
    c.execute("select authors.name, count(*) as hit from articles, authors, log"
              " where  articles.author = authors.id and substring(log.path, 10) "
              "= articles.slug group by authors.name order by hit desc limit 3")

    authors = c.fetchall()
    for i, author in enumerate(authors):
        print("{0}. '{1}' --- {2} views".format(i + 1, author[0], author[1]))


def get_high_error_days():
    """Calculate the rate of error for each days and print them if the rate is
    greater than 1%

    :return: None
    """

    # create view status_days as select status, date_part('day', time) as day from log;
    print("Finding days with more than 1% error rate")

    db = psycopg2.connect(database=DBNAME)

    c = db.cursor()
    c.execute("select ok_table.day, (error_table.error_count::decimal/ok_table.ok_count)*100"
              " as rate from (select day, count(*) as ok_count from status_days "
              "where status='200 OK' group by day) as ok_table, "
              "(select day, count(*) as error_count from status_days "
              "where status='404 NOT FOUND' group by day)"
              " as error_table where ok_table.day = error_table.day order by rate desc")

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
