#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists
import os

env.hosts = ['18.209.224.134', '35.168.7.197']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        filename = archive_path.split('/')[-1]
        folder_name = "/data/web_static/releases/" + filename.split('.')[0]

        put(archive_path, "/tmp/")

        # Extract the archive to /data/web_static/releases/<filename>
        run("mkdir -p {}".format(folder_name))
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move contents to parent folder and remove the extracted folder
        run("mv {}/web_static/* {}".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link linked to the new version of code
        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
