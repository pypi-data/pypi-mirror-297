import logging
from ipaddress import IPv4Address
from pathlib import Path
from typing import Union, Optional

import paramiko
from wiederverwendbar.before_after_wrap import wrap

from remote_host.base_remote_host import BaseRemoteHost
from remote_host.objects import DirectoryObject, FileObject

logger = logging.getLogger(__name__)


class LinuxRemoteHost(BaseRemoteHost):
    def __init__(self,
                 host: Union[str, IPv4Address],
                 username: str,
                 password: str,
                 port: int = 22,
                 check_ping: bool = True,
                 check_ping_timeout: int = 5,
                 check_ping_verbose: bool = False,
                 check_port: bool = True,
                 ssl_verify_hostname: bool = True):
        self._ssl_verify_hostname = ssl_verify_hostname
        self._client = paramiko.SSHClient()

        super().__init__(host=host,
                         username=username,
                         password=password,
                         port=port,
                         check_ping=check_ping,
                         check_ping_timeout=check_ping_timeout,
                         check_ping_verbose=check_ping_verbose,
                         check_port=check_port)

    def __enter__(self) -> "LinuxRemoteHost":
        super().__enter__()

        return self

    @property
    def ssl_verify_hostname(self) -> bool:
        """
        If True, the hostname will be verified.

        :return: Value of ssl_verify_hostname
        """

        return self._ssl_verify_hostname

    def connect(self) -> None:
        if self.ssl_verify_hostname:
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        else:
            self._client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        self._client.connect(hostname=self.host,
                             username=self.username,
                             password=self.password,
                             port=self.port)

    def disconnect(self) -> None:
        self._client.close()

    @property
    def is_connected(self) -> bool:
        return not self._client.get_transport() is None

    @property
    def client(self):
        if not self.is_connected:
            raise RuntimeError(f"Not connected to {self}.")
        return self._client

    def list_dir(self, remote_dir_path: str) -> list[Union[DirectoryObject, FileObject]]:
        objs = []

        first_line = True
        for line in self.execute_command(f"ls -l {remote_dir_path}", expected_exit_code=0)[1]:
            if first_line:
                first_line = False
                continue
            line_split = line.split()
            flags = line_split[0]
            name = line_split[-1]
            size = int(line_split[4])
            if "d" in flags:
                objs.append(DirectoryObject(name=name, path=f"{remote_dir_path}/{name}"))
            else:
                objs.append(FileObject(name=name, path=f"{remote_dir_path}/{name}", size=size))

        return objs

    def is_exists(self, remote_dir_path: str) -> bool:
        with self.client.open_sftp() as sftp:
            try:
                sftp.stat(remote_dir_path)
            except FileNotFoundError:
                return False
            return True

    def is_file_exists(self, remote_file_path: str) -> bool:
        return self.execute_command(f"test -f {remote_file_path}", expected_exit_code=0)[0] == 0

    def is_dir_exists(self, remote_dir_path: str) -> bool:
        return self.execute_command(f"test -d {remote_dir_path}", expected_exit_code=0)[0] == 0

    def get_file(self, remote_file_path: str, local_file_path: Path, overwrite: bool = False) -> None:
        with self.client.open_sftp() as sftp:
            sftp.get(remote_file_path, local_file_path)

    def put_file(self, local_file_path: Path, remote_file_path: str, overwrite: bool = False) -> None:
        with self.client.open_sftp() as sftp:
            sftp.put(local_file_path, remote_file_path)

    def delete_file(self, remote_file_path: str) -> None:
        with self.client.open_sftp() as sftp:
            sftp.remove(remote_file_path)

    def before_make_executable(self, remote_file_path: str, *_, **__):
        # check remote file exists
        if not self.is_file_exists(remote_file_path):
            raise FileNotFoundError(f"Remote file '{remote_file_path}' does not exist.")

        logger.debug(f"Make file '{remote_file_path}' executable on {self}.")

    def after_make_executable(self, remote_file_path: str, *_, **__):
        logger.info(f"File '{remote_file_path}' made executable on {self}.")

    @wrap(before=before_make_executable, after=after_make_executable)
    def make_executable(self, remote_file_path: str) -> None:
        """
        Make a file executable on the remote host.

        :param remote_file_path: Path to the file on the remote host
        :return: None
        """

        self.execute_command(f"chmod +x {remote_file_path}")

    def make_dir(self, remote_dir_path: str, parents: bool = False) -> None:
        self.execute_command(f"mkdir {'-p' if parents else ''} {remote_dir_path}")

    def delete_dir(self, remote_dir_path: str) -> None:
        self.execute_command(f"rm -r {remote_dir_path}")

    def execute_command(self,
                        command: str,
                        expected_exit_code: Optional[int] = 0) -> tuple[bool, list[str], list[str]]:
        # execute command
        stdin, stdout, stderr = self.client.exec_command(command)

        stdout_list = []
        stderr_list = []

        while True:
            if stdout.channel.recv_ready():
                output_stdout = stdout.readline()
                output_stdout = output_stdout.strip()
                logger.debug(f"stdout: {output_stdout}")
                stdout_list.append(output_stdout)
                continue
            if stderr.channel.recv_stderr_ready():
                output_stderr = stderr.readline()
                output_stderr = output_stderr.strip()
                logger.debug(f"stderr: {output_stderr}")
                stderr_list.append(output_stderr)
                continue
            if stdout.channel.closed and stderr.channel.closed:
                for line in stdout:
                    output_stdout = line.strip()
                    logger.debug(f"stdout: {output_stdout}")
                    stdout_list.append(output_stdout)

                for line in stderr:
                    output_stderr = line.strip()
                    logger.debug(f"stderr: {output_stderr}")
                    stderr_list.append(output_stderr)
                break

        # get exit status
        exit_status = stdout.channel.recv_exit_status()

        return exit_status, stdout_list, stderr_list

    def execute_file(self,
                     local_file_path: Path,
                     remote_path: str = "",
                     expected_exit_code: Optional[int] = 0,
                     overwrite: bool = False) -> tuple[int, list[str], list[str]]:

        # put local file to remote host
        remote_file_path = f"{remote_path}/{local_file_path.name}"
        self.put_file(local_file_path=local_file_path, remote_file_path=remote_file_path, overwrite=overwrite)

        # make remote file executable
        self.make_executable(remote_file_path)

        # execute remote file
        result = self.execute_command(remote_file_path, expected_exit_code=expected_exit_code)

        # remove remote file
        self.delete_file(remote_file_path)

        return result
