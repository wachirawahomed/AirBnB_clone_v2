#!/usr/bin/env python3
"""
Fabric script that deletes out-of-date archives
"""

from fabric.api import env, run, local
from datetime import datetime
from os import listdir
from os.path import isfile, join

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    try:
        number = int(number)
        if number < 1:
            number = 1

        # Local cleanup
        local("ls -t versions | tail -n +{} | xargs -I {} rm versions/{}".format(number + 1, '{}'))

        # Remote cleanup
        releases_path = "/data/web_static/releases"
        releases = run("ls -tr {}".format(releases_path)).split()
        if len(releases) > number:
            releases_to_delete = releases[:-number]
            for release in releases_to_delete:
                run("rm -rf {}/{}".format(releases_path, release))

        # Cleanup unnecessary archives
        archives_path = "versions"
        archives = [f for f in listdir(archives_path) if isfile(join(archives_path, f))]
        archives.sort(reverse=True)
        if len(archives) > number:
            archives_to_delete = archives[number:]
            for archive in archives_to_delete:
                local("rm -f {}/{}".format(archives_path, archive))

    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    do_clean()

