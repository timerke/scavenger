import os
from paramiko import AutoAddPolicy, SSHClient, Transport
from paramiko.sftp_client import SFTPClient


class ExtendedSFTPClient(SFTPClient):

    def mkdir(self, path: str, mode=511, ignore_existing: bool = False) -> None:
        try:
            super().mkdir(path, mode)
        except IOError:
            if ignore_existing:
                pass
            else:
                raise

    def put_dir(self, source: str, target: str) -> None:
        self.mkdir(target, ignore_existing=True)
        for item in os.listdir(source):
            if os.path.isfile(os.path.join(source, item)):
                self.put(os.path.join(source, item), "%s/%s" % (target, item))
            else:
                self.mkdir("%s/%s" % (target, item), ignore_existing=True)
                self.put_dir(os.path.join(source, item), "%s/%s" % (target, item))


class RemoteHost:

    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        """
        :param host: host of remote machine to which you want to connect via ssh;
        :param port: post of remote machine;
        :param username: login of user in remote machine;
        :param password: password of user in remote machine.
        """

        self._host: str = host
        self._port: int = port
        self._username: str = username
        self._password: str = password
        transport = Transport((host, port,))
        transport.connect(None, username, password)
        self._ftp: ExtendedSFTPClient = ExtendedSFTPClient.from_transport(transport)
        self._ssh: SSHClient = SSHClient()
        self._ssh.load_system_host_keys()
        self._ssh.set_missing_host_key_policy(AutoAddPolicy())
        self._ssh.connect(host, port, username, password)

    @property
    def ftp(self) -> ExtendedSFTPClient:
        return self._ftp

    @property
    def host(self) -> str:
        return self._host

    @property
    def password(self) -> str:
        return self._password

    @property
    def ssh(self) -> SSHClient:
        return self._ssh

    @property
    def username(self) -> str:
        return self._username

    def exec_command(self, command: str, sudo: bool = False) -> None:
        stdin, stdout, stderr = self._ssh.exec_command(command, get_pty=True)
        if sudo:
            stdin.write(self._password + "\n")
            stdin.flush()
        for line in iter(stdout.readline, ""):
            print(line, end="", flush=True)
