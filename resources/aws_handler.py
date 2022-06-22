import subprocess


class AWSHandler():
    def __init__(self) -> None:
        pass

    def s3Download(self, remote_folder_name, local_path) -> None:
        subprocess.run(["aws", "s3", "cp", remote_folder_name,
                       local_path])
    
    def s3Upload(self,remote_folder_name, local_path):
        subprocess.run(["aws", "s3", "cp", local_path, remote_folder_name])