#source: https://blog.ipswitch.com/how-to-create-and-configure-an-aws-vpc-with-python
#json tutorial source: https://realpython.com/python-json/#python-supports-json-natively
#Use boto3 to create a simple VPC with an EC2 instance
#SSH will be open to the instance from source IP in variable SSHIPSource
import boto3
import json
json_dict = json.loads(importme.json)
ec2 = boto3.resource('ec2')

#customization
cidrVPC='172.20.0.0/16'
VPCName="demoVPC"
cidrSubnet='172.20.1.0/24'
SSHIPSource='0.0.0.0/0'

# create VPC
vpc = ec2.create_vpc(CidrBlock=cidrVPC)
vpc.create_tags(Tags=[{"Key": "Name", "Value": VPCName}])
vpc.wait_until_available()

# enable public dns hostname so that we can SSH into it later
ec2Client = boto3.client('ec2')
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsSupport = { 'Value': True } )
ec2Client.modify_vpc_attribute( VpcId = vpc.id , EnableDnsHostnames = { 'Value': True } )

# create an internet gateway and attach it to VPC
internetgateway = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=internetgateway.id)

# create a route table and a public route
routetable = vpc.create_route_table()
route = routetable.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=internetgateway.id)

# create subnet and associate it with route table
subnet = ec2.create_subnet(CidrBlock=cidrSubnet, VpcId=vpc.id)
routetable.associate_with_subnet(SubnetId=subnet.id)

# Create a security group and allow SSH inbound rule through the VPC
securitygroup = ec2.create_security_group(GroupName='Admin-SSH-ONLY', Description='only allow SSH traffic', VpcId=vpc.id)
securitygroup.authorize_ingress(CidrIp=SSHAdminIP, IpProtocol='tcp', FromPort=22, ToPort=22)

#---------------------------------------------------------------
#Create EC2 instance

# create a file to store the key locally
outfile = open('ec2-keypair.pem', 'w')
# call the boto ec2 function to create a key pair
key_pair = ec2.create_key_pair(KeyName='ec2-keypair')
# capture the key and store it in a file
KeyPairOut = str(key_pair.key_material)
outfile.write(KeyPairOut)

# Create a linux instance in the subnet
instances = ec2.create_instances(
 ImageId='ami-0de53d8956e8dcf80',
 InstanceType='t2.micro',
 MaxCount=1,
 MinCount=1,
 NetworkInterfaces=[{
 'SubnetId': subnet.id,
 'DeviceIndex': 0,
 'AssociatePublicIpAddress': True,
 'Groups': [securitygroup.group_id]
 }],
 KeyName='ec2-keypair')