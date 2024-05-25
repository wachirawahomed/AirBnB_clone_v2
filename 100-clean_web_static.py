#!/usr/bin/python3
"""
Fabric script to delete out-of-date archives
"""
from fabric.api import env, put, run, local
from os.path import exists
from datetime import datetime

env.hosts = ['18.209.224.134', '35.168.7.197']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        print(e)
        return None


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


def deploy():
    """
    Creates and distributes an archive to the web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)


def do_clean(number=0):
    """
    Delete out-of-date archives.

    Arguments:
        number {int} -- Number of archives to keep (default: {0})
    """
    number = 1 if int(number) == 0 else int(number)

    # Local cleanup
    archives = sorted(os.listdir("versions"))
    archives_to_delete = archives[:-number]
    with lcd("versions"):
        for archive in archives_to_delete:
            local("rm ./{}".format(archive))

    # Remote cleanup
    releases = run("ls -tr /data/web_static/releases").split()
    releases_to_delete = [r for r in releases if "web_static_" in r][:-number]
    with cd("/data/web_static/releases"):
        for release in releases_to_delete:
            run("rm -rf ./{}".format(release))
