import json
import opsCenter
import nodes

# This python script generates a CloudFormation template that deploys DSE across multiple regions.

with open('clusterParameters.json') as inputFile:
    clusterParameters = json.load(inputFile)

regions = clusterParameters['regions']
vmSize = clusterParameters['vmSize']
nodeCount = clusterParameters['nodeCount']

# This is the skeleton of the template that we're going to add resources to
generatedTemplate = {
    {
        "AWSTemplateFormatVersion": "2010-09-09",
        "Description": "Amazon CloudFormation template for DataStax Enterprise",
        "Parameters": {
            "InstanceType": {
                "Description": "EC2 instance type",
                "Type": "String",
                "Default": "t2.small",
                "AllowedValues": ["t1.micro", "t2.nano", "t2.micro", "t2.small", "t2.medium", "t2.large", "m1.small",
                                  "m1.medium", "m1.large", "m1.xlarge", "m2.xlarge", "m2.2xlarge", "m2.4xlarge",
                                  "m3.medium", "m3.large", "m3.xlarge", "m3.2xlarge", "m4.large", "m4.xlarge",
                                  "m4.2xlarge", "m4.4xlarge", "m4.10xlarge", "c1.medium", "c1.xlarge", "c3.large",
                                  "c3.xlarge", "c3.2xlarge", "c3.4xlarge", "c3.8xlarge", "c4.large", "c4.xlarge",
                                  "c4.2xlarge", "c4.4xlarge", "c4.8xlarge", "g2.2xlarge", "g2.8xlarge", "r3.large",
                                  "r3.xlarge", "r3.2xlarge", "r3.4xlarge", "r3.8xlarge", "i2.xlarge", "i2.2xlarge",
                                  "i2.4xlarge", "i2.8xlarge", "d2.xlarge", "d2.2xlarge", "d2.4xlarge", "d2.8xlarge",
                                  "hi1.4xlarge", "hs1.8xlarge", "cr1.8xlarge", "cc2.8xlarge", "cg1.4xlarge"]
                ,
                "ConstraintDescription": "must be a valid EC2 instance type."
            },

            "KeyName": {
                "Description": "Name of an existing EC2 KeyPair to enable SSH access to the instances",
                "Type": "AWS::EC2::KeyPair::KeyName",
                "ConstraintDescription": "must be the name of an existing EC2 KeyPair."
            },

            "SSHLocation": {
                "Description": "The IP address range that can be used to SSH to the EC2 instances",
                "Type": "String",
                "MinLength": "9",
                "MaxLength": "18",
                "Default": "0.0.0.0/0",
                "AllowedPattern": "(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})/(\\d{1,2})",
                "ConstraintDescription": "must be a valid IP CIDR range of the form x.x.x.x/x."
            }
        },

        "Mappings": {
            "AWSInstanceType2Arch": {
                "t1.micro": {"Arch": "PV64"},
                "t2.nano": {"Arch": "HVM64"},
                "t2.micro": {"Arch": "HVM64"},
                "t2.small": {"Arch": "HVM64"},
                "t2.medium": {"Arch": "HVM64"},
                "t2.large": {"Arch": "HVM64"},
                "m1.small": {"Arch": "PV64"},
                "m1.medium": {"Arch": "PV64"},
                "m1.large": {"Arch": "PV64"},
                "m1.xlarge": {"Arch": "PV64"},
                "m2.xlarge": {"Arch": "PV64"},
                "m2.2xlarge": {"Arch": "PV64"},
                "m2.4xlarge": {"Arch": "PV64"},
                "m3.medium": {"Arch": "HVM64"},
                "m3.large": {"Arch": "HVM64"},
                "m3.xlarge": {"Arch": "HVM64"},
                "m3.2xlarge": {"Arch": "HVM64"},
                "m4.large": {"Arch": "HVM64"},
                "m4.xlarge": {"Arch": "HVM64"},
                "m4.2xlarge": {"Arch": "HVM64"},
                "m4.4xlarge": {"Arch": "HVM64"},
                "m4.10xlarge": {"Arch": "HVM64"},
                "c1.medium": {"Arch": "PV64"},
                "c1.xlarge": {"Arch": "PV64"},
                "c3.large": {"Arch": "HVM64"},
                "c3.xlarge": {"Arch": "HVM64"},
                "c3.2xlarge": {"Arch": "HVM64"},
                "c3.4xlarge": {"Arch": "HVM64"},
                "c3.8xlarge": {"Arch": "HVM64"},
                "c4.large": {"Arch": "HVM64"},
                "c4.xlarge": {"Arch": "HVM64"},
                "c4.2xlarge": {"Arch": "HVM64"},
                "c4.4xlarge": {"Arch": "HVM64"},
                "c4.8xlarge": {"Arch": "HVM64"},
                "g2.2xlarge": {"Arch": "HVMG2"},
                "g2.8xlarge": {"Arch": "HVMG2"},
                "r3.large": {"Arch": "HVM64"},
                "r3.xlarge": {"Arch": "HVM64"},
                "r3.2xlarge": {"Arch": "HVM64"},
                "r3.4xlarge": {"Arch": "HVM64"},
                "r3.8xlarge": {"Arch": "HVM64"},
                "i2.xlarge": {"Arch": "HVM64"},
                "i2.2xlarge": {"Arch": "HVM64"},
                "i2.4xlarge": {"Arch": "HVM64"},
                "i2.8xlarge": {"Arch": "HVM64"},
                "d2.xlarge": {"Arch": "HVM64"},
                "d2.2xlarge": {"Arch": "HVM64"},
                "d2.4xlarge": {"Arch": "HVM64"},
                "d2.8xlarge": {"Arch": "HVM64"},
                "hi1.4xlarge": {"Arch": "HVM64"},
                "hs1.8xlarge": {"Arch": "HVM64"},
                "cr1.8xlarge": {"Arch": "HVM64"},
                "cc2.8xlarge": {"Arch": "HVM64"}
            },

            "AWSInstanceType2NATArch": {
                "t1.micro": {"Arch": "NATPV64"},
                "t2.nano": {"Arch": "NATHVM64"},
                "t2.micro": {"Arch": "NATHVM64"},
                "t2.small": {"Arch": "NATHVM64"},
                "t2.medium": {"Arch": "NATHVM64"},
                "t2.large": {"Arch": "NATHVM64"},
                "m1.small": {"Arch": "NATPV64"},
                "m1.medium": {"Arch": "NATPV64"},
                "m1.large": {"Arch": "NATPV64"},
                "m1.xlarge": {"Arch": "NATPV64"},
                "m2.xlarge": {"Arch": "NATPV64"},
                "m2.2xlarge": {"Arch": "NATPV64"},
                "m2.4xlarge": {"Arch": "NATPV64"},
                "m3.medium": {"Arch": "NATHVM64"},
                "m3.large": {"Arch": "NATHVM64"},
                "m3.xlarge": {"Arch": "NATHVM64"},
                "m3.2xlarge": {"Arch": "NATHVM64"},
                "m4.large": {"Arch": "NATHVM64"},
                "m4.xlarge": {"Arch": "NATHVM64"},
                "m4.2xlarge": {"Arch": "NATHVM64"},
                "m4.4xlarge": {"Arch": "NATHVM64"},
                "m4.10xlarge": {"Arch": "NATHVM64"},
                "c1.medium": {"Arch": "NATPV64"},
                "c1.xlarge": {"Arch": "NATPV64"},
                "c3.large": {"Arch": "NATHVM64"},
                "c3.xlarge": {"Arch": "NATHVM64"},
                "c3.2xlarge": {"Arch": "NATHVM64"},
                "c3.4xlarge": {"Arch": "NATHVM64"},
                "c3.8xlarge": {"Arch": "NATHVM64"},
                "c4.large": {"Arch": "NATHVM64"},
                "c4.xlarge": {"Arch": "NATHVM64"},
                "c4.2xlarge": {"Arch": "NATHVM64"},
                "c4.4xlarge": {"Arch": "NATHVM64"},
                "c4.8xlarge": {"Arch": "NATHVM64"},
                "g2.2xlarge": {"Arch": "NATHVMG2"},
                "g2.8xlarge": {"Arch": "NATHVMG2"},
                "r3.large": {"Arch": "NATHVM64"},
                "r3.xlarge": {"Arch": "NATHVM64"},
                "r3.2xlarge": {"Arch": "NATHVM64"},
                "r3.4xlarge": {"Arch": "NATHVM64"},
                "r3.8xlarge": {"Arch": "NATHVM64"},
                "i2.xlarge": {"Arch": "NATHVM64"},
                "i2.2xlarge": {"Arch": "NATHVM64"},
                "i2.4xlarge": {"Arch": "NATHVM64"},
                "i2.8xlarge": {"Arch": "NATHVM64"},
                "d2.xlarge": {"Arch": "NATHVM64"},
                "d2.2xlarge": {"Arch": "NATHVM64"},
                "d2.4xlarge": {"Arch": "NATHVM64"},
                "d2.8xlarge": {"Arch": "NATHVM64"},
                "hi1.4xlarge": {"Arch": "NATHVM64"},
                "hs1.8xlarge": {"Arch": "NATHVM64"},
                "cr1.8xlarge": {"Arch": "NATHVM64"},
                "cc2.8xlarge": {"Arch": "NATHVM64"}
            }
            ,
            "AWSRegionArch2AMI": {
                "us-east-1": {"PV64": "ami-8ff710e2", "HVM64": "ami-f5f41398", "HVMG2": "ami-4afd1d27"},
                "us-west-2": {"PV64": "ami-eff1028f", "HVM64": "ami-d0f506b0", "HVMG2": "ami-ee897b8e"},
                "us-west-1": {"PV64": "ami-ac85fbcc", "HVM64": "ami-6e84fa0e", "HVMG2": "ami-69106909"},
                "eu-west-1": {"PV64": "ami-23ab2250", "HVM64": "ami-b0ac25c3", "HVMG2": "ami-936de5e0"},
                "eu-central-1": {"PV64": "ami-27c12348", "HVM64": "ami-d3c022bc", "HVMG2": "ami-8e7092e1"},
                "ap-northeast-1": {"PV64": "ami-26160d48", "HVM64": "ami-29160d47", "HVMG2": "ami-91809aff"},
                "ap-northeast-2": {"PV64": "NOT_SUPPORTED", "HVM64": "ami-cf32faa1", "HVMG2": "NOT_SUPPORTED"},
                "ap-southeast-1": {"PV64": "ami-f3dd0a90", "HVM64": "ami-1ddc0b7e", "HVMG2": "ami-3c30e75f"},
                "ap-southeast-2": {"PV64": "ami-8f94b9ec", "HVM64": "ami-0c95b86f", "HVMG2": "ami-543d1137"},
                "sa-east-1": {"PV64": "ami-e188018d", "HVM64": "ami-fb890097", "HVMG2": "NOT_SUPPORTED"},
                "cn-north-1": {"PV64": "ami-77a46e1a", "HVM64": "ami-05a66c68", "HVMG2": "NOT_SUPPORTED"}
            }

        },

        "Resources": {
            "EC2Instance": {
                "Type": "AWS::EC2::Instance",
                "Properties": {
                    "UserData": {"Fn::Base64": {"Fn::Join": ["", ["IPAddress=", {"Ref": "IPAddress"}]]}},
                    "InstanceType": {"Ref": "InstanceType"},
                    "SecurityGroups": [{"Ref": "InstanceSecurityGroup"}],
                    "KeyName": {"Ref": "KeyName"},
                    "ImageId": {"Fn::FindInMap": ["AWSRegionArch2AMI", {"Ref": "AWS::Region"},
                                                  {"Fn::FindInMap": ["AWSInstanceType2Arch", {"Ref": "InstanceType"},
                                                                     "Arch"]}]}
                }
            },

            "InstanceSecurityGroup": {
                "Type": "AWS::EC2::SecurityGroup",
                "Properties": {
                    "GroupDescription": "Enable SSH access",
                    "SecurityGroupIngress":
                        [{"IpProtocol": "tcp", "FromPort": "22", "ToPort": "22", "CidrIp": {"Ref": "SSHLocation"}}]
                }
            },

            "IPAddress": {
                "Type": "AWS::EC2::EIP"
            },

            "IPAssoc": {
                "Type": "AWS::EC2::EIPAssociation",
                "Properties": {
                    "InstanceId": {"Ref": "EC2Instance"},
                    "EIP": {"Ref": "IPAddress"}
                }
            }
        },
        "Outputs": {
            "InstanceId": {
                "Description": "InstanceId of the newly created EC2 instance",
                "Value": {"Ref": "EC2Instance"}
            },
            "InstanceIPAddress": {
                "Description": "IP address of the newly created EC2 instance",
                "Value": {"Ref": "IPAddress"}
            }
        }
    }
}

# Create DSE nodes in each location
for datacenterIndex in range(0, len(regions)):
    region = regions[datacenterIndex]
    resources = nodes.generate_template(region, datacenterIndex, vmSize, nodeCount, regions)
    # generatedTemplate['resources'] += resources

# Create the OpsCenter node
resources = opsCenter.generate_template(regions, nodeCount)
# generatedTemplate['resources'] += resources

with open('generatedTemplate.json', 'w') as outputFile:
    json.dump(generatedTemplate, outputFile, sort_keys=True, indent=4, ensure_ascii=False)
