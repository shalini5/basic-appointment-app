Application to provide notable POST and GET APIs.

## Development
Run `docker-compose up -d --build` to build the docker images.
Run `docker ps` to make sure there are two containers running:

`basic-notable-app_notable_1`
`basic-notable-app_notable-db_1`


 ## Test
 Run `docker-compose exec notable python manage.py test` to run tests under `services/notable/project/tests`.
 
 ## Other Commands 
* To apply the model to the database: `docker-compose exec notable python manage.py recreate_db`
* To populate the database with some initial data: `docker-compose exec notable python manage.py seed_db`


## Author
Shalini Oruganti
shalini.oruganti@gmail.com