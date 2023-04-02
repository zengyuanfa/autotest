import paramiko


class LinuxConnection:
    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = None
        self.sftp = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.host, username=self.username, password=self.password, banner_timeout=10)
        self.sftp = self.client.open_sftp()

    def download_dir(self, remote_dir, local_dir):
        self.sftp.chdir(remote_dir)
        for file_name in self.sftp.listdir():
            remote_file = remote_dir + "/" + file_name
            local_file = local_dir + "/" + file_name
            if self.sftp.stat(remote_file).st_size > 0:
                self.sftp.get(remote_file, local_file)
            else:
                with open(local_file, 'w') as f:
                    pass

    def disconnect(self):
        if self.client:
            self.client.close()


if __name__ == '__main__':
    host = 'host'
    username = 'root'
    password = 'password'
    conn = LinuxConnection(host, username, password)
    conn.connect()
    remote_path = '/home/files'
    local_path = 'download/'
    conn.download_dir(remote_path, local_path)
    conn.disconnect()
