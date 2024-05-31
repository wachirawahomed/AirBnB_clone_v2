#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo
"""

from fabric.api import local, env, run, put
from datetime import datetime
from os.path import exists

env.hosts = ['18.209.224.134', '35.168.7.197']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    # Create the versions folder if it doesn't exist
    local("mkdir -p versions")

    # Generate the filename with current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = "versions/web_static_" + timestamp + ".tgz"

    # Create the .tgz archive
    result = local("tar -czvf {} web_static".format(file_name))

    # Check if the archive has been correctly generated
    if result.failed:
        return None
    else:
        return file_name


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web servers
        put(archive_path, "/tmp/")

        # Get the filename without extension
        filename = archive_path.split('/')[-1]

        # Create the destination directory on the web servers
        folder_name = "/data/web_static/releases/" + filename.split('.')[0]
        run('mkdir -p {}'.format(folder_name))

        # Uncompress the archive to the destination directory
        run('tar -xzf /tmp/{} -C {}'.format(filename, folder_name))

        # Delete the archive from the web servers
        run('rm /tmp/{}'.format(filename))

        # Move contents to parent folder and remove the extracted folder
        run('mv {}/web_static/* {}'.format(folder_name, folder_name))
        run('rm -rf {}/web_static'.format(folder_name))

        # Delete the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create new symbolic link linked to the new version of code
        run('ln -s {} /data/web_static/current'.format(folder_name))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False


def deploy():
    """
    Creates and distributes an archive to web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    
    result = do_deploy(archive_path)
    return result
