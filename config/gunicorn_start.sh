#!/bin/bash

NAME="britecore-backend"                           # Name of the application
DJANGODIR=/home/ubuntu/crispy-enigma/backend # Django project directory
USER=ubuntu                                  # the user to run as
GROUP=ubuntu                                 # the group to run as
NUM_WORKERS=3                                # how many worker processes should Gunicorn spawn

echo "Starting $NAME"

# Activate the virtual environment
cd $DJANGODIR
source /home/ubuntu/crispy-enigma/venv/bin/activate
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn -w $NUM_WORKERS --bind=0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=backend.settings backend.wsgi
