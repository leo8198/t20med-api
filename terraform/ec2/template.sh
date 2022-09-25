#!/bin/bash

sudo apt-get update
sudo apt-get install apache2 -y
echo "hello from terraform" >> /var/www/html/index.html
sudo systemctl start apache2