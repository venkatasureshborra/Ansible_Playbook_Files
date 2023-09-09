provider "aws" {
region = "ap-south-1"
}
resources "aws_instance" "server_machines"{
ami = "ami-02bb7d8191b50f4bb"
instance_type= "t2.micro"
count=3
key_name= "testing"
security_groups=["terraform-20230828100409557200000001"]
tags={
Name= "hostmachines"
}
}
