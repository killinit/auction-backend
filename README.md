# Django Demo Backend

Django demo backend featuring a RESTfull Api and WebSockets push notifications:

* The RESTful web api was developed with [django-rest-framework](http://www.django-rest-framework.org/). 
* The WebSockets integration was developed using the recent [django-channels](https://github.com/andrewgodwin/channels.git)
  package.

A demo frontend developed with angular 2 is available to integrate with this backend: 
[auction-frontend-web](https://github.com/luissalgadofreire/auction-frontend-web.git).

Details of the environment:

- Nginx as reverse proxy for HTTP and Websockets connections (listening on port 80 and passing to Daphne)
- Daphne (an ASGI HTTP/Websockets server listening on port 8000)
- Python 3.5.1 (installed through Miniconda, to allow for data science libraries)
- Jupyter Notebook Server (installed with Miniconda, and listening on port 8888)
- Django (including Django Channels and Daphne, allowing for Websockets connections)
- Celery (asynchronous task queue/job queue manager) 
- Flower as a web frontend for Celery (listening on port 5555)
- RabbitMQ (serving as Celery's message broker, listening on port 5672 and 15672)
- Redis (serving as Django Channels' backend and as Celery's results backend, listening on port 6379)
- Memcached for caching (listening on port 11211)
- PostgreSQL (listening on port 5432)


## Setup instructions for local deployment - dev

**Note 1**: the below instructions are for Windows. You might need to adjust them for Linux or Mac.

1. Create new docker-machine (locally): ``docker-machine create -d virtualbox auction-backend-dev``
2. List docker-machines: ``docker-machine ls``
3. Activate docker-machine: ``eval $(docker-machine env auction-backend-dev)``
4. Adjust all IP's within file ``.env_dev_django`` to the IP of the virtual machine
5. (Optional) Adjust remaining environment values within file ``.env_dev_django`` and ``.env_dev_rabbitmq``
6. (Optional) Adjust the Python packages to install using pip in file ``web/requirements-pip.txt``
7. (Optional) Adjust the Python packages to install using conda (scientific packages) in file ``web/requirements-conda.txt``
8. Build images: ``docker-compose build``
9. Start services: ``docker-compose up -d``
10. Open web container's terminal: ``docker exec -i -t auctionbackend_web_1 /bin/bash``
11. Create django superuser: ``python src/manage.py createsuperuser``
12. Load fixtures (initial demo data): ``python src/manage.py loaddata demo``
13. Open Django: `docker-machine ip auction-backend-dev` - grap IP and view django in your browser (e.g. 192.168.99.100)
14. Open Jupyter Notebook: using the same IP, append port 8888 and view jupyter notebook in your browser (e.g. 192.168.99.100:8888)
15. Open Flower: using the same IP, append port 5555 to view Flower in your browser (e.g. 192.168.99.100:5555)
16. Open RabbitMQ frontend: using the same IP, append port 15672 and view RabbitMQ in your browser (e.g. 192.168.99.100:15672)


## Setup instructions for remote deployment (AWS or DigitalOcean) - staging
 
1. Create an account for [Amazon Web Services](https://aws.amazon.com/free/?sc_channel=PS&sc_campaign=acquisition_PT&sc_publisher=google&sc_medium=english_cloud_computing_hv_b&sc_content=aws_core_e&sc_detail=aws&sc_category=cloud_computing_hv&sc_segment=118649773164&sc_matchtype=e&sc_country=PT&s_kwcid=AL!4422!3!118649773164!e!!g!!aws&ef_id=VyHV1QAABcBDs8G9:20160823141601:s) 
  or [DigitalOcean](https://www.digitalocean.com/?refcode=bc4d24968943&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=CopyPaste).
2. Create new docker-machine (aws) [replace access-key and secret-key with your own]: ``docker-machine create -d amazonec2 --amazonec2-access-key XZXZXZXZXZXZXZXZX --amazonec2-secret-key XZXZXZXZXZXZXZXZXZX --amazonec2-region eu-west-1 --amazonec2-vpc-id vpc-f0836595 auction-backend-staging``
3. or Create new docker-machine (digitalocean) [replace access-token with your own]: ``docker-machine create -d digitalocean --digitalocean-access-token=XZXZXZXZXZXZXZXZX auction-backend-staging``
4. List docker-machines: ``docker-machine ls``
5. Activate docker-machine: ``eval $(docker-machine env auction-backend-staging)``
6. Copy files ``.env_dev_django`` and ``.env_dev_django`` and rename them ``.env_prod_django`` and ``.env_prod_django``
7. Adjust all IP's within file ``.env_prod_django`` to the IP of the virtual machine
8. (Optional) Adjust remaining environment values within file ``.env_prod_django`` and ``.env_prod_rabbitmq``
9. (Optional) Adjust the Python packages to install using pip in file ``web/requirements-pip.txt``
10. (Optional) Adjust the Python packages to install using conda (scientific packages) in file ``web/requirements-conda.txt``
11. Build images: ``docker-compose build``
12. Start services: ``docker-compose -f production.yml up -d``
13. Open web container's terminal: ``docker exec -i -t auctionbackend_web_1 /bin/bash``
14. Create django superuser: ``python src/manage.py createsuperuser``
15. Load fixtures: ``python src/manage.py loaddata demo``
16. Open Django - `docker-machine ip auction-backend-staging` - grap IP and view django in your browser (e.g. 194.187.71.89)
17. Open Jupyter Notebook: using the same IP, append port 8888 to view jupyter notebook in your browser (e.g. 194.187.71.89:8888)
18. Open Flower: using the same IP, append port 5555 to view Flower in your browser (e.g. 194.187.71.89:5555)
19. Open RabbitMQ frontend: using the same IP, append port 15672 and view RabbitMQ in your browser (e.g. 194.187.71.89:15672)