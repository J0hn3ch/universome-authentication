FLASK AUTHENTICATION APP
========================

Flask App for User Authentication
---------------------------------

# Requirements
1. Docker Engine
2. Python
3. Flask Framework

# 1. Getting started
Run the following command start the project.
``` docker compose up ```

## 1.1 Design
* [MVC design pattern in Flask](https://www.reddit.com/r/flask/comments/134j8qw/how_can_we_use_the_mvc_pattern_in_flask/)
* [MVC and MVT design patterns](https://www.geeksforgeeks.org/difference-between-mvc-and-mvt-design-patterns/)

# 2. Application factory
The application factory is coded into the file \__init__.py

## 2.1 Home page - Descrizione
Al primo avvio, l'intero sistema vien configurato affinchè il Database disponga del profilo di amministratore di base e consenta
l'inserimento di nuovi utenti, dopo aver inizializzato il database. Viene fatta una verifica facendo degli inserimenti di test per
verificare se le operazioni di Lettura, Creazione, Aggiornamento ed Eliminazione vengono effettuate correttamente.

La Home page dell'applicativo conterrà un messaggio di Benvenuto, con una sezione "Chi siamo" e un pulsante per effettuare l'accesso a chi è registrato.

## 2.2 Dashboard dell'amministratore
La dashboard dell'amministratore, consente la registrazione di nuovi utenti al sistema, o nuovi terminali.

## 2.3 Profilo utente

## 2.3.1 Utente normale
Un profili "Utente normale" è un profilo assegnato ad un soggetto, membro del progetto, che darà la possibilità di aggiornare, modificare e cancellare le proprie informazioni dal sistema.

## 2.3.2 Terminale
Un profilo con ruolo "Terminale" è un profilo assegnato ad un dispositivo che potrà leggere e verificare gli utenti registrati, per controllare se hanno accesso o no alla sede.

Per ogni dispositivo distribuito all'interno degli spazi dell'ateneo, questo verrà configurato con un profilo autorizzato solo alla
lettura. I membri


# 3. Security
## 3.1 Password Hashing
Use BCrypt module from Flask Extension

# 4. Deployment
## 4.1 Threaded mode
* [Enable Threaded mode](https://stackoverflow.com/questions/38876721/handle-flask-requests-concurrently-with-threaded-true)

# Miscellaneous
## Database
1. [DB Browser for SQLite] (https://sqlitebrowser.org/)

# Error encountered
1. ```ImportError: cannot import name 'url_decode' from 'werkzeug.urls' (/opt/venv/lib/python3.10/site-packages/werkzeug/urls.py)```
2. 

# Guides and resources
## App
1. **Python**:
    a. File ```__init__.py```: [https://betterstack.com/community/questions/what-is-init-py-for/](https://betterstack.com/community/questions/what-is-init-py-for/)
2. **Flask**:
    * [https://auth0.com/blog/best-practices-for-flask-api-development/](https://auth0.com/blog/best-practices-for-flask-api-development/)
    * [https://auth0.com/blog/developing-restful-apis-with-python-and-flask/](https://auth0.com/blog/developing-restful-apis-with-python-and-flask/)
3. **Flask-Login**: [https://flask-login.readthedocs.io/en/latest/](https://flask-login.readthedocs.io/en/latest/)
4. **Flask-Bcrypt**: [https://flask-bcrypt.readthedocs.io/en/1.0.1/index.html](https://flask-bcrypt.readthedocs.io/en/1.0.1/index.html)