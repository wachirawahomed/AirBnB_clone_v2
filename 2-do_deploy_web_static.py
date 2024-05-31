#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, put, run
from os.path import exists
import os

# Set the hosts and user
env.hosts = ['18.209.224.134', '35.168.7.197']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Extract filename and folder name from the archive_path
        filename = archive_path.split('/')[-1]
        no_ext = filename.split(".")[0]
        folder_name = "/data/web_static/releases/{}/".format(no_ext)

        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Create the folder where the archive will be uncompressed
        run("mkdir -p {}".format(folder_name))

        # Uncompress the archive to the folder
        run("tar -xzf /tmp/{} -C {}".format(filename, folder_name))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move contents to parent folder and remove the web_static sub-folder
        run("mv {}/web_static/* {}".format(folder_name, folder_name))
        run("rm -rf {}/web_static".format(folder_name))

        # Delete the current symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link linked to the new version of code
        run("ln -s {} /data/web_static/current".format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False
