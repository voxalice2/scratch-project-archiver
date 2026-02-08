project_directory = "projects"

try:
    cooldown = float(input("Projects will automatically be downloaded in ascending order from Scratch's servers.\nTo start, type the number of seconds to wait between each download: "))
except ValueError:
    cooldown = 0

if cooldown > 0:
    launch_confirmation = int(input("Now input the first project ID you want to download: "))

    import urllib.request
    import time

    from datetime import datetime
    current_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')

    import sys
    import logging
    logging.basicConfig(
        format = '%(asctime)s - %(name)s (%(levelname)s): %(message)s',
        level = logging.INFO,
        handlers = [
            logging.FileHandler(f"archive_log.log"),
            logging.StreamHandler(sys.stdout)
        ])
    logger = logging.getLogger(__name__)

    import os, shutil

    try:
        os.mkdir(project_directory)
    except FileExistsError:
        pass

    def download_project(file, name, type):
        with open(name, "wb") as downloaded_file:
            downloaded_file.write(file.read())
            logger.info(f"{type} download: {name}")

    if launch_confirmation > 0:
        for project_id in range(launch_confirmation, 1276652897):
            download_file_name = f"{project_directory}/{project_id}"

            try:
                with urllib.request.urlopen(f'https://scratch-projects-v3.scratch.org/{project_id}') as original_project_file:
                    download_project(original_project_file, download_file_name, "v3")

            except urllib.error.HTTPError:
                try:
                    with urllib.request.urlopen(f'https://scratch-projects-v2.scratch.org/{project_id}') as original_project_file:
                        download_project(original_project_file, download_file_name, "v2")

                except urllib.error.HTTPError:
                    logger.info(f"FAILED to download {project_id}!")

            time.sleep(cooldown)