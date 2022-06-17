from datetime import datetime
import os
import shutil
import hashlib
import glob
from time import sleep


# Configuration
source_directory = r"changeme"
target_directory = r"changeme"
file_extension = r".changeme"
# Turn continuous monitoring on or off. Default True.
enable_monitoring = True
# The refresh rate in seconds of folder monitoring. Default 1.
monitor_rate = 1
# How long in seconds to wait after last file change before syncing. (To avoid syncing files that are actively being written to). Default 2.
monitor_activity_delay = 2
# End of Configuration


def hash_file(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def trim_folders():
    for i in glob.glob("**", root_dir=target_directory, recursive=True):
        tgt_path = os.path.join(target_directory, i)
        src_path = os.path.join(source_directory, i)
        if os.path.isdir(tgt_path) and not os.path.exists(src_path):
            print("Removing Folder: " + i)
            shutil.rmtree(tgt_path)


def trim_files():
    for i in glob.glob("**", root_dir=target_directory, recursive=True):
        tgt_path = os.path.join(target_directory, i)
        src_path = os.path.join(
            source_directory, i.removesuffix(file_extension))
        if os.path.isfile(tgt_path) and not os.path.exists(src_path):
            print("Removing File: " + i)
            os.remove(tgt_path)


def create_folders():
    for i in glob.glob("**", root_dir=source_directory, recursive=True):
        tgt_path = os.path.join(target_directory, i)
        src_path = os.path.join(source_directory, i)
        if os.path.isdir(src_path) and not os.path.exists(tgt_path):
            print("Creating Folder: " + i)
            os.makedirs(tgt_path)


def copy_files():
    for i in glob.glob("**", root_dir=source_directory, recursive=True):
        tgt_path = os.path.join(target_directory, i + file_extension)
        src_path = os.path.join(source_directory, i)
        if os.path.isfile(src_path):
            if not os.path.exists(tgt_path):
                print("New File: " + i + file_extension)
                shutil.copy(src_path, tgt_path)
            else:
                if hash_file(src_path) != hash_file(tgt_path):
                    print("Updating File: " + i + file_extension)
                    shutil.copy(src_path, tgt_path)


def initial_sync():
    trim_folders()
    trim_files()
    create_folders()
    copy_files()


def monitoring():
    # Dictionary of last modified times for items in the source directory.
    last_modified = {}
    for i in glob.glob("**", root_dir=source_directory, recursive=True):
        src_path = os.path.join(source_directory, i)
        last_modified[i] = os.path.getmtime(src_path)
    # For every item in source_directory, check if it has been modified since last_modified, or has been newly created (not in last_modified).
    # For files, we wait a specified amount of time before copying. Folders get created immediately.
    while True:
        for i in glob.glob("**", root_dir=source_directory, recursive=True):
            src_path = os.path.join(source_directory, i)
            tgt_path_folder = os.path.join(target_directory, i)
            tgt_path_file = os.path.join(target_directory, i + file_extension)
            # Guard clause simulating .isfile and .isdir checks prior to .getmtime as we have elsewhere.
            # We end up running the check twice but it's the cleanest solution I could come up with without having long if statements.
            if not os.path.isfile(src_path) and not os.path.isdir(src_path):
                continue
            if not i in last_modified or os.path.getmtime(src_path) > last_modified[i]:
                if os.path.isdir(src_path) and not os.path.exists(tgt_path_folder):
                    print("Creating Folder: " + i)
                    os.makedirs(tgt_path_folder)
                elif os.path.isfile(src_path):
                    while True:
                        if os.path.getmtime(src_path) <= datetime.now().timestamp() - monitor_activity_delay:
                            if not i in last_modified:
                                print("New File: " + i + file_extension)
                            else:
                                print("Updating File: " + i + file_extension)
                            last_modified[i] = os.path.getmtime(src_path)
                            shutil.copy(src_path, tgt_path_file)
                            break
                        else:
                            next_check = (os.path.getmtime(
                                src_path) - datetime.now().timestamp()) + monitor_activity_delay
                            print(
                                f"Waiting {next_check:.2f} seconds while {i} is being modified.")
                            sleep(next_check)
        # For every item in target_directory, we check if it is still present in source_directory, and remove it if not.
        for i in glob.glob("**", root_dir=target_directory, recursive=True):
            tgt_path = os.path.join(target_directory, i)
            src_path_folder = os.path.join(source_directory, i)
            src_path_file = os.path.join(
                source_directory, i.removesuffix(file_extension))
            if os.path.isdir(tgt_path) and not os.path.exists(src_path_folder):
                print("Removing Folder: " + i)
                shutil.rmtree(tgt_path)
                if i in last_modified:
                    del last_modified[i]
            elif os.path.isfile(tgt_path) and not os.path.exists(src_path_file):
                print("Removing File: " + i)
                os.remove(tgt_path)
                if i in last_modified:
                    del last_modified[i]
        sleep(monitor_rate)


def config_info():
    print(
        f"Configuration:\n┣Source Directory: {source_directory}\n┣Target Directory: {target_directory}\n┗File Extension: {file_extension}")
    if enable_monitoring:
        print(
            f"Monitoring Configuration:\n┣Monitoring Rate: {monitor_rate} seconds\n┗Monitoring Activity Delay: {monitor_activity_delay} seconds")


if __name__ == "__main__":
    config_info()
    if not os.path.exists(source_directory):
        print("Error: Configuration: Source Directory does not exist.")
        exit(1)
    if not os.path.exists(target_directory):
        print("Error: Configuration: Target Directory does not exist.")
        exit(1)
    print("Initializing...")
    initial_sync()
    print("Sync Complete")
    if enable_monitoring:
        print("Starting Monitoring... Close Application or Press Ctrl+C to Stop")
        while True:
            try:
                monitoring()
            except KeyboardInterrupt:
                print("Stopping Monitoring")
                break
            except:
                print("Error: Monitoring: Resyncing in 5 Seconds...")
                sleep(5)
                initial_sync()
    print("Program Done")
