from .errors import ClientNotFoundError
import subprocess as _subprocess
import json

class _vpc:
    def __init__(self, region: str = None, aws_access_key: str = None, aws_access_secret_key: str = None):
        self.region_name = region
        self._access_key = aws_access_key
        self._secret_key = aws_access_secret_key

    def _run_aws_command(self, cmd: list) -> dict:
        env = None
        if self._access_key and self._secret_key:
            env = {
                "AWS_ACCESS_KEY_ID": self._access_key,
                "AWS_SECRET_ACCESS_KEY": self._secret_key
            }
        try:
            process = _subprocess.Popen(cmd, stdout=_subprocess.PIPE, stderr=_subprocess.PIPE, text=True, env=env)
            stdout, stderr = process.communicate()
        except FileNotFoundError:
            raise ClientNotFoundError()
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

    def _create_internet_gateway(self, igw_name: str = "constellation-igw") -> dict:
        cmd = [
            "aws", "ec2", "create-internet-gateway",
            "--region", self.region_name
        ]

        igw_creation_result = self._run_aws_command(cmd)

        if "Error" in igw_creation_result:
            return igw_creation_result

        igw_id = igw_creation_result.get('InternetGateway', {}).get('InternetGatewayId')
        if not igw_id:
            return {"Error": "Internet Gateway ID not found in creation response"}

        tag_result = self._run_aws_command([
            "aws", "ec2", "create-tags",
            "--resources", igw_id,
            "--tags", f"Key=Name,Value={igw_name}",
            "--region", self.region_name
        ])

        if "Error" in tag_result:
            return tag_result

        return {"InternetGatewayId": igw_id, "InternetGatewayName": igw_name, "TagResult": tag_result}

    def _attach_internet_gateway(self, igw_id: str, vpc_id: str) -> dict:
        cmd = [
            "aws", "ec2", "attach-internet-gateway",
            "--internet-gateway-id", igw_id,
            "--vpc-id", vpc_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _detach_internet_gateway(self, igw_id: str, vpc_id: str) -> dict:
        cmd = [
            "aws", "ec2", "detach-internet-gateway",
            "--internet-gateway-id", igw_id,
            "--vpc-id", vpc_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _delete_internet_gateway(self, igw_id: str) -> dict:
        cmd = [
            "aws", "ec2", "delete-internet-gateway",
            "--internet-gateway-id", igw_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _describe_internet_gateways(self, vpc_id: str = None) -> dict:
        cmd = [
            "aws", "ec2", "describe-internet-gateways",
            "--region", self.region_name
        ]

        if vpc_id:
            cmd.extend(["--filters", f"Name=attachment.vpc-id,Values={vpc_id}"])

        return self._run_aws_command(cmd)

    def _create_nat_gateway(self, subnet_id: str, allocation_id: str, nat_gateway_name: str = "constellation-nat-gateway") -> dict:
        cmd = [
            "aws", "ec2", "create-nat-gateway",
            "--subnet-id", subnet_id,
            "--allocation-id", allocation_id,
            "--region", self.region_name
        ]

        nat_creation_result = self._run_aws_command(cmd)

        if "Error" in nat_creation_result:
            return nat_creation_result

        nat_gateway_id = nat_creation_result.get('NatGateway', {}).get('NatGatewayId')
        if not nat_gateway_id:
            return {"Error": "NAT Gateway ID not found in creation response"}

        tag_result = self._run_aws_command([
            "aws", "ec2", "create-tags",
            "--resources", nat_gateway_id,
            "--tags", f"Key=Name,Value={nat_gateway_name}",
            "--region", self.region_name
        ])

        if "Error" in tag_result:
            return tag_result

        return {"NatGatewayId": nat_gateway_id, "NatGatewayName": nat_gateway_name, "TagResult": tag_result}

    def _delete_nat_gateway(self, nat_gateway_id: str) -> dict:
        cmd = [
            "aws", "ec2", "delete-nat-gateway",
            "--nat-gateway-id", nat_gateway_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _describe_nat_gateways(self, vpc_id: str = None, subnet_id: str = None) -> dict:
        cmd = [
            "aws", "ec2", "describe-nat-gateways",
            "--region", self.region_name
        ]

        if vpc_id:
            cmd.extend(["--filter", f"Name=vpc-id,Values={vpc_id}"])
        if subnet_id:
            cmd.extend(["--filter", f"Name=subnet-id,Values={subnet_id}"])

        return self._run_aws_command(cmd)

    def _associate_nat_gateway(self, nat_gateway_id: str, route_table_id: str) -> dict:
        cmd = [
            "aws", "ec2", "create-route",
            "--route-table-id", route_table_id,
            "--nat-gateway-id", nat_gateway_id,
            "--destination-cidr-block", "0.0.0.0/0",
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _disassociate_nat_gateway(self, route_table_id: str) -> dict:
        cmd = [
            "aws", "ec2", "delete-route",
            "--route-table-id", route_table_id,
            "--destination-cidr-block", "0.0.0.0/0",
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _create_vpc_peering_connection(self, vpc_id: str, peer_vpc_id: str, peer_region: str = None,
                                       peer_owner_id: str = None,
                                       peering_name: str = "constellation-peering-connection") -> dict:
        cmd = [
            "aws", "ec2", "create-vpc-peering-connection",
            "--vpc-id", vpc_id,
            "--peer-vpc-id", peer_vpc_id,
            "--region", self.region_name
        ]

        if peer_region:
            cmd.extend(["--peer-region", peer_region])

        if peer_owner_id:
            cmd.extend(["--peer-owner-id", peer_owner_id])

        peering_creation_result = self._run_aws_command(cmd)

        if "Error" in peering_creation_result:
            return peering_creation_result

        peering_connection_id = peering_creation_result.get('VpcPeeringConnection', {}).get('VpcPeeringConnectionId')
        if not peering_connection_id:
            return {"Error": "VPC Peering Connection ID not found in creation response"}

        tag_result = self._run_aws_command([
            "aws", "ec2", "create-tags",
            "--resources", peering_connection_id,
            "--tags", f"Key=Name,Value={peering_name}",
            "--region", self.region_name
        ])

        if "Error" in tag_result:
            return tag_result

        return {"VpcPeeringConnectionId": peering_connection_id, "PeeringConnectionName": peering_name,
                "TagResult": tag_result}

    def _accept_vpc_peering_connection(self, peering_connection_id: str) -> dict:
        cmd = [
            "aws", "ec2", "accept-vpc-peering-connection",
            "--vpc-peering-connection-id", peering_connection_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _delete_vpc_peering_connection(self, peering_connection_id: str) -> dict:
        cmd = [
            "aws", "ec2", "delete-vpc-peering-connection",
            "--vpc-peering-connection-id", peering_connection_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _describe_vpc_peering_connections(self, peering_connection_id: str = None, vpc_id: str = None,
                                          peer_vpc_id: str = None) -> dict:
        cmd = [
            "aws", "ec2", "describe-vpc-peering-connections",
            "--region", self.region_name
        ]

        filters = []

        if peering_connection_id:
            filters.extend(["--vpc-peering-connection-ids", peering_connection_id])

        if vpc_id:
            filters.extend(["--filters", f"Name=requester-vpc-info.vpc-id,Values={vpc_id}"])

        if peer_vpc_id:
            filters.extend(["--filters", f"Name=accepter-vpc-info.vpc-id,Values={peer_vpc_id}"])

        cmd.extend(filters)

        return self._run_aws_command(cmd)

    def _reject_vpc_peering_connection(self, peering_connection_id: str) -> dict:
        cmd = [
            "aws", "ec2", "reject-vpc-peering-connection",
            "--vpc-peering-connection-id", peering_connection_id,
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    def _describe_vpc_peering_connection_requests(self, vpc_id: str = None) -> dict:
        cmd = [
            "aws", "ec2", "describe-vpc-peering-connections",
            "--filters", f"Name=requester-vpc-info.vpc-id,Values={vpc_id}",
            "--region", self.region_name
        ]

        return self._run_aws_command(cmd)

    @property
    def region(self) -> str:
        if self.region_name:
            return self.region_name