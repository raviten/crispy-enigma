


sudo cp /home/ubuntu/backend/conf/nginx.conf /etc/nginx/sites-enabled/default
sudo cp /home/ubuntu/backend/conf/supervisor_backend.conf /etc/supervisor/conf.d/



cd /home/ubuntu/backend/
sudo chown ubuntu:ubuntu -R .
rm -rf venv
virtualenv venv --python=python3.5
source venv/bin/activate
pip install -r requirements.txt

#Db related tasks skip to another file
python manage.py migrate
python manage.py collectstatic

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart backend
sudo service nginx restart
