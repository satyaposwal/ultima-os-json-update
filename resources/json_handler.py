# aws cli to download the s3 bucket reources to the given local path

import json


class JsonHandler():
    def __init__(self) -> None:
        pass

    def readJson(self, filePath):
        with open(filePath, 'r') as f:
            data = json.load(f)
            return data

    def writeJson(self, data, filePath):
        with open(filePath, 'w') as f:
            json.dump(data, f, indent=2)
