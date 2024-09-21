import logging
import socket
from abc import ABC, abstractmethod
from ipaddress import IPv4Address
from pathlib import Path
from typing import Union, Optional

from wiederverwendbar.before_after_wrap import wrap, WrappedClass
from wiederverwendbar.functions.wait_ping import wait_ping

from remote_host.objects import DirectoryObject, FileObject

logger = logging.getLogger(__name__)


class BaseRemoteHost(ABC, metaclass=WrappedClass):
    """
    Base class for remote hosts.
    """

    def __init__(self,
                 host: Union[str, IPv4Address],
                 username: str,
                 password: str,
                 port: int,
                 check_ping: bool = True,
                 check_ping_timeout: int = 5,
                 check_ping_verbose: bool = False,
                 check_port: bool = True):
        self.host = str(host)
        self.username = username
        self.password = password
        self.port = port
        self.check_ping = check_ping
        self.check_ping_timeout = check_ping_timeout
        self.check_ping_verbose = check_ping_verbose
        self.check_port = check_port

        logger.debug(f"Create {self}.")

    def __str__(self):
        return f"{self.__class__.__name__}(host={self.host}, connected={self.is_connected})"

    def __del__(self):
        if self.is_connected:
            self.disconnect()

    def __enter__(self) -> "BaseRemoteHost":
        # connect to host
        self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # disconnect from host
        if self.is_connected:
            self.disconnect()

    def _check_ping(self) -> None:
        if not wait_ping(host=self.host, timeout=1, count=self.check_ping_timeout, verbose=self.check_ping_verbose):
            raise RuntimeError(f"Remote host {self} is not pingable.")

    @property
    def client_hostname(self) -> str:
        """
        Get the hostname of the client.

        :return: Hostname of the client
        """

        return socket.gethostname()

    def before_is_tcp_port_open(self, port: int, *_, **__):
        logger.debug(f"Check if port '{port}' is open on {self}.")

    def after_is_tcp_port_open(self, port: int, __ba_result__: bool, *_, **__) -> None:
        if __ba_result__:
            logger.debug(f"Port '{port}' is open on {self}.")
        else:
            logger.debug(f"Port '{port}' is not open on {self}.")

    @wrap(before=before_is_tcp_port_open, after=after_is_tcp_port_open)
    def is_tcp_port_open(self, port: int) -> bool:
        """
        Check if port is open on Remote Host.

        :param port: Port to check.
        :return: True if port is open.
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if sock.connect_ex((self.host, port)) == 0:
            return True

        return False

    def before_connect(self, *_, **__):
        # check if already connected
        if self.is_connected:
            raise RuntimeError(f"Already connected to {self}.")

        logger.debug(f"Connect to {self}.")

        # ping remote host if enabled
        if self.check_ping:
            self._check_ping()

        # check if port is open
        if self.check_port:
            if not self.is_tcp_port_open(self.port):
                raise ConnectionRefusedError(f"Port '{self.port}' is not open on {self}.")

    def after_connect(self, *_, **__):
        # check if not connected
        if not self.is_connected:
            raise RuntimeError(f"Not connected to {self}.")

        logger.info(f"Connected to {self}.")

    @abstractmethod
    @wrap(before=before_connect, after=after_connect)
    def connect(self) -> None:
        """
        Connect to the remote host.

        :return: None
        """
        ...

    def before_disconnect(self, *_, **__):
        # check if already disconnected
        if not self.is_connected:
            raise RuntimeError(f"Already disconnected from {self}.")

        logger.debug(f"Disconnect from {self}.")

    def after_disconnect(self, *_, **__):
        # check if connected
        if self.is_connected:
            raise RuntimeError(f"Not disconnected from {self}.")

        logger.info(f"Disconnected from {self}.")

    @abstractmethod
    @wrap(before=before_disconnect, after=after_disconnect)
    def disconnect(self) -> None:
        """
        Disconnect from the remote host.

        :return: None
        """
        ...

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        """
        Check if connected to the remote host.

        :return: True if connected, False otherwise
        """
        ...

    def before_list_dir(self, remote_dir_path: str, *_, **__):
        logger.debug(f"List directory '{remote_dir_path}' on {self}.")

    def after_list_dir(self, remote_dir_path: str, *_, **__) -> None:
        logger.debug(f"Directory '{remote_dir_path}' on {self} listed successfully.")

    @abstractmethod
    @wrap(before=before_list_dir, after=after_list_dir)
    def list_dir(self, remote_dir_path: str) -> list[Union[DirectoryObject, FileObject]]:
        """
        List directory on Remote Host.

        :param remote_dir_path: Path to directory.
        :return: List of DirectoryObject or FileObject.
        """
        ...

    def before_is_exists(self, remote_path: str, *_, **__):
        logger.debug(f"Check if path '{remote_path}' exists on {self}.")

    def after_is_exists(self, remote_path: str, __ba_result__: bool, *_, **__) -> None:
        if __ba_result__:
            logger.debug(f"Path '{remote_path}' exists on {self}.")
        else:
            logger.debug(f"Path '{remote_path}' does not exist on {self}.")

    @abstractmethod
    @wrap(before=before_is_exists, after=after_is_exists)
    def is_exists(self, remote_path: str) -> bool:
        """
        Check if a path exists on the remote host.

        :param remote_path: Path on the remote host
        :return: True if the path exists, False otherwise
        """
        ...

    def before_is_file_exists(self, remote_file_path: str, *_, **__):
        logger.debug(f"Check if file '{remote_file_path}' exists on {self}.")

    def after_is_file_exists(self, remote_file_path: str, __ba_result__: bool, *_, **__) -> None:
        if __ba_result__:
            logger.debug(f"File '{remote_file_path}' exists on {self}.")
        else:
            logger.debug(f"File '{remote_file_path}' does not exist on {self}.")

    @abstractmethod
    @wrap(before=before_is_file_exists, after=after_is_file_exists)
    def is_file_exists(self, remote_file_path: str) -> bool:
        """
        Check if a file exists on the remote host.

        :param remote_file_path: Path to the file on the remote host
        :return: True if the file exists, False otherwise
        """
        ...

    def before_get_file(self, remote_file_path: str, local_file_path: Path, *_, overwrite: bool = False, **__):
        # check remote file exists
        if not self.is_file_exists(remote_file_path):
            raise FileNotFoundError(f"Remote file '{remote_file_path}' does not exist.")

        # check local file exists
        if local_file_path.is_file():
            if not overwrite:
                raise FileExistsError(f"Local file '{local_file_path}' already exists.")
            local_file_path.unlink()

        logger.debug(f"Get remote file '{remote_file_path}' to local file '{local_file_path}'.")

    def after_get_file(self, remote_file_path: str, local_file_path: Path, *_, **__) -> None:
        logger.info(f"Remote file '{remote_file_path}' get to local file '{local_file_path}'.")

    @abstractmethod
    @wrap(before=before_get_file, after=after_get_file)
    def get_file(self, remote_file_path: str, local_file_path: Path, overwrite: bool = False) -> None:
        """
        Get a file from the remote host to the local machine.

        :param remote_file_path: Path to the file on the remote host
        :param local_file_path: Path to the file on the local machine
        :param overwrite: Overwrite local file if it exists
        :return: None
        """
        ...

    def before_put_file(self, local_file_path: Path, remote_file_path: str, *_, overwrite: bool = False, **__):
        # check local file exists
        if not local_file_path.is_file():
            raise FileNotFoundError(f"Local file '{local_file_path}' does not exist.")

        # check remote file exists
        if self.is_file_exists(remote_file_path):
            if not overwrite:
                raise FileExistsError(f"Remote file '{remote_file_path}' already exists.")
            self.delete_file(remote_file_path)

        logger.debug(f"Put local file '{local_file_path}' to remote file '{remote_file_path}'.")

    def after_put_file(self, local_file_path: Path, remote_file_path: str, *_, **__) -> None:
        logger.info(f"Local file '{local_file_path}' put to remote file '{remote_file_path}'.")

    @abstractmethod
    @wrap(before=before_put_file, after=after_put_file)
    def put_file(self, local_file_path: Path, remote_file_path: str, overwrite: bool = False) -> None:
        """
        Put a file from the local machine to the remote host.

        :param local_file_path: Path to the file on the local machine
        :param remote_file_path: Path to the file on the remote host
        :param overwrite: Overwrite remote file if it exists
        :return: None
        """
        ...

    def before_delete_file(self, remote_file_path: str, *_, **__):
        # check remote file exists
        if not self.is_file_exists(remote_file_path):
            raise FileNotFoundError(f"Remote file '{remote_file_path}' does not exist.")

        logger.debug(f"Delete file '{remote_file_path}' from {self}.")

    def after_delete_file(self, remote_file_path: str, *_, **__) -> None:
        logger.info(f"Deleted file '{remote_file_path}' from {self}.")

    @abstractmethod
    @wrap(before=before_delete_file, after=after_delete_file)
    def delete_file(self, remote_file_path: str) -> None:
        """
        Delete a file from the remote host.

        :param remote_file_path: Path to the file on the remote host
        :return: None
        """
        ...

    def before_is_dir_exists(self, remote_dir_path: str, *_, **__):
        logger.debug(f"Check if directory '{remote_dir_path}' exists on {self}.")

    def after_is_dir_exists(self, remote_dir_path: str, __ba_result__: bool, *_, **__) -> None:
        if __ba_result__:
            logger.debug(f"Directory '{remote_dir_path}' exists on {self}.")
        else:
            logger.debug(f"Directory '{remote_dir_path}' does not exist on {self}.")

    @abstractmethod
    @wrap(before=before_is_dir_exists, after=after_is_dir_exists)
    def is_dir_exists(self, remote_dir_path: str) -> bool:
        """
        Check if a directory exists on the remote host.

        :param remote_dir_path: Path to the directory on the remote host
        :return: True if the directory exists, False otherwise
        """
        ...

    def before_make_dir(self, remote_dir_path: str, *_, parents: bool = False, **__):
        # check if directory exists
        if self.is_dir_exists(remote_dir_path):
            if not parents:
                raise FileExistsError(f"Remote directory '{remote_dir_path}' already exists.")

        logger.debug(f"Make directory '{remote_dir_path}' on {self}.")

    def after_make_dir(self, remote_dir_path: str, *_, **__):
        logger.info(f"Directory '{remote_dir_path}' made on {self}.")

    @abstractmethod
    @wrap(before=before_make_dir, after=after_make_dir)
    def make_dir(self, remote_dir_path: str, parents: bool = False) -> None:
        """
        Make a directory on the remote host.

        :param remote_dir_path: Path to the directory on the remote host
        :param parents: Create parent directories if they do not exist
        :return: None
        """
        ...

    def before_delete_dir(self, remote_dir_path: str, *_, **__):
        # check if directory exists
        if not self.is_dir_exists(remote_dir_path):
            raise FileNotFoundError(f"Remote directory '{remote_dir_path}' does not exist.")

        logger.debug(f"Delete directory '{remote_dir_path}' from {self}.")

    def after_delete_dir(self, remote_dir_path: str, *_, **__):
        logger.info(f"Deleted directory '{remote_dir_path}' from {self}.")

    @abstractmethod
    @wrap(before=before_delete_dir, after=after_delete_dir)
    def delete_dir(self, remote_dir_path: str) -> None:
        """
        Delete a directory from the remote host.

        :param remote_dir_path: Path to the directory on the remote host
        :return: None
        """
        ...

    def before_execute_command(self, command: str, *_, **__):
        logger.debug(f"Execute command '{command}' on {self}.")

    def after_execute_command(self, command: str, __ba_result__: tuple[int, list[str], list[str]], *_, expected_exit_code: Optional[int] = 0, **__):
        if expected_exit_code is not None:
            if __ba_result__[0] == expected_exit_code:
                logger.info(f"Command '{command}' executed successfully on {self}.")
            else:
                raise RuntimeError(f"Command '{command}' failed on {self}.")

    @abstractmethod
    @wrap(before=before_execute_command, after=after_execute_command)
    def execute_command(self,
                        command: str,
                        expected_exit_code: Optional[int] = 0) -> tuple[int, list[str], list[str]]:
        """
        Execute a command on the remote host.

        :param command: Command to execute
        :param expected_exit_code: Expected exit code. If None, no check will be done. Default is 0
        :return: Exit code, stdout and stderr
        """
        ...

    def before_execute_file(self, local_file_path: Path, *_, **__):
        logger.debug(f"Execute file '{local_file_path}' on {self}.")

    def after_execute_file(self, local_file_path: Path, __ba_result__: tuple[int, list[str], list[str]], *_, expected_exit_code: Optional[int] = 0, **__):
        if expected_exit_code is not None:
            if __ba_result__[0] == expected_exit_code:
                logger.info(f"File '{local_file_path}' executed successfully on {self}.")
            else:
                raise RuntimeError(f"File '{local_file_path}' failed on {self}.")

    @abstractmethod
    @wrap(before=before_execute_file, after=after_execute_file)
    def execute_file(self,
                     local_file_path: Path,
                     remote_path: str = "",
                     expected_exit_code: Optional[int] = 0,
                     overwrite: bool = False) -> tuple[int, list[str], list[str]]:
        """
        Copy a file from the local machine to the remote machine
        After that execute the file on the remote machine.

        :param local_file_path: Local file path
        :param remote_path: Path on the remote machine
        :param expected_exit_code: Expected exit code. If None, no check will be done. Default is 0
        :param overwrite: Overwrite remote file if it exists

        :return: True if the file was copied and executed successfully, False otherwise
        """
        ...
