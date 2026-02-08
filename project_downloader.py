project_directory = "projects"

try:
    cooldown = float(input("Projects will automatically be downloaded in ascending order from Scratch's servers.\nPress Ctrl+C at any time to start shutting down this script.\nTo start, type the number of seconds to wait between each download: "))
except ValueError:
    cooldown = 0

if cooldown > 0:
    try:
        launch_confirmation = int(input("Now input the first project ID you want to download: "))
    except ValueError:
        launch_confirmation = 0

    try:
        stop_id = int(input("If you want to stop downloading at a particular ID, type it now: "))
    except ValueError:
        stop_id = 1300000000

    if stop_id < 1:
        stop_id = 1300000000

    from datetime import datetime
    current_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')

    import sys
    import logging
    logging.basicConfig(
        format = '%(asctime)s - %(name)s (%(levelname)s): %(message)s',
        level = logging.INFO,
        handlers = [logging.FileHandler(f"archive_log.log"), logging.StreamHandler(sys.stdout)]
    )
    logger = logging.getLogger(__name__)

    import os, shutil

    try:
        os.mkdir(project_directory)
    except FileExistsError:
        pass

    def copy_file_to_disk(original, name, version):
        with open(name, "wb") as downloaded_file:
            downloaded_file.write(original.read())
            logger.info(f"{version} download: {name}")

    import concurrent.futures
    import urllib.request

    def download_project(project_id, name):
        try:
            try:
                with urllib.request.urlopen(f'https://scratch-projects-v3.scratch.org/{project_id}') as project_file:
                    copy_file_to_disk(project_file, name, "v3")

            except urllib.error.HTTPError:
                try:
                    with urllib.request.urlopen(f'https://scratch-projects-v2.scratch.org/{project_id}') as project_file:
                        copy_file_to_disk(project_file, name, "v2")

                except urllib.error.HTTPError:
                    try:
                        with urllib.request.urlopen(f'https://scratch-projects.scratch.org/{project_id}') as project_file:
                            copy_file_to_disk(project_file, name, "scratch-projects")

                    except urllib.error.HTTPError:
                        logger.info(f"FAILED to download {project_id}!")

        except KeyboardInterrupt:
            pass

    import time

    try:
        if launch_confirmation > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers = 9) as executor:
                for project_id in range(launch_confirmation, stop_id + 1):
                    download_file_name = f"{project_directory}/{project_id}"
                    executor.submit(download_project, project_id, download_file_name)

                    time.sleep(cooldown)
                
            logger.info(f"Downloads finished ({launch_confirmation} - {stop_id})")

    except KeyboardInterrupt:
        logger.info("Manually stopped (KeyboardInterrupt)")