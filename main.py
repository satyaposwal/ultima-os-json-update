import os
import subprocess
from resources.aws_handler import AWSHandler
from resources.json_handler import JsonHandler
from datetime import date, datetime


date = datetime.now()
formattedDate = date.strftime("%Y%m%d")

# Files constants
osUpdatePkgZipFile = 'os-update-pkg.zip'
osVersionFile = 'availableOSVersions.json'
newOsBuildFp = os.environ['New_OS_build_fp']
minApkVersion = os.environ['Min_apk_version']

# S3 constants
s3URI = 's3://nextgen-os-pipeline-temp1/UltimaOS'
jsonFileS3DownLoadPath = f'{s3URI}/dev/{osVersionFile}'
jsonFileS3UploadPath = f'{s3URI}/dev/{osVersionFile}'
zipFileS3DownloadPath = f'{s3URI}/zipFiles/{osUpdatePkgZipFile}'
zipFileS3UploadPath = f'{s3URI}/dev/{formattedDate}_OS_Update/{osUpdatePkgZipFile}'

def updateavailableOSVersion():
    json = JsonHandler()
    data = json.readJson(osVersionFile)
    keys = list(data.keys())
    lastKey = keys[len(keys)-1]
    newBlock = createDataBlock()
    print('Updating the last block and adding new block')
    data[lastKey] = newBlock[newOsBuildFp]
    data[newOsBuildFp] = newBlock[newOsBuildFp]
    json.writeJson(data, osVersionFile)
    json.printJsonFile(osVersionFile)


def createDataBlock():
    newBlock = {
        newOsBuildFp: {
            'availableOSBuildFingerprint': newOsBuildFp,
            'fileName': 'os-update-pkg.zip',
            'fileLocation': f'{formattedDate}_OS_Update/os-update-pkg.zip',
            'hash': getFileHash(),
            'minApkVersion': minApkVersion
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
    aws = AWSHandler()
    # Downloading availableOSVersions.json file from S3
    aws.s3Download(remote_folder_name=jsonFileS3DownLoadPath,
                   local_path=osVersionFile)
    # Downloading artifact file from S3
    aws.s3Download(remote_folder_name=zipFileS3DownloadPath,
                   local_path=osUpdatePkgZipFile)

    # update the file
    updateavailableOSVersion()

    # Uploading availableOSVersions.json file to S3
    aws.s3Upload(remote_folder_name=jsonFileS3UploadPath,
                 local_path=osVersionFile)
    # Uploading artifact file to S3
    aws.s3Upload(remote_folder_name=zipFileS3UploadPath,
                 local_path=osUpdatePkgZipFile)


if __name__ == '__main__':
    main()
