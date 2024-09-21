import subprocess as _subprocess
import json

class _vpc:
    def __init__(self, region: str = None, aws_access_key: str = None, aws_access_secret_key: str = None):
        self.region_name = region
        self._access_key = aws_access_key
        self._secret_key = aws_access_secret_key

    def _run_aws_command(self, cmd: list) -> dict:
        # Set environment variables for AWS credentials if provided
        env = None
        if self._access_key and self._secret_key:
            env = {
                "AWS_ACCESS_KEY_ID": self._access_key,
                "AWS_SECRET_ACCESS_KEY": self._secret_key
            }

        process = _subprocess.Popen(cmd, stdout=_subprocess.PIPE, stderr=_subprocess.PIPE, text=True, env=env)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            return {"Error": stderr}

        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            return {"Error": "Failed to parse JSON output"}

    def _describe_route_table(self, route_table_id: str) -> dict:
        cmd = [
            "aws", "ec2", "describe-route-tables",
            "--route-table-ids", route_table_id,
            "--region", self.region_name
        ]
        return self._run_aws_command(cmd)

    def _create_route_table(self, vpc_id: str, route_table_name: str = "constellation-route-table") -> dict:
        cmd = [
            "aws", "ec2", "create-route-table",
            "--vpc-id", vpc_id,
            "--region", self.region_name
        ]

        route_table_creation_result = self._run_aws_command(cmd)

        if "Error" in route_table_creation_result:
            return route_table_creation_result

        route_table_id = route_table_creation_result.get('RouteTable', {}).get('RouteTableId')
        if not route_table_id:
            return {"Error": "Route Table ID not found in creation response"}

        tag_result = self._run_aws_command([
            "aws", "ec2", "create-tags",
            "--resources", route_table_id,
            "--tags", f"Key=Name,Value={route_table_name}",
            "--region", self.region_name
        ])

        if "Error" in tag_result:
            return tag_result

        return {"RouteTableId": route_table_id, "RouteTableName": route_table_name, "TagResult": tag_result}

    def _delete_route_table(self, route_table_id: str) -> dict:
        cmd = [
            "aws", "ec2", "delete-route-table",
            "--route-table-id", route_table_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _associate_route_table(self, route_table_id: str, subnet_id: str) -> dict:
        cmd = [
            "aws", "ec2", "associate-route-table",
            "--route-table-id", route_table_id,
            "--subnet-id", subnet_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _disassociate_route_table(self, association_id: str) -> dict:
        cmd = [
            "aws", "ec2", "disassociate-route-table",
            "--association-id", association_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _replace_route_table_association(self, association_id: str, route_table_id: str) -> dict:
        cmd = [
            "aws", "ec2", "replace-route-table-association",
            "--association-id", association_id,
            "--route-table-id", route_table_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _create_route(self, route_table_id: str, destination_cidr_block: str, gateway_id: str = None, nat_gateway_id: str = None) -> dict:
        cmd = [
            "aws", "ec2", "create-route",
            "--route-table-id", route_table_id,
            "--destination-cidr-block", destination_cidr_block,
            "--region", self.region_name
        ]

        if gateway_id:
            cmd.extend(["--gateway-id", gateway_id])

        if nat_gateway_id:
            cmd.extend(["--nat-gateway-id", nat_gateway_id])

        return self._run_aws_command(cmd)

    def _delete_route(self, route_table_id: str, destination_cidr_block: str) -> dict:
        cmd = [
            "aws", "ec2", "delete-route",
            "--route-table-id", route_table_id,
            "--destination-cidr-block", destination_cidr_block,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _describe_route_tables(self, vpc_id: str) -> dict:
        cmd = [
            "aws", "ec2", "describe-route-tables",
            "--filters", f"Name=vpc-id,Values={vpc_id}",
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _describe_subnet(self, subnet_id: str) -> dict:
        cmd = [
            "aws", "ec2", "describe-subnets",
            "--subnet-ids", subnet_id,
            "--region", self.region_name
        ]
        return self._run_aws_command(cmd)

    def _describe_subnets(self, vpc_id: str) -> dict:
        cmd = [
            "aws", "ec2", "describe-subnets",
            "--filters", f"Name=vpc-id,Values={vpc_id}",
            "--region", self.region_name
        ]
        return self._run_aws_command(cmd)

    def _create_subnet(self, vpc_id: str, cidr_block: str, availability_zone: str = None, subnet_name: str = "constellation-subnet") -> dict:
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

        subnet_id = subnet_creation_result.get('Subnet', {}).get('SubnetId')
        if not subnet_id:
            return {"Error": "Subnet ID not found in creation response"}

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

    def _create_default_vpc(self, subnet_name: str = "constellation-subnet") -> dict:
        cmd = [
            "aws", "ec2", "create-default-vpc",
            "--region", self.region_name
        ]
        vpc_creation_result = self._run_aws_command(cmd)

        if "Error" in vpc_creation_result:
            return vpc_creation_result

        vpc_id = vpc_creation_result.get('Vpc', {}).get('VpcId')
        if not vpc_id:
            return {"Error": "VPC ID not found in creation response"}

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

        tag_result = self._run_aws_command([
            "aws", "ec2", "create-tags",
            "--resources", subnet_id,
            "--tags", f"Key=Name,Value={subnet_name}",
            "--region", self.region_name
        ])

        if "Error" in tag_result:
            return tag_result

        return {"VpcId": vpc_id, "SubnetId": subnet_id, "SubnetName": subnet_name, "TagResult": tag_result}

    def _describe_vpc(self, vpc_id: str) -> dict:
        cmd = [
            "aws", "ec2", "describe-vpcs",
            "--vpc-ids", vpc_id,
            "--region", self.region_name
        ]
        return self._run_aws_command(cmd)

    def _create_vpc(self, cidr_block: str, vpc_name: str = "constellation-vpc") -> dict:
        cmd = [
            "aws", "ec2", "create-vpc",
            "--cidr-block", cidr_block,
            "--region", self.region_name
        ]

        vpc_creation_result = self._run_aws_command(cmd)

        if "Error" in vpc_creation_result:
            return vpc_creation_result

        vpc_id = vpc_creation_result.get('Vpc', {}).get('VpcId')
        if not vpc_id:
            return {"Error": "VPC ID not found in creation response"}

        tag_result = self._run_aws_command([
            "aws", "ec2", "create-tags",
            "--resources", vpc_id,
            "--tags", f"Key=Name,Value={vpc_name}",
            "--region", self.region_name
        ])

        if "Error" in tag_result:
            return tag_result

        return {"VpcId": vpc_id, "VpcName": vpc_name, "TagResult": tag_result}

    def _delete_vpc(self, vpc_id: str) -> dict:
        cmd = [
            "aws", "ec2", "delete-vpc",
            "--vpc-id", vpc_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _modify_vpc_attribute(self, vpc_id: str, attribute_name: str, attribute_value) -> dict:
        cmd = [
            "aws", "ec2", "modify-vpc-attribute",
            "--vpc-id", vpc_id,
            f"--{attribute_name}", str(attribute_value).lower(),
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _associate_vpc_cidr_block(self, vpc_id: str, cidr_block: str) -> dict:
        cmd = [
            "aws", "ec2", "associate-vpc-cidr-block",
            "--vpc-id", vpc_id,
            "--cidr-block", cidr_block,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _disassociate_vpc_cidr_block(self, association_id: str) -> dict:
        cmd = [
            "aws", "ec2", "disassociate-vpc-cidr-block",
            "--association-id", association_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _describe_vpc_cidr_reservations(self, vpc_id: str) -> dict:
        cmd = [
            "aws", "ec2", "describe-vpc-cidr-block-associations",
            "--vpc-id", vpc_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    @property
    def region(self) -> str:
        if self.region_name:
            return self.region_name
