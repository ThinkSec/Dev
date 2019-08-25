#playground for JSON
import json

#load json from file, goes into python 'dictionary'
with open('importme.json') as f:
  data = json.load(f)

#print all objects in 'ec2types'
print(data['ec2types'])

#print all ec2 definitions with "AssociatePublicIpAddress": true
for A in data['ec2types']['ec2definition']:
    if A['AssociatePublicIpAddress'] == True:
        print(A['SubnetId'])