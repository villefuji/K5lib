from os import environ as env
import k5lib
import logging

# add filemode="w" to overwrite
logging.basicConfig(filename="get_domainid.log", level=logging.DEBUG)

username = env['OS_USERNAME']
password = env['OS_PASSWORD']
domain = env['OS_USER_DOMAIN_NAME']

domainId = k5lib.get_domain_id(username, password, domain)
print(domainId)