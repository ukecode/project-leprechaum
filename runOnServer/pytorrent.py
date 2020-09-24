import subprocess
 
class torrentClass (object):
    def __init__(self, auth):
        self.auth = auth
    
    def download_new_torrent(self,msg):
        command = subprocess.run(["transmission-remote", "-n", self.auth, "-a", msg])
        print("Command ok")
        return command.returncode

    def list_torrent(self):
        command = subprocess.run(["transmission-remote", "-n", self.auth, "-l"],stdout=subprocess.PIPE, text=True)
        return command.stdout

    def start_all_torrents(self):
        command = subprocess.run(["transmission-remote", "-n", self.auth, "-s"],stdout=subprocess.PIPE, text=True)
        return command.stdout

    def start_torrent_id(self, id):
        command = subprocess.run(["transmission-remote", "-n", self.auth, "-s", "-t", id],stdout=subprocess.PIPE, text=True)
        return command.stdout

    def stop_all_torrents(self):
        command = subprocess.run(["transmission-remote", "-n", self.auth, "-S"],stdout=subprocess.PIPE, text=True)
        return command.stdout

    def list_status(self):
        command = subprocess.run(["transmission-remote", "-n", self.auth, "-si"],stdout=subprocess.PIPE, text=True)
        return command.stdout

    def commands(self, cmds):
        cmds = cmds.split()
        command = subprocess.run(cmds,stdout=subprocess.PIPE, text=True)
        print(command)
        return command.stdout

    def changeDownloadDirectory(self, directory):
        self.directory = directory
        command = subprocess.run(["transmission-remote", "-n", self.auth, "-c", directory],stdout=subprocess.PIPE, text=True)
        command = subprocess.run(["transmission-remote", "-n", self.auth, "-C", directory],stdout=subprocess.PIPE, text=True)
