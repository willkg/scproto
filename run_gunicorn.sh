#!/bin/bash

KIND="$1"

if [[ $KIND == "" ]]
then
    echo "Specify the framework you want to use."
    echo "Aborting."
    exit
fi
gunicorn --config "${KIND}_conf.py" "scproto.${KIND}_wsgi:app"
