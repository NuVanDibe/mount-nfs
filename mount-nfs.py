#!/usr/bin/env python3

import argparse
import os
import yaml

# Default location of the YAML file
DEFAULT_FILE = '/etc/mount-nfs.d/shares.yml'

import os

def check_target_dirs(paths):
    """
    Check the target directories before mounting the NFS shares.

    If the directories don't exist, create them.
    If the directories exist and are not empty or already mounted, raise an error.

    :param paths: a list of dictionaries containing the paths to be mounted and their mount points.
    :return: None
    :raises: ValueError if the target directories are not empty or are already mounted.
    """
    for path in paths:
        mount_point = path['mount_point']
        if not os.path.exists(mount_point):
            os.makedirs(mount_point)
        elif os.path.ismount(mount_point):
            raise ValueError(f'{mount_point} is already mounted.')
        elif os.listdir(mount_point):
            raise ValueError(f'{mount_point} is not empty.')

def mount_nfs_shares(file):
    """
    Mount the NFS shares defined in the YAML file.
    """
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for share in data['shares']:
        paths = share['paths']
        try:
            check_target_dirs(paths)
        except ValueError as e:
            print(f'Error: {e}')
            exit(1)
        for path in paths:
            escaped_path = path['path'].replace(' ', '\ ')
            print(f"Mounting {share['ip_address']}:{escaped_path} to {path['mount_point']}...")
            os.system(f"sudo mount -t nfs {share['ip_address']}:{escaped_path} {path['mount_point']}")

def unmount_nfs_shares(file):
    """
    Unmount the NFS shares defined in the YAML file.
    """
    with open(file) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    for share in data['shares']:
        for path in share['paths']:
            print(f"Unmounting {path['mount_point']}...")
            os.system(f"sudo umount {path['mount_point']}")


# Parse command-line arguments
parser = argparse.ArgumentParser(description='Mount or unmount NFS shares from a YAML file.')
parser.add_argument('-f', '--file', default=DEFAULT_FILE,
                    help=f'location of the YAML file (default: {DEFAULT_FILE})')
parser.add_argument('-u', '--unmount', action='store_true',
                    help='unmount NFS shares')
args = parser.parse_args()

# Check if the specified file exists
if not os.path.exists(args.file):
    if args.file == DEFAULT_FILE:
        print(f'Error: default YAML file {DEFAULT_FILE} not found.')
    else:
        print(f'Error: file {args.file} not found.')
    exit(1)

# Begin work
print(f'Using {args.file}...')

# Mount or unmount NFS shares
if args.unmount:
    unmount_nfs_shares(args.file)
else:
    mount_nfs_shares(args.file)
