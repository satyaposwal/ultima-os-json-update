import os
import subprocess
from resources.aws_handler import AWSHandler
from resources.json_handler import JsonHandler
from datetime import date, datetime


def updateavailableOSVersion():
    json = JsonHandler()
    data = json.readJson('availableOSVersions.json')
    keys = list(data.keys())
    lastKey = keys[len(keys)-1]
    newBlock = createDataBlock()
    print('Updating the last block and adding new block')
    data[lastKey] = newBlock[os.environ['New_OS_build_fp']]
    data[os.environ['New_OS_build_fp']] = newBlock[os.environ['New_OS_build_fp']]
    json.writeJson(data, 'availableOSVersions.json')


def createDataBlock():
    date = datetime.now()
    formattedDate = date.strftime("%Y%m%d")
    newBlock = {
        os.environ['New_OS_build_fp']: {
            'availableOSBuildFingerprint': os.environ['New_OS_build_fp'],
            'fileName': 'os-update-pkg.zip',
            'fileLocation': f'{formattedDate}_OS_Update/os-update-pkg.zip',
            'hash': getFileHash(),
            'minApkVersion': os.environ['Min_apk_version']
        }
    }
    return newBlock


def getFileHash():
    process = subprocess.Popen(
        ["md5sum", './os-update-pkg.zip'], stdout=subprocess.PIPE
    )
    hash = str(process.communicate()[0]).split()[0][2:]
    return hash


def main():
    fileName = os.environ["File_Name"]
    date = datetime.now()
    formattedDate = date.strftime("%Y%m%d")
    aws = AWSHandler()
    jsonFileS3DownLoadPath = 's3://nextgen-os-pipeline-temp1/UltimaOS/dev/availableOSVersions.json'
    jsonFileS3UploadPath = 's3://nextgen-os-pipeline-temp1/UltimaOS/dev/availableOSVersions.json'
    zipFileS3DownloadPath = f's3://nextgen-os-pipeline-temp1/UltimaOS/zipFiles/{fileName}'
    zipFileS3UploadPath = f's3://nextgen-os-pipeline-temp1/UltimaOS/dev/{formattedDate}_OS_Update/os-update-pkg.zip'

    # Downloading availableOSVersions.json file from S3
    aws.s3Download(remote_folder_name=jsonFileS3DownLoadPath,
                   local_path='availableOSVersions.json')
    # Downloading artifact file from S3
    aws.s3Download(remote_folder_name=zipFileS3DownloadPath,
                   local_path=fileName)
    proc = subprocess.Popen('find .', stdout=subprocess.PIPE)
    tmp = proc.stdout.read()
    print(str(tmp))
    updateavailableOSVersion()
    # Uploading availableOSVersions.json file to S3
    aws.s3Upload(remote_folder_name=jsonFileS3UploadPath,
                 local_path='availableOSVersions.json')
    # Uploading artifact file to S3
    aws.s3Upload(remote_folder_name=zipFileS3UploadPath,
                 local_path='os-update-pkg.zip')


if __name__ == '__main__':
    main()
