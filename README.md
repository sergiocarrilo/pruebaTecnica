#Ejecutar la prueba técnica de la api de seguros

##Requisitos previos

Para poder ejecutar esta prueba es necesario tener los siguientes requisitos:

Docker (**version 20.10.8**)

    Instalación de Docker:
        
        https://docs.docker.com/engine/install/

docker-compose  (**version 1.26.0**)

    Instalación docker-compose:
        
        https://docs.docker.com/compose/install/

Una vez instalados estos requistos el siguiente paso es intalar el proyecto en local.

##Tecnologías utilizadas

Las principales tecnologías que hemos seleccionado para su implemetación son las siguientes:

    Python 3.8
    Django 3.2.6
    DRF 3.12.4
    MYSQL 5.7.25
    Docker 20.10.8
    Docker compose 1.26.0

El motivo por el cual, he elegido usar estas tecnologías es porque son las herramientas con las que trabajo actualmente.

Django es un framework para proyectos web pensado para disponer de una aplicación en tiempos de desarrollo cortos. 
Algunas de sus características implementa por defecto las principales medidas de seguridad clásicas (SQL Injection, CSRF, por ejemplo), dispone de un ORM muy potente, proporciona un panel de administración muy útil, etc.

Django Rest Framework es un framework pensado para implementar APIs basado en Django, aparte proporciona muchas funcionalidades específicas para el desarrollo de APIs, autenticación, serialización de datos, etc.

MySQL, permite manejar grandes bases de datos, su sistema de seguridad encriptado para acceder a ellas, su facilidad de instalación en distintos sistemas operativos.

Docker es la tecnología para crear y gestiónar imágenes y contenedores software, y Docker Compose, tecnología de orquestación basada en contenedores.
##Instalación del proyecto

Lo primero iremos al directorio donde queremos tener nuestro proyecto y ejecutaremos el siguiente comando:

    https://github.com/sergiocarrilo/prueba-tecnica-api-rest.git

Una vez descargado el proyecto del repositorio accederemos al directorio.

Para poder levantar el proyecto es necesario crear la imagen de la aplicación, paa ello ejecutaremos:

    docker-compose build --no-cache api-insurances

Una vez creada la imagen de la aplicación, procedemos a levantar el contenedor de la aplicación:
    
    docker-compose up api-insurances

Este comando nos levantará también la base de datos, pero puede hacerse manualmente ejecutando:
    
    docker-compose up db-insurances

En este momento, ya tenemos la aplicación lista para operar con ella. 

##Funcionalidades disponibles

Una vez arrancado el proyecto, dispondremos de las funcionalidades descritas en el enunciado de la prueba, adjunto un 
ejemplo con curl de cada una de las llamadas a la api.

Adicionalmente a lo requerido se ha añadido un endpoint para Login y otro para Register, 
ambos devuelve el token necesario para poder autenticarse en el resto de endpoints.

###Register

    curl --location --request POST 'http://0.0.0.0:8888/api/register/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "username": "test",
            "email": "api@prueba.com",
            "password": "_123qwe_",
            "first_name": "prueba",
            "last_name": "tecnica"
        }'

    Respuesta:

    {
        "user": {
            "username": "test",
            "first_name": "prueba",
            "last_name": "tecnica",
            "email": "api@prueba.com",
            "password": "pbkdf2_sha256$260000$ZNVTUaKrrfpzmhB2kJJn4w$VZ+wJHMCYYULvxsn4RKZ5FqdtGOV+o8SjiQ98S6rnGs="
        },
        "access_token": "2fd0dd03ff18582b6c160ad264b1bfdd6a3c200a"
    }


###Login

    curl --location --request POST 'http://0.0.0.0:8888/api/login/' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "email": "api@prueba.com",
            "password": "_123qwe_"
        }'


    Respuesta:
    {
        "user": {
            "username": "test",
            "first_name": "prueba",
            "last_name": "tecnica",
            "email": "api@prueba.com",
            "password": "pbkdf2_sha256$260000$ZNVTUaKrrfpzmhB2kJJn4w$VZ+wJHMCYYULvxsn4RKZ5FqdtGOV+o8SjiQ98S6rnGs="
        },
        "access_token": "2fd0dd03ff18582b6c160ad264b1bfdd6a3c200a"
    }

Una vez vistos los endpoints de registro y login para general la autenticación, 
pasaremos a ver los endpoints necesarios para cubrir la funcionalidad del enunciado: 

###Create Insurance (añadir seguro)

    curl --location --request POST 'http://0.0.0.0:8888/api/insurance/' \
        --header 'Authorization: Token 78ffcce4e24fdadea2a37c08df37323a335ca5e2' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "insurance_price": 94.5,
            "insurance_category": "Coche",
            "periodicity": "Anual",
            "insurer": 5,
            "detail": "Audi A3",
            "coverage_end": "2021-09-01"
        }'
    
    Respuesta:
    {
        "response": "The insurance has been created successfully"
    }

###Delete Insurance(borrar seguro)
En este caso es necesario para el id del seguro en la url:

    curl --location --request DELETE 'http://0.0.0.0:8888/api/insurance/7/' \
        --header 'Authorization: Token 78ffcce4e24fdadea2a37c08df37323a335ca5e2' \
        --data-raw ''

    Respuesta:
    {
        "response": "The insurance has been deleted successfully"
    }

###Insurances List(listar seguros)

    curl --location --request GET 'http://0.0.0.0:8888/api/insurance/' \
        --header 'Authorization: Token 78ffcce4e24fdadea2a37c08df37323a335ca5e2'

    Respuesta:

    {
        "response": [
            {
            "id": 9,
            "insurer": "Qualitas Auto",
            "insurance_category": "Coche",
            "insurance_price": 94.5
            },
            {
                "id": 14,
                "insurer": "Qualitas Auto",
                "insurance_category": "Moto",
                "insurance_price": 77.5
            }
        ]
    }


###Insurances Detail(detalle del seguros)
En este caso es necesario para el id del seguro en la url:

    curl --location --request GET 'http://0.0.0.0:8888/api/insurance/9/' \
        --header 'Authorization: Token 78ffcce4e24fdadea2a37c08df37323a335ca5e2'

    Respuesta:
    {
        "response": [
            {
                "id": 9,
                "insurance_price": 94.5,
                "insurance_category": "Coche",
                "periodicity": "Anual",
                "insurer": 5,
                "detail": "Audi A3",
                "coverage_end": "2021-09-01",
                "insurer_name": "Qualitas Auto",
                "insurer_phone": "916836483"
            }
        ]
    }

#Account (reiniciar contraseña)

    curl --location --request PATCH 'http://0.0.0.0:8888/api/password/change/' \
        --header 'Authorization: Token 78ffcce4e24fdadea2a37c08df37323a335ca5e2' \
        --header 'Content-Type: application/json' \
        --data-raw '{
            "old_password": "_123qwe_",
            "new_password": "123qwe__"
        }'

    Respuesta:
    {
        "response": "Password has been changed"
    }


#Account (baja)

    curl --location --request DELETE 'http://0.0.0.0:8888/api/account/' \
        --header 'Authorization: Token 78ffcce4e24fdadea2a37c08df37323a335ca5e2'

    Respuesta:
    {
        "response": "Your account has been canceled correctly"
    }