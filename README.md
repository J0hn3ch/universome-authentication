FLASK AUTHENTICATION APP
========================

Flask App for User Authentication
---------------------------------

# Requirements
1. Docker Engine
2. Python
3. Flask Framework

# 1. Getting started
Move from the command line in the 'universome-authentication' folder and run the following command start the project.

``` docker compose up ```

The application can be used from the http://127.0.0.1:8000

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
APPROCCIO SHAZAM: Il client invia una richiesta al server che si desidera avvicinare un Tag RFID e rimane in attesa della risposta dal server per la convalida.

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
* [uWSGI] (https://en.wikipedia.org/wiki/UWSGI)

## 4.1 Threaded mode
* [Enable Threaded mode](https://stackoverflow.com/questions/38876721/handle-flask-requests-concurrently-with-threaded-true)

# Miscellaneous
## Flask
1. Important: [Application Context](https://flask.palletsprojects.com/en/2.3.x/appcontext/)
2. Dinamyc HTML Page: [JavaScript, fetch, and JSON - Flask](https://flask.palletsprojects.com/en/2.3.x/patterns/javascript/)

## Database
1. [DB Browser for SQLite] (https://sqlitebrowser.org/)
2. [Database Connection and Cursor closing] (https://www.quora.com/What-is-the-difference-between-cursor-and-connection-when-performing-operations-on-databases)

## Database Cache
1. [Redis](https://redis.com/)
2. 

## Styling
1. libsass - [https://sass.github.io/libsass-python/index.html](https://sass.github.io/libsass-python/index.html)
2. libsass with Flask - [https://sass.github.io/libsass-python/frameworks/flask.html](https://sass.github.io/libsass-python/frameworks/flask.html)

# Error encountered
1. ```ImportError: cannot import name 'url_decode' from 'werkzeug.urls' (/opt/venv/lib/python3.10/site-packages/werkzeug/urls.py)```
2. ```sqlite3.OperationalError: attempt to write a readonly database``` Solution: ```RUN chown ${UID}:${UID} instance -R``` in _Dockerfile_

# Guides and resources

## App
1. **Python**:
    * File ```__init__.py```: [https://betterstack.com/community/questions/what-is-init-py-for/](https://betterstack.com/community/questions/what-is-init-py-for/)
    * The Try, Except and Finally block: [https://medium.com/analytics-vidhya/do-you-really-understand-try-finally-in-python-110cee4c1a8](https://medium.com/analytics-vidhya/do-you-really-understand-try-finally-in-python-110cee4c1a8)
2. **Flask**:
    * [https://auth0.com/blog/best-practices-for-flask-api-development/](https://auth0.com/blog/best-practices-for-flask-api-development/)
    * [https://auth0.com/blog/developing-restful-apis-with-python-and-flask/](https://auth0.com/blog/developing-restful-apis-with-python-and-flask/)
    * make_response() Docs: [https://tedboy.github.io/flask/generated/flask.make_response.html](https://tedboy.github.io/flask/generated/flask.make_response.html)

3. **Flask-Login**: [https://flask-login.readthedocs.io/en/latest/](https://flask-login.readthedocs.io/en/latest/)
4. **Flask-Bcrypt**: [https://flask-bcrypt.readthedocs.io/en/1.0.1/index.html](https://flask-bcrypt.readthedocs.io/en/1.0.1/index.html)
5. **Flask-WTF - Documentation** [https://flask-wtf.readthedocs.io/en/1.2.x/quickstart/](https://flask-wtf.readthedocs.io/en/1.2.x/quickstart/)
6. **WTForms - Crash course**: [https://wtforms.readthedocs.io/en/3.0.x/crash_course/](https://wtforms.readthedocs.io/en/3.0.x/crash_course/)
7. **PySerial - Documentation**: [https://pyserial.readthedocs.io/en/latest/](https://pyserial.readthedocs.io/en/latest/)
8. **Server-Sent Event**: [https://dev.to/cloudx/backend-to-frontend-communication-with-server-sent-events-56kf](https://dev.to/cloudx/backend-to-frontend-communication-with-server-sent-events-56kf)
9. **Flask-SSE**: [https://flask-sse.readthedocs.io/en/latest/quickstart.html](https://flask-sse.readthedocs.io/en/latest/quickstart.html)

## Database
1. Timestamp: [https://dev.mysql.com/doc/refman/8.0/en/timestamp-initialization.html](https://dev.mysql.com/doc/refman/8.0/en/timestamp-initialization.html)

## Environment
1. Virtual environment and container: [https://stackoverflow.com/questions/48561981/activate-python-virtualenv-in-dockerfile](https://stackoverflow.com/questions/48561981/activate-python-virtualenv-in-dockerfile)
2. Baud rate: [Common Baud rate](https://lucidar.me/en/serialib/most-used-baud-rates-table/)
3. TTY: [Keep TTY open in Docker](https://kossy0701.medium.com/what-is-tty-true-in-docker-compose-yml-47a72891aee2)
4. dmesg: Operation not permitted: [Privileged Docker container](https://stackoverflow.com/questions/41178553/docker-how-to-avoid-operation-not-permitted-in-docker-container)
5. Permission problems in TTY from Docker to RaspberryOS

## Container
1. Docker installation (for RPi 3B+ with aarch64, 64bit RaspberryOS): [https://docs.docker.com/engine/install/debian/](https://docs.docker.com/engine/install/debian/)
2. Docker Compose Flask Sample: [https://github.com/docker/awesome-compose/tree/master/flask](https://github.com/docker/awesome-compose/tree/master/flask)

## Hardware
1. Logic Level Shifter / Converter
    * Fake LLS[https://forum.arduino.cc/t/logic-level-shifter-problem/1138650](https://forum.arduino.cc/t/logic-level-shifter-problem/1138650)

# Tutorials

### Project structure
1. [How to structure Flask project](https://www.reddit.com/r/flask/comments/vttloi/af_how_am_i_supposed_to_structure_my_flask_project/)

### Flask-Login
1. [Add authentication to your app with Flask-Login](https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login)
2. [How to authenticate users in Flask](https://www.freecodecamp.org/news/how-to-authenticate-users-in-flask/)
3. [How Flask-Login works](https://stackoverflow.com/questions/12075535/flask-login-cant-understand-how-it-works)

# Credits

# License