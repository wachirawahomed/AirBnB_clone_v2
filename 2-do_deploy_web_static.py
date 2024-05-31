#!/usr/bin/python3
"""Fabric script that distributes an archive to your web servers"""

from fabric.api import *
from os.path import exists
from datetime import datetime

env.hosts = ['18.209.224.134', '35.168.7.197']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Distributes an archive to the web servers and deploys it"""

    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp')

        # Get the filename without extension
        filename = archive_path.split('/')[-1].split('.')[0]

        # Create the destination directory
        run('mkdir -p /data/web_static/releases/{}/'.format(filename))

        # Uncompress the archive to the destination directory
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(filename, filename))

        # Remove the archive from the server
        run('rm /tmp/{}.tgz'.format(filename))

        # Move the contents of the uncompressed folder to a new location
        run('mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(filename, filename))

        # Remove the uncompressed folder
        run('rm -rf /data/web_static/releases/{}/web_static'.format(filename))

        # Delete the symbolic link /data/web_static/current
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version of your code
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(filename))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
