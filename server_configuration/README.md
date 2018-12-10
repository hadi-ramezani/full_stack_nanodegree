# Linux Server Configuration

## Project Description
In this project, I took a baseline installation of a Linux server on AWS (basic Lightsail server) and configured it to host 
my item catalog application. The configurations include installation of the necessary packages, apache and database servers,
and changes to the firewall settings. The source-code for the item catalog applications is provided under the "item_catalog"
directory. 

## Server Information
IP address: 35.170.61.8
URL: http://ec2-35-170-61-8.compute-1.amazonaws.com/

## Summary of Software Installed
Update the packages installed on the machine:

	sudo apt-get update
	sudo apt-get upgrade

It is helpful to install the latest version of [Anaconda](https://www.anaconda.com/download/#linux). Once you download/transfer 
the installer file to the server, you can navigate to the location that the installer file is saved and run:

	bash <the name of the installer file>

Follow the instructions and it will install Anaconda for you. You'll need pip to easily install python packages. Installing Anaconda 
will install pip for you as well. Alternatively, you can install python-pip by running: 

	sudo apt install python-pip

Install git:

	sudo apt-get install git

Install other python packages necessary to run the application:

	sudo pip install flask
	sudo pip install sqlalchemy
	sudo pip install oauth2client
	sudo pip install requests
	sudo pip install httplib2

Install apache server and mod-wsgi to be able to run the python application on apache server:

	sudo apt-get install apache2
	sudo apt-get install libapache2-mod-wsgi	

Install postgresql server:

	sudo apt-get install postgresql postgresql-contrib

Once the installation is complete, create a postgresql user:

	sudo -u postgres createuser -P itemcatalog

Then, create an empty database:

	sudo -u postgres createdb -O itemcatalog itemcatalog

The source code for the application has been updated to work with postgresql instead of sqlite.

## Summary of Configurations Made

### Add the user "grader" with sudo access
To add the use grader, run the command:
	
	sudo adduser grader

To give the grader user sudo access, run the command:

	sudo nano /etc/sudoers.d/grader

Then, add the line:

	grader ALL=(ALL) NOPASSWD:ALL

to that file and save the changes.

In order to connect as grader user, you'll need a private key.


### Host ssh on non-default 2200 port
To change the ssh port from the standard 22 to the non-default 2200 port, change the line "Port 22" to "Port 2200"
in the file /etc/ssh/sshd_config.

### Disable remote login of the root user
To disable remote login of the root user, change the line "PermitRootLogin prohibit-password" in the file /etc/ssh/sshd_config
to "PermitRootLogin no"

### Enforce key-based authentication
To disable password-based authentication and enforce key-based authentication, uncomment and change the line "PasswordAuthentication yes"
to "PasswordAuthentication no" in the file /etc/ssh/sshd_config

In order for ssh-related changes to take place, restart the ssh service using the command:

	sudo service ssh restart  


### Configure firewall setting using ufw
Run the following command to make sure ufw is disabled:

	sudo ufw status

Run the following command to block all incoming traffic:

	sudo ufw default deny incoming

Run the following command to allow outgoing traffic:

	sudo ufw default allow outgoing

Since ssh now uses port 2200, open this port using the command:

	sudo ufw allow 2200/tcp

Allow http requests on port 80:

	sudo ufw allow www

Allow NTPon port 123:

	sudo ufw allow ntp

Now activate the firewall:

	sudo ufw enable

Check the status and the ports using the command:

	sudo ufw status

### Update google authentication configurations
In order for the users to be able to login to the app using their google account, login to your google API console and 
update the "Authorized domain" field along with "Authorized JavaScript origins" and "Authorized redirect URIs". Then, you need to update 
client_secrets.json file accordingly.


### Configure the apache server
To configure the apache server, place the file item_catalog.conf under /etc/apache2/sites-enabled/.

Then, disable the default host using the command:

	sudo a2dissite 000-default.conf

To use the configuration file that you copied, run:

	sudo a2ensite item_catalog.conf
	sudo service apache reload


The application should now be accessible on your browser using "http://35.170.61.8.xip.io/", "http://35.170.61.8" addresses.