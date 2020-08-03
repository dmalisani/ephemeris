# Ephemeris
Sample program in Django + Django Rest Framework

## Install
Requires python 3.X

    pip install -r requirements.txt
## Create superuser
    python manage.py createsuperuser

## How to use admin
Enter to admin site: you have to enter to http://localhost:8000/admin and use credentials of superuser.

## API usage examples
http://localhost:8000/efemerides?dia=2020-06-20
response

    {
       "hoy":[
          "Dia de la bandera",
          "Día Mundial de los Refugiados"
       ],
       "mes":{
          "1":[
             "Dia mundial de los padres y madres"
          ],
          "5":[
             "Dia mundial del medio ambiente"
          ],
          "20":[
	     "Dia de la bandera",
	     "Día Mundial de los Refugiados"          ],
          "3":[
             "Dìa mundial de los asteroides"
          ]
       }
    }

## Run containers
    git clone https://github.com/dmalisani/ephemeris.git
    cd ephemeris
    docker-compose up --build
    localhost:8000/efemerides
