############################## ScrapydWeb #####################################
# Setting SCRAPYDWEB_BIND to '0.0.0.0' or IP-OF-CURRENT-HOST would make
# ScrapydWeb server visible externally, otherwise, set it to '127.0.0.1'.
# The default is '0.0.0.0'.
SCRAPYDWEB_BIND = '0.0.0.0'
# Accept connections on the specified port, the default is 5000.
SCRAPYDWEB_PORT = 5000

# The default is False, set it to True to enable basic auth for web UI.
ENABLE_AUTH = True
# In order to enable basic auth, both USERNAME and PASSWORD should be non-empty strings.
USERNAME = 'user'
PASSWORD = 'pass'


############################## Scrapy #########################################
# ScrapydWeb is able to locate projects in the SCRAPY_PROJECTS_DIR,
# so that you can simply select a project to deploy, instead of eggifying it in advance.
# e.g., 'C:/Users/username/myprojects/' or '/home/username/myprojects/'
SCRAPY_PROJECTS_DIR = '/Users/victorboso/Documents/dev/argyle/web_scraping/'


############################## Scrapyd ########################################
# Make sure that [Scrapyd](https://github.com/scrapy/scrapyd) has been installed
# and started on all of your hosts.
# Note that for remote access, you have to manually set 'bind_address = 0.0.0.0'
# in the configuration file of Scrapyd and restart Scrapyd to make it visible externally.
# Check out 'https://scrapyd.readthedocs.io/en/latest/config.html#example-configuration-file' for more info.
# ------------------------------ Chinese --------------------------------------
#  [Scrapyd](https://github.com/scrapy/scrapyd)
#  Scrapyd Scrapyd  'bind_address = 0.0.0.0' Scrapyd
#  https://scrapyd.readthedocs.io/en/latest/config.html#example-configuration-file

# - the string format: username:password@ip:port#group
#   - The default port would be 6800 if not provided,
#   - Both basic auth and group are optional.
#   - e.g., '127.0.0.1' or 'username:password@192.168.123.123:6801#group'
# - the tuple format: (username, password, ip, port, group)
#   - When the username, password, or group is too complicated (e.g., contains ':@#'),
#   - or if ScrapydWeb fails to parse the string format passed in,
#   - it's recommended to pass in a tuple of 5 elements.
#   - e.g., ('', '', '127.0.0.1', '', '') or ('username', 'password', '192.168.123.123', '6801', 'group')
SCRAPYD_SERVERS = [
    'localhost:6800',# localhost 
    # 'username:password@localhost:6801#group',
    # ('username', 'password', 'localhost', '6801', 'group'),
]

# If the IP part of a Scrapyd server is added as '127.0.0.1' in the SCRAPYD_SERVERS above,
# ScrapydWeb would try to read Scrapy logs directly from disk, instead of making a request
# to the Scrapyd server.
# Check out this link to find out where the Scrapy logs are stored:
# https://scrapyd.readthedocs.io/en/stable/config.html#logs-dir
# e.g., 'C:/Users/username/logs/' or '/home/username/logs/'
SCRAPYD_LOGS_DIR = 'path to put your logs'
#EX: SCRAPYD_LOGS_DIR = '/Users/victorboso/Documents/dev/argyle/web_scraping/scrapyd/logs/'
