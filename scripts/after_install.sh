cd /home/ubuntu/backend/
virtualenv venv --python=python3.5.2
pip install -r requirements.txt
source venv/bin/activate


#Db related tasks skip to another file
python manage.py migrate

mv /home/ubuntu/backend/conf/nginx.conf /etc/nginx/sites-enabled/default
mv /home/ubuntu/backend/conf/supervisor_backend.conf /etc/supervisor.d/conf.d/



sudo chown ubuntu:ubuntu -R .
sudo supervisorctl reread
sudo supervisorctl update
sudo service nginx restart
