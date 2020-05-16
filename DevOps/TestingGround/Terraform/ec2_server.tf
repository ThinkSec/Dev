provider "aws" {
  profile    = "default"
  region     = "us-east-1"
}

locals {
  user_data = <<EOF
#!/bin/bash
echo "Hello Terraform!"
EOF
}

module "security-group" {
  source  = "terraform-aws-modules/security-group/aws"
  # insert the 2 required variables here
  name = "ManagementAccess"
  vpc_id = "vpc-025b2d2e8c784ecc6"

  ingress_cidr_blocks = ["0.0.0.0/32"]
  ingress_rules       = ["http-80-tcp", "all-icmp", "http-8080-tcp"]
  egress_rules        = ["all-all"]
}


module "ec2-instance" {
  source  = "terraform-aws-modules/ec2-instance/aws"
  # insert the 10 required variables here
  ami = "ami-b374d5a5"
  associate_public_ip_address = true
  instance_type = "t2.micro"
  name = "Jenkins2"
  subnet_id = "subnet-0c5f0f886e832ce12"
  user_data_base64 = base64encode(local.user_data)
  vpc_security_group_ids = [module.security-group.this_security_group_id]
}