#!/usr/bin/env bash
# Sets up webservers for deployment

# Install Nginx if not already installed
sudo apt-get update
sudo apt-get -y update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
sudo echo "<html>
<head>
</head>
<body>
  Holberton School
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership to ubuntu user and group
sudo chown -hR ubuntu:ubuntu /data/

# Update Nginx configuration
sudo sed -i '/listen 80 server_name _;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
