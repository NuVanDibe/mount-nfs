# Mount NFS Shares on Boot

This script mounts your favorite NFS shares on boot, so they're always available when you need them. All you have to do is define the NFS shares in a YAML file, and the script takes care of the rest.

## Usage

### Command line

You can use the `mount-nfs.py` script from the command line to mount or unmount NFS shares defined in a YAML file. If no options are specified, it will attempt to mount the shares located in (`/etc/mount-nfs.d/shares.yml`).

Here are the available options:

    -h, --help: show help message and exit.
    -f FILE, --file FILE: use a custom YAML file instead of the default one at (/etc/mount-nfs.d/shares.yml).
    -u, --unmount: unmount NFS shares defined in the YAML file.

### Systemd Service

The script comes with a systemd service file (`mount-nfs.service`) that mounts the NFS shares on boot. The service file calls the `mount-nfs.py` script with the default YAML file (`/etc/mount-nfs.d/shares.yml`).

Here's how you can set it up:

1. Edit the YAML file at `/etc/mount-nfs.d/shares.yml` with your favorite NFS shares.
2. Enable and start the service using the following commands:

```bash
sudo systemctl enable mount-nfs.service
sudo systemctl start mount-nfs.service
```

That's it! Your favorite NFS shares will be mounted on boot, so you can start using them right away.

#### How to Unmount

To stop and disable the service, use the following commands:

```bash
sudo systemctl stop mount-nfs.service
sudo systemctl disable mount-nfs.service
```

## YAML File

The YAML file should have the following format:

```yml
shares:
  - name: homeserver
    ip_address: 192.168.1.15
    paths:
      - path: /home/user/documents
        mount_point: /mount/homeserver/mydocs
  - name: synology
    ip_address: 192.168.1.31
    paths:
      - path: /volume1/Videos
        mount_point: /mount/mediashare/videos
      - path: /volume1/Music
        mount_point: /mount/mediashare/music
      - path: /volume1/documents
        mount_point: /mount/syno/docs
      - path: /volume1/docker
        mount_point: /mount/syno/docker
```

The `shares` section contains a list of dictionaries, where each dictionary defines an NFS share to be mounted. Each dictionary should have the following keys:

- `ip_address`: the IP address of the NFS server.
- `paths`: a list of dictionaries containing the paths to be mounted and their mount points.

Each dictionary in the `paths` list should have the following keys:

- `path`: the path to be mounted on the NFS server.
- `mount_point`: the mount point directory where the NFS share should be mounted.

## How it Works

The script contains two functions:

### `check_target_dirs(paths)`

Checks the target directories before mounting the NFS shares.

- If the directories don't exist, creates them.
- If the directories exist and are not empty or already mounted, raises an error message.

### `mount_nfs_shares(file)`

Mounts the NFS shares defined in the YAML file.

- Calls `check_target_dirs()` to check the target directories before mounting.
- Uses `os.system()` to mount the NFS shares.

### `unmount_nfs_shares(file)`

Unmounts the NFS shares defined in the YAML file.

- Uses `os.system()` to unmount the NFS shares.

## License

This script is licensed under the WTFPLv2 License. See the LICENSE file for more information.
