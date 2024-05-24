#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo
"""

from fabric.api import local
from datetime import datetime


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
