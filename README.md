# Logs Analysis

## Project Description
In this project, I have written a python module that connects to a back-end database of a newspaper website and produces a report about the popularity of articles and authors as well as the behavior of the users on the website. The database contains three tables:
- authors: information about the authors of the articles including name and bio.
- articles: information about the articles including title, lead, body, and time.
- log: information about accessing the website such as ip, status, and the path to the resources/articles.    

The goals is to answer the following three questions using single queries:

**1- What are the most popular three articles of all time? Which articles have been accessed the most?**  

**2- Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views?**
  
**3- On which days did more than 1% of requests lead to errors?**

## Requirements
To run the code, you'll need the followings installed on your machine:  

Python3  
PostgreSQL

You also need to download the database schema and data using the following this [link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)

To make sure the results can be fully reproduced, it is recommended to setup a virtual machine using [VirtualBox](https://www.vagrantup.com/) and [Vagrant](https://www.virtualbox.org/wiki/). This step is optional but highly recommended. You can follow the remaining of this section once you install VirtualBox and Vagrant.  
Use Vagrantfile provided in this project (the owners of this code are @forbiddenvoid @karlud @asparr from Udacity) to setup your environment. Copy this file in your vagrant directory and run:

    vagrant up 

after that, run 

    vagrant ssh 

to login to your virtual machine.

## Database Set-Up
Copy newsdata.sql into your vagrant directory and run the following command:

    psql -d news -f newsdata.sql

## How to Run
To run the code and prepare the report, you can do:

    python log_analysis.py

A sample output is provided in "sample_output.txt" file

## Views
Each question is handled using a separate function in the module. Before you run the code, first create a view using the following command:

    create view status_date as select status, date(time) as date from log;



