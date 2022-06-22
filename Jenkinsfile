pipeline {
    environment {
      New_OS_build_fp = "${New_OS_build_fp}"
      Min_apk_version = "${Min_apk_version}"
      File_Name = "${File_Name}"
    }
    agent any

    stages {
        stage('Upload Zip') {
            steps {
                script {
                    def file = input message: 'Upload Os Update Pkg Zip file.', parameters: [file(name:'os-update-pkg.zip')]
                    withAWS(credentials: 'Shreyas AWS Root', region: 'ap-south-1') {
                        
                        s3Upload(
                            pathStyleAccessEnabled: true,
                            payloadSigningEnabled: true,
                            file: "${file}",
                            bucket: 'nextgen-os-art',
                            path: "UltimaOS/zipFiles/BUILD-${BUILD_NUMBER}/"
                           
                        )
                    }
                }
            }
        }
        stage('Json version update') {
            steps {
                script {
                    awsCodeBuild ( 
                        credentialsId: '6102eb68-8687-472d-b8e1-99a8fffb6a82', 
                        credentialsType: 'jenkins', 
                        downloadArtifacts: 'false', 
                        projectName: 'ultima-os-pipeline', 
                        region: 'us-east-1', 
                        sourceControlType: 'project',
                        sourceTypeOverride: 'GITHUB',
                        sourceVersion: 'DEVOPS-1',
                        envVariables: "[ { New_OS_build_fp, $New_OS_build_fp}, { Min_apk_version, $Min_apk_version}, {Build_No, $BUILD_NUMBER}]"
                    )
                }
            }
        }
        
    }
}
