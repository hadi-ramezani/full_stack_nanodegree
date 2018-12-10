# Item Catalog

## Project Description
In this project, I have developed an application that provides a list of items within a variety of categories (similar to
the Amazon website for example). This application provides a user registration and authentication system. Unregistered
users are able to view all items and categories on the website. Registered (logged in) users are able to create, edit,
and edit new categories and items. Only the creator of each item and category have the ability to make changes to the
items. Everyone can see all items and categories.

## Requirements
To run the code, you'll need the followings installed on your machine:

Python3
flask
sqlalchemy
oauth2client

To make sure the results can be fully reproduced, it is recommended to setup a virtual machine using
[VirtualBox](https://www.vagrantup.com/) and [Vagrant](https://www.virtualbox.org/wiki/). This step is optional but
highly recommended. You can follow the remaining of this section once you install VirtualBox and Vagrant.
Use Vagrantfile provided in this project (the owners of this code are @forbiddenvoid @karlud @asparr from Udacity) to
setup your environment. Copy this file in your vagrant directory and run:

    vagrant up

after that, run

    vagrant ssh

to login to your virtual machine.

## Database Set-Up
To get started, I have prepared a file called "some_items.py". This file adds a user (myself) along with a number of categories
and items. Note that the description of each items are just the generic definitions from Wikipedia (https://www.wikipedia.org/).
This file will create an initial database for you so that the website won't be empty when you load it. Once the
website is loaded you can make modifications and add new categories/items. To create the database run the following command:

    python some_items.py

## How to Run
In order to enable user authentication/authorization using google accounts, you need a "client_secrets.json" file that
contains your client_id, and client_secrent among other information.

To run the website, navigate to the project directory and run:

    python application.py

Then go to your browser (any browser should work fine) and enter: localhost:8000


## References
The codes for the styling and authentication have been adapted from the instructions in the Nanodegree videos.