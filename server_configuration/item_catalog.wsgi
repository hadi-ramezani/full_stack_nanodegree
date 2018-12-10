import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/server_configuration/item_catalog/")

from application import app as application
application.secret_key = 'super_secret_key'
