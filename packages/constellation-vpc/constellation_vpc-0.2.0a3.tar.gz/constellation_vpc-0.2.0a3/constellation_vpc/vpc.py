from .subnet import Subnet
from ._vpc import _vpc
from .errors import ErrorHandler
from .routing_table import RoutingTable

class VPC(_vpc):
    def __init__(self, region: str, vpc_id: str = None, aws_access_key: str = None, aws_access_secret_key: str = None,
                 vpc_cidr_block: str = None):
        self._vpc_id = vpc_id
        self._region = region
        self._aws_access_key = aws_access_key
        self._aws_access_secret_key = aws_access_secret_key
        self._vpc_cidr_block = vpc_cidr_block
        self._error_handler = ErrorHandler()

        super().__init__(region=region, aws_access_key=self._aws_access_key,
                         aws_access_secret_key=self._aws_access_secret_key)
        del self._aws_access_key, self._aws_access_secret_key
        self._initialize_vpc()

    def _initialize_vpc(self):
        if self._vpc_id is not None:
            vpc_data = super()._describe_vpc(self._vpc_id)
            if "Error" in vpc_data:
                print(vpc_data["Error"])
                self._error_handler.parse_and_raise(vpc_data)
            vpc_info = vpc_data.get('Vpcs', [])[0]  # Get the first VPC entry from the result

            self._cidr_block = vpc_info.get('CidrBlock')
            self._cidr_block_association_set = vpc_info.get('CidrBlockAssociationSet', [])
            self._dhcp_options_id = vpc_info.get('DhcpOptionsId')
            self._instance_tenancy = vpc_info.get('InstanceTenancy')
            self._is_default = vpc_info.get('IsDefault')
            self._state = vpc_info.get('State')
            self._owner_id = vpc_info.get('OwnerId')
            self._tags = vpc_info.get('Tags', [])
        elif self._vpc_cidr_block is not None:
            vpc_data = super()._create_vpc(self._vpc_cidr_block)
            if "Error" in vpc_data:
                self._error_handler.parse_and_raise(vpc_data)
            self._vpc_id = vpc_data.get('Vpc', {}).get('VpcId')
            self._initialize_vpc()

    def create_vpc(self, cidr_block: str) -> dict:
        vpc = super()._create_vpc(cidr_block)
        if "Error" in vpc:
            self._error_handler.parse_and_raise(vpc)
        self._vpc_id = vpc.get('Vpc', {}).get('VpcId')
        return vpc

    def delete_vpc(self, vpc_id: str = None) -> dict:
        vpc_id = vpc_id or self._vpc_id
        result = super()._delete_vpc(vpc_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def associate_cidr_block(self, cidr_block: str) -> dict:
        result = super()._associate_vpc_cidr_block(self._vpc_id, cidr_block)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def disassociate_cidr_block(self, association_id: str) -> dict:
        result = super()._disassociate_vpc_cidr_block(association_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def describe_cidr_reservations(self) -> dict:
        result = super()._describe_vpc_cidr_reservations(self._vpc_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def modify_attribute(self, attribute_name: str, attribute_value) -> dict:
        result = super()._modify_vpc_attribute(self._vpc_id, attribute_name, attribute_value)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def describe_vpc(self, vpc_id: str = None) -> dict:
        vpc_id = vpc_id or self._vpc_id
        result = super()._describe_vpc(vpc_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def _get_subnets(self):
        """
        Fetches all subnets associated with this VPC and returns a list of initialized Subnet objects.
        """
        result = super()._describe_subnets(self._vpc_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)

        subnets = result.get('Subnets', [])
        self._subnets = []

        for subnet_info in subnets:
            subnet = Subnet(
                region=self._region,
                subnet_id=subnet_info.get('SubnetId'),
                aws_access_key=self._access_key,
                aws_access_secret_key=self._secret_key,
                vpc_id=self._vpc_id
            )
            self._subnets.append(subnet)

        return self._subnets

    def _get_routing_tables(self):
        """
        Fetches all routing tables associated with this VPC and returns a list of initialized RoutingTable objects.
        """
        result = super()._describe_route_tables(self._vpc_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)

        routing_tables = result.get('RouteTables', [])
        self._routing_tables = []
        for rt_info in routing_tables:
            routing_table = RoutingTable(
                region=self._region,
                route_table_id=rt_info.get('RouteTableId'),
                aws_access_key=self._aws_access_key,
                aws_access_secret_key=self._aws_access_secret_key,
                vpc_id=self._vpc_id
            )
            self._routing_tables.append(routing_table)

        return self._routing_tables

    @property
    def cidr_block(self):
        return self._cidr_block

    @property
    def cidr_block_association_set(self):
        return self._cidr_block_association_set

    @property
    def dhcp_options_id(self):
        return self._dhcp_options_id

    @property
    def instance_tenancy(self):
        return self._instance_tenancy

    @property
    def is_default(self):
        return self._is_default

    @property
    def state(self):
        return self._state

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def tags(self):
        return self._tags

    @property
    def vpc_id(self):
        return self._vpc_id

    @property
    def subnets(self):
        return self._get_subnets()

    @property
    def routing_tables(self):
        return self._routing_tables



    def __del__(self):
        # Cleanup resources if needed
        for attr in list(self.__dict__.keys()):
            delattr(self, attr)


if __name__ == '__main__':
    vpc = VPC('us-west-2', vpc_id="vpc-017f9600d16474436")
    subnets = vpc.subnets
