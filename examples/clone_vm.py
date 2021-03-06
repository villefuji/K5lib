from os import environ as env
import sys
sys.path.append('k5lib')
import k5lib

# Create a log file
k5lib.create_logfile('clone_vm.log')

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']
projectName = env['OS_PROJECT_NAME']
region = env['OS_REGION_NAME']

projectToken = k5lib.get_project_token(username, password, domain, projectName, region)
projectId = k5lib.get_project_id(username, password, domain, projectName, region)

volumeId = 'REPLACE WITH volumeId'
imageName = 'mgmt_exported_OS'

imageId = k5lib.clone_vm(projectToken, projectId, region, imageName, volumeId)
print(imageId)
