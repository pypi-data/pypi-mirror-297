import subprocess as _subprocess
import json


class _vpc:
    def __init__(self, region: str = None, aws_access_key: str = None, aws_access_secret_key: str = None,
                 aws_sts_session_token: str = None):
        self.region_name = region
        self._access_key = aws_access_key
        self._secret_key = aws_access_secret_key
        self._session_token = aws_sts_session_token

    def _run_aws_command(self, cmd: list) -> dict:
        if self._access_key and self._secret_key:
            cmd.extend(["--aws-access-key-id", self._access_key])
            cmd.extend(["--aws-secret-access-key", self._secret_key])

        if self._session_token:
            cmd.extend(["--aws-session-token", self._session_token])

        process = _subprocess.Popen(cmd, stdout=_subprocess.PIPE, stderr=_subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return {"Error": stderr}

        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return {"Error": "Failed to parse JSON output"}

    def _describe_subnet(self, subnet_id: str) -> dict:
        cmd = [
            "aws", "ec2", "describe-subnets",
            "--subnet-ids", subnet_id,
            "--region", self.region_name
        ]
        data = self._run_aws_command(cmd)

        if "Error" in data:
            return data

        try:
            subnet_info = data['Subnets'][0]
            return {
                "AvailabilityZone": subnet_info.get("AvailabilityZone"),
                "AvailabilityZoneId": subnet_info.get("AvailabilityZoneId"),
                "AvailableIpAddressCount": subnet_info.get("AvailableIpAddressCount"),
                "CidrBlock": subnet_info.get("CidrBlock"),
                "DefaultForAz": subnet_info.get("DefaultForAz"),
                "MapPublicIpOnLaunch": subnet_info.get("MapPublicIpOnLaunch"),
                "MapCustomerOwnedIpOnLaunch": subnet_info.get("MapCustomerOwnedIpOnLaunch"),
                "State": subnet_info.get("State"),
                "SubnetId": subnet_info.get("SubnetId"),
                "VpcId": subnet_info.get("VpcId"),
                "OwnerId": subnet_info.get("OwnerId"),
                "AssignIpv6AddressOnCreation": subnet_info.get("AssignIpv6AddressOnCreation"),
                "Ipv6CidrBlockAssociationSet": subnet_info.get("Ipv6CidrBlockAssociationSet"),
                "SubnetArn": subnet_info.get("SubnetArn"),
                "EnableDns64": subnet_info.get("EnableDns64"),
                "Ipv6Native": subnet_info.get("Ipv6Native"),
                "PrivateDnsNameOptionsOnLaunch": subnet_info.get("PrivateDnsNameOptionsOnLaunch")
            }
        except (KeyError, IndexError):
            return {"Error": "Unexpected response structure"}

    def _create_subnet(self, vpc_id: str, cidr_block: str, availability_zone: str = None, subnet_name: str = "constallation-subnet") -> dict:
        cmd = [
            "aws", "ec2", "create-subnet",
            "--vpc-id", vpc_id,
            "--cidr-block", cidr_block,
            "--region", self.region_name
        ]

        if availability_zone:
            cmd.extend(["--availability-zone", availability_zone])

        subnet_creation_result = self._run_aws_command(cmd)

        if "Error" in subnet_creation_result:
            return subnet_creation_result

        # Extract Subnet ID from the creation result
        subnet_id = subnet_creation_result.get('Subnet', {}).get('SubnetId')
        if not subnet_id:
            return {"Error": "Subnet ID not found in creation response"}

        # Add the Name tag to the subnet
        tag_result = self._run_aws_command([
            "aws", "ec2", "create-tags",
            "--resources", subnet_id,
            "--tags", f"Key=Name,Value={subnet_name}",
            "--region", self.region_name
        ])

        if "Error" in tag_result:
            return tag_result

        return {"SubnetId": subnet_id, "SubnetName": subnet_name, "TagResult": tag_result}

    def _delete_subnet(self, subnet_id: str) -> dict:
        cmd = [
            "aws", "ec2", "delete-subnet",
            "--subnet-id", subnet_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _associate_subnet_cidr_block(self, subnet_id: str, cidr_block: str) -> dict:
        cmd = [
            "aws", "ec2", "associate-subnet-cidr-block",
            "--subnet-id", subnet_id,
            "--cidr-block", cidr_block,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _disassociate_subnet_cidr_block(self, association_id: str) -> dict:
        cmd = [
            "aws", "ec2", "disassociate-subnet-cidr-block",
            "--association-id", association_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _get_subnet_cidr_reservations(self, subnet_id: str) -> dict:
        cmd = [
            "aws", "ec2", "get-subnet-cidr-reservations",
            "--subnet-id", subnet_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _modify_subnet_attribute(self, subnet_id: str, attribute_name: str, attribute_value) -> dict:
        cmd = [
            "aws", "ec2", "modify-subnet-attribute",
            "--subnet-id", subnet_id,
            f"--{attribute_name}", str(attribute_value).lower(),
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _create_default_vpc(self, subnet_name: str = "constallation-subnet") -> dict:
        cmd = [
            "aws", "ec2", "create-default-vpc",
            "--region", self.region_name
        ]
        vpc_creation_result = self._run_aws_command(cmd)

        if "Error" in vpc_creation_result:
            return vpc_creation_result

        # Extract VPC ID from the creation result
        vpc_id = vpc_creation_result.get('Vpc', {}).get('VpcId')
        if not vpc_id:
            return {"Error": "VPC ID not found in creation response"}

        # Describe the subnets to find the newly created subnet
        subnets = self._run_aws_command([
            "aws", "ec2", "describe-subnets",
            "--filters", f"Name=vpc-id,Values={vpc_id}",
            "--region", self.region_name
        ])
        if "Error" in subnets:
            return subnets

        subnet_id = subnets.get('Subnets', [])[0].get('SubnetId')
        if not subnet_id:
            return {"Error": "Subnet ID not found"}

        # Add the Name tag to the subnet
        tag_result = self._run_aws_command([
            "aws", "ec2", "create-tags",
            "--resources", subnet_id,
            "--tags", f"Key=Name,Value={subnet_name}",
            "--region", self.region_name
        ])

        if "Error" in tag_result:
            return tag_result

        return {"VpcId": vpc_id, "SubnetId": subnet_id, "SubnetName": subnet_name, "TagResult": tag_result}

    @property
    def region(self) -> str:
        if self.region_name:
            return self.region_name
