from pathlib import Path

from remote_host import LinuxRemoteHost, WindowsRemoteHost

if __name__ == "__main__":
    remote_host = LinuxRemoteHost(host="10.10.40.101", username="root", password="xxx")
    remote_host.connect()

    list_dir = remote_host.list_dir("/root")

    is_path = remote_host.is_exists("README.md")
    is_file = remote_host.is_file_exists("README.md")
    is_dir = remote_host.is_dir_exists("README.md")

    if remote_host.is_file_exists("README.md"):
        remote_host.delete_file("README.md")

    remote_host.put_file(local_file_path=Path("README.md"), remote_file_path="README.md")

    remote_host.execute_command("ls -l")

    remote_host.execute_file(local_file_path=Path("test.sh"), overwrite=True)

    remote_host = WindowsRemoteHost(host="10.4.11.113", username="Administrator", password="xxx", domain="somedomain")
    remote_host.connect()

    is_path = remote_host.is_exists("Windows")
    is_file = remote_host.is_file_exists("Windows")
    is_dir = remote_host.is_dir_exists("Windows")

    remote_host.disconnect()
