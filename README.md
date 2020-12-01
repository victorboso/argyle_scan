# scan_upwork
## Installation

1 - Open a terminal [1]

2 - Pull the image and start the container
```
sudo docker pull scrapinghub/splash
sudo docker run -it -p 8050:8050 --rm scrapinghub/splash --max-timeout 300
```
*Splash is now available at 0.0.0.0 at port 8050 (http)*

3 - Open a terminal [2]

4 - Create a virtualenv, active the env, install the dependencies
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

5 - Create a new folder called "scrapyd" into the root of project, with the other folders ["scrapydweb", "scan"...]
```
mkdir scrapyd
cd scrapyd
mkdir logs
scrapyd
```

6 - Open a terminal [3]

7 - Go to the root of project, activate the virtualenv
```
cd <to/path/of/project>
source venv/bin/activate
```

8 - Into the file "scrapydweb_settings_v10.py", change the variable "SCRAPYD_LOGS_DIR" to the path that you created before and 
change the variable "SCRAPY_PROJECTS_DIR" to the root path, where the "scan", "scrapydweb" and "scrapyd" folders are located
```
cd scrapydweb
nano scrapydweb_settings_v10.py
```

9 - Start the application
*you need to be in the "scrapydweb" folder*
```
scrapydweb
```
*Scrapydweb is now available at 0.0.0.0 at port 5000 (http)*

10 - Open your browser
```
http://localhost:5000
```
*username: user*
*password: pass*

11 - Into the application, now, we'll deploy our first project
* Menu on the left, click on "Deploy project"
* Click on "Package and Deploy"
* Select on the menu "spider" our spider, called "upwork"
* Enable "settings & arguments"
* At the box "additional", add the parameter "-a da_user="<here-we-put-the-device-authorization-manually-yet>" -o test.json"
* Click on "Check CMD" and then "Run spider"

12 - Wait a few seconds and the results will be in the "scan" folder



**Obs**

Choices:
* Scrapy
  * An open source framework
  * Fast
  * Simple
  * Excellent architecture
  * Easy to implement any middlawares, pipelines, extensions...
  * Excellent documentation
  
* Scrapyd + Scrapyd-client
  * Easy to deploy and run Scrapy spiders
  * We can optimize our process and scale with docker, like [AWS ECS + Spots] with the costs very cheap
  * We managed to create several projects and version each one
  * Easy to maintain
  * It works with http 
  * Allows us to schedule our crawler
  * With the API HTTP, we can control all the spiders, like [List jobs, cancel, delete]...
  
* Scrapydweb
  * We can see
    * log analysis
    * Stats collection
    * Progress visualization
  * Deploy our project
  * Send message and notification [Email, slack...]
  * Manage the project
  * CPU and Memory each one Node [Scrapyd]
  
  
**Nice to have**
* Implement: Scrapoxy
  * It starts a pool of proxies to relay our requests
  * Crawl without blacklist
  * Easy to implement
* Integration with Database
* Add pipeline to refactor all the data
  
