import os
from nfs_client import mount, unmount

# --- Configuration ---
# The IP address or hostname of your NFS server
SERVER_IP = '192.168.1.100'

# The path on the NFS server that is exported (e.g., /home/share)
REMOTE_PATH = '/exports/data'

# The local directory where the remote path will be mounted
LOCAL_MOUNT_POINT = '/mnt/nfs_data'


def nfs_operation():
    """Mounts an NFS share, lists files, and then unmounts."""
    print(f"Attempting to mount {SERVER_IP}:{REMOTE_PATH} to {LOCAL_MOUNT_POINT}...")

    # 1. Create the local mount point if it doesn't exist
    if not os.path.exists(LOCAL_MOUNT_POINT):
        os.makedirs(LOCAL_MOUNT_POINT)

    try:
        # 2. Mount the NFS share
        # This function executes the system's mount command
        mount(
            server=SERVER_IP,
            remote_path=REMOTE_PATH,
            local_mount_point=LOCAL_MOUNT_POINT,
            # NFS protocol version (e.g., 'nfs4' for NFSv4)
            nfs_proto_version='nfs4'
        )
        print("✅ Mount successful.")

        # 3. Perform file operations (e.g., list contents)
        print(f"\nContents of {LOCAL_MOUNT_POINT}:")

        # os.listdir treats the mount point like any local directory
        files_and_folders = os.listdir(LOCAL_MOUNT_POINT)
        for item in files_and_folders:
            print(f"- {item}")

        # You can now read/write files as if they were local
        # Example: with open(os.path.join(LOCAL_MOUNT_POINT, 'myfile.txt'), 'r') as f: ...

    except Exception as e:
        print(f"❌ An error occurred: {e}")

    finally:
        # 4. Ensure the share is unmounted to clean up
        if os.path.ismount(LOCAL_MOUNT_POINT):
            print(f"\nAttempting to unmount {LOCAL_MOUNT_POINT}...")
            unmount(LOCAL_MOUNT_POINT)
            print("✅ Unmount successful.")
        else:
            print(f"\n{LOCAL_MOUNT_POINT} was not mounted, skipping unmount.")


if __name__ == '__main__':
    nfs_operation()
