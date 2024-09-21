import logging
import time
from ipaddress import IPv4Address
from pathlib import Path
from typing import Union, Optional

from pypsexec.client import Client
from smb.SMBConnection import SMBConnection

from remote_host import DirectoryObject, FileObject
from remote_host.base_remote_host import BaseRemoteHost

logger = logging.getLogger(__name__)


class WindowsRemoteHost(BaseRemoteHost):
    def __init__(self,
                 host: Union[str, IPv4Address],
                 username: str,
                 password: str,
                 domain: str = "",
                 port: int = 445,
                 share: str = "C$",
                 check_ping: bool = True,
                 check_ping_timeout: int = 5,
                 check_ping_verbose: bool = False,
                 check_port: bool = True,
                 encryption: bool = True):
        self._domain = domain
        self._share = share
        self._encryption = encryption
        self._smb_connection: Optional[SMBConnection] = None
        self._client: Optional[Client] = None

        super().__init__(host=host,
                         username=username,
                         password=password,
                         port=port,
                         check_ping=check_ping,
                         check_ping_timeout=check_ping_timeout,
                         check_ping_verbose=check_ping_verbose,
                         check_port=check_port)

    def __enter__(self) -> "WindowsRemoteHost":
        super().__enter__()

        return self

    @property
    def domain(self) -> str:
        """
        Get the domain of the remote host.

        :return: Domain of the remote host
        """

        return self._domain

    @property
    def share(self) -> str:
        """
        Get the share of the remote host.

        :return: Share of the remote host
        """

        return self._share

    @property
    def encryption(self) -> bool:
        """
        If True, the connection will be encrypted.

        :return: Value of encryption
        """

        return self._encryption

    def connect(self) -> None:
        # create smb connection
        self._smb_connection = SMBConnection(username=self.username,
                                             password=self.password,
                                             my_name=self.client_hostname,
                                             remote_name=self.host,
                                             domain=self.domain,
                                             sign_options=SMBConnection.SIGN_WHEN_REQUIRED,
                                             is_direct_tcp=True)
        self._smb_connection.connect(self.host, self.port)

        # check if share available
        share_available = False
        for share in self._smb_connection.listShares():
            if share.name == self.share:
                share_available = True
                break
        if not share_available:
            raise ConnectionRefusedError(f"Share '{self.share}' is not available on {self}.")

        # create client
        self._client = Client(server=self.host,
                              username=f"{self.domain}\\{self.username}" if self.domain else self.username,
                              password=self.password,
                              port=self.port,
                              encrypt=self.encryption)
        self._client.connect()
        self._client.create_service()

    def disconnect(self) -> None:
        # cleanup and disconnect from client
        self._client.cleanup()
        self._client.disconnect()
        self._client = None

        # disconnect from smb connection
        self._smb_connection.close()
        self._smb_connection = None

    @property
    def is_connected(self) -> bool:
        if self._smb_connection is None:
            return False
        if self._smb_connection.session_id == 0:
            return False
        if self._client is None:
            return False
        if self._client.session.session_id == 0:
            return False
        if getattr(getattr(self._client, "_service"), "_handle") is None:
            return False
        return True

    @property
    def smb_connection(self) -> SMBConnection:
        if not self.is_connected:
            raise RuntimeError(f"Not connected to {self}.")
        return self._smb_connection

    @property
    def client(self) -> Client:
        if not self.is_connected:
            raise RuntimeError(f"Not connected to {self}.")
        return self._client

    def list_dir(self, remote_dir_path: str) -> list[Union[DirectoryObject, FileObject]]:
        objs = []

        for file in self.smb_connection.listPath(self.share, remote_dir_path):
            if file.filename == ".":
                continue
            if file.filename == "..":
                continue
            if file.isDirectory:
                objs.append(DirectoryObject(name=file.filename, path=file.filename if remote_dir_path == "" else f"{remote_dir_path}/{file.filename}"))
            else:
                objs.append(FileObject(name=file.filename, path=file.filename if remote_dir_path == "" else f"{remote_dir_path}/{file.filename}", size=file.file_size))

        return objs

    def is_exists(self, remote_path: str) -> bool:
        remote_path = remote_path.replace("\\", "/")
        remote_path_parent = str(Path(remote_path).parent).replace("\\", "/")
        if remote_path_parent == ".":
            remote_path_parent = ""
        for obj in self.list_dir(remote_path_parent):
            if remote_path == obj.path:
                return True
        return False

    def is_file_exists(self, remote_file_path: str) -> bool:
        remote_file_path = remote_file_path.replace("\\", "/")
        remote_file_parent = str(Path(remote_file_path).parent).replace("\\", "/")
        if remote_file_parent == ".":
            remote_file_parent = ""
        for obj in self.list_dir(remote_file_parent):
            if type(obj) is not FileObject:
                continue
            if remote_file_path == obj.path:
                return True
        return False

    def get_file(self, remote_file_path: str, local_file_path: Path, overwrite: bool = False) -> None:
        with open(local_file_path, 'wb', buffering=0) as file:
            self.smb_connection.retrieveFile(self.share, remote_file_path, file)

    def put_file(self, local_file_path: Path, remote_file_path: str, overwrite: bool = False) -> None:
        with open(local_file_path, 'rb', buffering=0) as file:
            self.smb_connection.storeFile(self.share, remote_file_path, file)

    def delete_file(self, remote_file_path: str) -> None:
        self.smb_connection.deleteFiles(self.share, remote_file_path)

    def is_dir_exists(self, remote_dir_path: str) -> bool:
        remote_dir_path = remote_dir_path.replace("\\", "/")
        remote_dir_parent = str(Path(remote_dir_path).parent).replace("\\", "/")
        if remote_dir_parent == ".":
            remote_dir_parent = ""
        for obj in self.list_dir(remote_dir_parent):
            if type(obj) is not DirectoryObject:
                continue
            if remote_dir_path == obj.path:
                return True
        return False

    def make_dir(self, remote_dir_path: str, parents: bool = False) -> None:
        self.smb_connection.createDirectory(self.share, remote_dir_path)

    def delete_dir(self, remote_dir_path: str, recursive: bool = False) -> None:
        self.smb_connection.deleteDirectory(self.share, remote_dir_path)

    def execute_command(self, command: str, expected_exit_code: Optional[int] = 0) -> tuple[int, list[str], list[str]]:
        executable = command.split(" ")[0]
        arguments = " ".join(command.split(" ")[1:])

        try:
            stdout, stderr, exit_code = self.client.run_executable(executable, arguments)
        except Exception as e:
            self.disconnect()
            logger.error(f"Failed to execute command\n{e}")
            raise SystemExit(1)

        stdout_str = stdout.decode("utf-8", errors="ignore")
        stderr_str = stderr.decode("utf-8", errors="ignore")

        stdout_lines = stdout_str.split("\n")
        stderr_lines = stderr_str.split("\n")

        for line in stdout_lines:
            line = line.strip()
            if len(stdout_lines) == 1 and line == "":
                continue
            logger.debug(f"stdout: {line}")

        for line in stderr_lines:
            line = line.strip()
            if len(stderr_lines) == 1 and line == "":
                continue
            logger.debug(f"stderr: {line}")

        return exit_code, stdout_lines, stderr_lines

    def execute_file(self,
                     local_file_path: Path,
                     remote_path: str = "",
                     expected_exit_code: Optional[int] = 0,
                     overwrite: bool = False) -> tuple[int, list[str], list[str]]:

        # put local file to remote host
        remote_file_path = f"{remote_path}/{local_file_path.name}"
        self.put_file(local_file_path=local_file_path, remote_file_path=remote_file_path, overwrite=overwrite)

        # execute remote file
        result = self.execute_command(remote_file_path, expected_exit_code=expected_exit_code)

        # remove remote file
        self.delete_file(remote_file_path)

        return result

    def cmd(self,
            command: str,
            expected_exit_code: Optional[int] = 0) -> tuple[int, list[str], list[str]]:
        """
        Execute command on Remote Host.

        :param command: Command to execute.
        :param expected_exit_code: Expected exit code of command. If None, no check will be done. Default: 0
        :return: True if command was executed successfully.
        """

        command = f"cmd.exe /c {command}"

        return self.execute_command(command=command, expected_exit_code=expected_exit_code)

    def powershell(self,
                   command: str,
                   expected_exit_code: Optional[int] = 0) -> tuple[int, list[str], list[str]]:
        """
        Execute command on Remote Host.

        :param command: Command to execute.
        :param expected_exit_code: Expected exit code of command. If None, no check will be done. Default: 0
        :return: True if command was executed successfully.
        """

        command = f"powershell.exe -Command \"& {{{command}}}\""

        return self.execute_command(command=command, expected_exit_code=expected_exit_code)

    def get_installed_software(self) -> list[tuple[str, str]]:
        """
        Get installed software and uninstall strings on Remote Host.

        :return: List of installed software.
        """

        logger.debug(f"Get installed software on {self}.")

        installed_software = []

        def parse_stdout():
            for line in stdout:
                if line == "_-__-_" or "_-_" not in line:
                    continue
                line_split = line.split("_-_")
                software = line_split[0]
                if software == "":
                    continue
                uninstall_string = line_split[1]
                quiet_uninstall_string = line_split[2]
                if quiet_uninstall_string == "":
                    if uninstall_string == "":
                        continue
                    if "msiexec" not in uninstall_string.lower():
                        continue
                    uninstall_string = uninstall_string.replace("/I", "/x").replace("/i", "/x").replace("{", " \"{").replace("}", "}\"")
                    if not "/quiet" in uninstall_string.lower():
                        quiet_uninstall_string = uninstall_string + " /quiet"
                    else:
                        quiet_uninstall_string = uninstall_string
                installed_software.append((software, quiet_uninstall_string))

        command_x86 = ("$InstalledSoftware = Get-ChildItem \"HKLM:\\Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\"; "
                       "foreach($obj in $InstalledSoftware){write-host $obj.GetValue('DisplayName')-NoNewline; "
                       "write-host \" _-_ \" -NoNewline; write-host $obj.GetValue('UninstallString') -NoNewline; "
                       "write-host \" _-_ \" -NoNewline; write-host $obj.GetValue('QuietUninstallString')}")

        _, stdout, _ = self.powershell(command=command_x86, expected_exit_code=0)

        parse_stdout()

        command_x64 = ("$InstalledSoftware = Get-ChildItem \"HKLM:\\SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\"; "
                       "foreach($obj in $InstalledSoftware){write-host $obj.GetValue('DisplayName')-NoNewline; "
                       "write-host \" _-_ \" -NoNewline; write-host $obj.GetValue('UninstallString') -NoNewline; "
                       "write-host \" _-_ \" -NoNewline; write-host $obj.GetValue('QuietUninstallString')}")

        try:
            _, stdout, _ = self.powershell(command=command_x64, expected_exit_code=0)

            parse_stdout()
        except RuntimeError:
            pass

        return installed_software

    def is_software_installed(self, software: str) -> bool:
        """
        Check if software is installed on Remote Host.

        :param software: Software to check.
        :return: True if software is installed.
        """

        logger.debug(f"Check if software '{software}' is installed on {self}.")

        installed_software = self.get_installed_software()

        for s, _ in installed_software:
            if s == software:
                logger.debug(f"Software '{s}' is installed on {self}.")
                return True

        logger.debug(f"Software '{software}' is not installed on {self}.")
        return False

    def get_uninstall_string(self, software: str) -> Optional[str]:
        """
        Get uninstall string of software on Remote Host.

        :param software: Software to check.
        :return: Uninstall string or None if not available.
        """

        logger.debug(f"Get uninstall string of software '{software}' on {self}.")

        installed_software = self.get_installed_software()

        for s, u in installed_software:
            if s == software:
                logger.debug(f"Uninstall string of software '{software}' on {self} is '{u}'.")
                return u

        logger.debug(f"Uninstall string of software '{software}' on {self} is not available.")
        return None

    def uninstall_software(self, software: str, install_check_retries: int, install_check_delay: float) -> bool:
        """
        Uninstall software on Remote Host.

        :param software: Software to uninstall.
        :param install_check_retries: Number of retries to check if software is uninstalled.
        :param install_check_delay: Delay between retries to check if software is uninstalled.
        :return: True if software was uninstalled successfully.
        """

        logger.debug(f"Uninstalling '{software}' on host {self} ...")

        # get uninstall command
        uninstall_command = self.get_uninstall_string(software=software)

        if uninstall_command is None:
            logger.error(f"Uninstall command for '{software}' not found on '{self}'.")
            return False

        # get process name
        try:
            process_name = uninstall_command[:uninstall_command.index(".exe")]
        except ValueError:
            try:
                process_name = uninstall_command[:uninstall_command.index(".EXE")]
            except ValueError:
                logger.error(f"Process name not found in uninstall command '{uninstall_command}'.")
                return False
        if "\\" in process_name:
            process_name = process_name[::-1][:process_name[::-1].index("\\")][::-1]
        process_name = process_name.replace("'", "").replace('"', "")

        # execute uninstall command
        if not self.cmd(f"{uninstall_command}"):
            return False

        # check if uninstall process is still running
        for check_try in range(install_check_retries):
            if self.is_process_running(process_name=process_name):
                logger.debug(f"'{software}' setup is still running on host {self}. Sleeping for {install_check_delay} seconds.")
                time.sleep(install_check_delay)
                continue
            break

        logger.debug(f"Check if '{software}' is installed.")
        if self.is_software_installed(software=software):
            logger.error(f"'{software}' was not uninstalled on {self}.")
            return False

        logger.info(f"'{software}' uninstalled successfully on {self}.")

        return True

    def get_service_status(self, service_name: str) -> bool:
        """
        Get service status on Remote Host.

        :param service_name: Service name.
        :return: Service status.
        """

        logger.debug(f"Get service status of '{service_name}' on {self}.")

        command = f"sc.exe query {service_name}"

        _, stdout, _ = self.cmd(command=command, expected_exit_code=0)

        service_state = "UNKNOWN"
        for line in stdout:
            if "STATE" in line:
                service_state = line.split(" ")[-2]
                break

        logger.debug(f"Service status of '{service_name}' on {self} is '{service_state}'.")

        if service_state == "RUNNING":
            return True

        return False

    def restart_service(self, service_name: str) -> bool:
        """
        Restart service on Remote Host.

        :param service_name: Service name.
        :return: True if service was restarted successfully.
        """

        logger.debug(f"Restart service '{service_name}' on {self}.")

        command = f"Restart-Service {service_name} -Force"

        return self.powershell(command=command, expected_exit_code=0)[0] == 0

    def get_processes(self) -> list[str]:
        """
        Get processes on Remote Host.

        :return: List of processes.
        """

        logger.debug(f"Get processes on {self}.")

        command = "Get-Process | Format-Table -HideTableHeaders -Property ProcessName"

        _, stdout, _ = self.powershell(command=command, expected_exit_code=0)

        processes = []

        for line in stdout:
            if line.strip() == "":
                continue
            processes.append(line.strip())

        return processes

    def is_process_running(self, process_name: str) -> bool:
        """
        Check if process is running on Remote Host.

        :param process_name: Process to check.
        :return: True if process is running.
        """

        logger.debug(f"Check if process '{process_name}' is running on {self}.")

        processes = self.get_processes()

        if process_name in processes:
            logger.debug(f"Process '{process_name}' is running on {self}.")
            return True

        logger.debug(f"Process '{process_name}' is not running on {self}.")
        return False
