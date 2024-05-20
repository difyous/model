# Project: <Model> [31/08/2023]

## Author:  Mohammed CHALOULI

### ENVIRONMENT

- PostgreSQL Ver: psql (PostgreSQL) 13.11
- Python Ver:  3.9.16
- Port: 80

- sudo visudo

### To change the timeout, run, sudo visudo and add the line

    Defaults        timestamp_timeout=600 <!-- 100 Hours . and exit with :x or :wq  || :q! without saving changes -->

### Making python is the default rather than python3

- python -V
- sudo yum install epel-release
- If not installed : sudo yum install python39
- sudo ln -sf /usr/bin/python3.9 /usr/bin/python
- python -m pip install --upgrade pip

## Virtual env

- python -m venv .venv --prompt="URDVirtual"

## Database PostgreSQL

- If there is no DB server

  - sudo dnf install dnf-utils
  - sudo dnf install https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
  - sudo dnf install postgresql13 postgresql13-server

- sudo systemctl status postgresql-13
- sudo -u postgres psql
- \l : to see all databases
- CREATE DATABASE <Model> WITH OWNER = postgres;
- ALTER USER postgres WITH PASSWORD 'RD_database';

## Get requirements.txt from local machine using

- . .venv/bin/activate
- pip install -r requirements.txt  # pip freeze > requirements.txt

- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py collectstatic --no-input
- python manage.py runserver 0.0.0.0:8000

### To Test the Dev Project

- sudo yum install screen
- screen -d -m python manage.py runserver 0.0.0.0:8000&  # sudo if using port 80
- sudo firewall-cmd --zone=public --add-port=8000/tcp --permanent
- sudo firewall-cmd --reloadad

- screen -ls
- screen -r
- python manage.py check --deploy
- python manage.py shell # Quick tests

## Export

- python -Xutf8 manage.py dumpdata Myapp > UserApp -o user.json
- python -Xutf8 manage.py dumpdata Myapp -o data.json

## Import

- python -Xutf8 ./manage.py loaddata -v 3 data.json

## Better to install always 3.9 to be sure

- sudo yum list available | grep mod_wsgi
- sudo yum list installed | grep mod_wsgi

## Select the wsgi with the same version as your Python otherwise django is not installed or [wsgi:error] if (_wrapped := self._wrapped) is empty

- sudo systemctl status httpd
- sudo yum install python39-mod_wsgi.x86_64
- sudo yum install httpd
- sudo yum install nano
- sudo nano /etc/httpd/conf.d/django.conf

## In the file django.conf Write

    Alias /assets /home/user-VM/FOLDER/template/assets
    Alias /media /home/user-VM/FOLDER/template/media
    <Directory /home/user-VM/FOLDER/template/assets>
      Require all granted
    </Directory>
    <Directory /home/user-VM/FOLDER/template/media>
      Require all granted
    </Directory>
    <Directory /home/user-VM/FOLDER/application>
      <Files wsgi.py>
        Require all granted
      </Files>
    </Directory>

    WSGIDaemonProcess django_project python-path=/home/user-VM/FOLDER:/home/user-VM/FOLDER/.venv/lib/python3.9/site-packages
    WSGIProcessGroup django_project
    WSGIScriptAlias / /home/user-VM/FOLDER/application/wsgi.py
    WSGIRestrictStdout Off
    <VirtualHost *:80>
        ServerAdmin admin@django_project.localhost
        ServerName django_project.localhost
        ServerAlias www.django_project.localhost
        DocumentRoot /home/user-VM/FOLDER

        ErrorLog  /home/user-VM/FOLDER/apache_error.log
        CustomLog /home/user-VM/FOLDER/apache_access.log combined

        Alias /assets /home/user-VM/FOLDER/template/assets
        Alias /media /home/user-VM/FOLDER/template/media
        <Directory /home/user-VM/FOLDER/template/assets>
          Require all granted
        </Directory>
        <Directory /home/user-VM/FOLDER/template/media>
          Require all granted
        </Directory>
        <Directory /home/user-VM/FOLDER/application>
          <Files wsgi.py>
            Require all granted
          </Files>
        </Directory>
        
        Header set Access-Control-Allow-Origin "*"
        Header set Access-Control-Allow-Methods "GET, POST, PUT,PATCH, DELETE, OPTIONS"
        Header set Access-Control-Allow-Headers "Content-Type"
        # Time out 15 minutes
        Timeout 900

    </VirtualHost>

## Launching the server

- sudo chown :apache /home/user-VM/FOLDER/
- sudo usermod -a -G user-VM apache
- chmod 710 /home/user-VM
- sudo chmod -R 777 /home/user-VM/FOLDER/
- sudo setsebool -P httpd_can_network_connect 1
- sudo systemctl restart httpd
- sudo systemctl enable httpd

## application/wsgi.py

    import os,sys,site
    from django.core.wsgi import get_wsgi_application
    site.addsitedir('/home/user-VM/FOLDER/.venv/lib/python3.9/site-packages/')
    sys.path.append('/home/user-VM/FOLDER')
    sys.path.append('/home/user-VM/FOLDER/application/')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "application.settings")
    application = get_wsgi_application()

## Add in settings.py

    'DIRS': ['template' , os.path.join(BASE_DIR, 'template')],

### Update the config of apache

- sudo reboot
- sudo systemctl restart httpd

### Update the config of apache [Optional]

- sudo nano /etc/httpd/conf/httpd.conf
- change /var/www ==> /home/user-VM/
- change /var/www/html ==> /home/user-VM/FOLDER/

## P.S: Updating the config file of Apache may take to 15 min to be effective

## Error Monitoring and Logs

- sudo tail -f /var/log/httpd/error_log | egrep -v "(.gif|.jpg|.png|.swf|.ico)"
sudo tail -f /home/user-VM/FOLDER/apache_error.log | egrep -v "(.gif|.jpg|.png|.swf|.ico)"
- sudo yum install zip
- zip -r myzip.zip  . # Quick download
- zip -r myCode.zip . -x "template/assets/*"
