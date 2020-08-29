#!/bin/bash
app="flask_website"
sudo docker run -p 5000:5000 --rm -v $PWD/output/:/usr/src/app/output --name ${app} ${app}