#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
methods:
    do_pack(): packs web_static/ files into .tgz archive
    do_deploy(archive_path): deploys archive to webservers
    deploy(): do_packs && do_deploys
    do_clean(n=0): removes old versions and keeps n (or 1) newest versions only
"""

from fabric.api import env, run, local, put
from datetime import datetime
from os.path import exists

# Set the hosts and user
env.hosts = ['18.209.224.134', '35.168.7.197']
env.user = 'ubuntu'


def do_pack():
    """
    Create a compressed archive of web_static contents
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static".format(now))
        return "versions/web_static_{}.tgz".format(now)
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distribute an archive to the web servers
    """
    if not os.path.exists(archive_path):
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

        # Move content to the parent folder & remove the web_static sub-folder
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


def deploy():
    """
    Create and distribute an archive to the web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

def do_clean(number=0):
    """
    Delete out-of-date archives
    """
    if int(number) < 1:
        number = 1
    else:
        number = int(number) + 1

    # Clean versions folder
    local("ls -1t versions | tail -n +{} "
            "| xargs -I {{}} rm versions/{{}}".format(number))

    # Clean releases folder
    releases = run("ls -1t /data/web_static/releases").split()
    for release in releases[number:]:
        run("rm -rf /data/web_static/releases/{}".format(release))
