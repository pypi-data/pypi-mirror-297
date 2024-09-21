from ._vpc import _vpc
from .errors import ErrorHandler
from .routing_table import RoutingTable

class Subnet(_vpc):
    def __init__(self, region: str, subnet_id: str = None, aws_access_key: str = None,
                 aws_access_secret_key: str = None, vpc_id: str = None,
                 cidr_block: str = None, availability_zone: str = None):
        self._subnet_id = subnet_id
        self._region = region
        self._aws_access_key = aws_access_key
        self._aws_access_secret_key = aws_access_secret_key
        self._vpc_id = vpc_id
        self._cidr_block = cidr_block
        self._availability_zone = availability_zone
        self._error_handler = ErrorHandler()

        super().__init__(region=region, aws_access_key=self._aws_access_key, aws_access_secret_key=self._aws_access_secret_key)
        del self._aws_access_key, self._aws_access_secret_key
        self._initialize_subnet()

    def _initialize_subnet(self):
        if self._subnet_id is not None:
            subnet = super()._describe_subnet(self._subnet_id)
            self._availability_zone = subnet.get('AvailabilityZone')
            self._availability_zone_id = subnet.get('AvailabilityZoneId')
            self._available_ip_address_count = subnet.get('AvailableIpAddressCount')
            self._cidr_block = subnet.get('CidrBlock')
            self._default_for_az = subnet.get('DefaultForAz')
            self._map_public_ip_on_launch = subnet.get('MapPublicIpOnLaunch')
            self._map_customer_owned_ip_on_launch = subnet.get('MapCustomerOwnedIpOnLaunch')
            self._state = subnet.get('State')
            self._subnet_id = subnet.get('SubnetId')
            self._vpc_id = subnet.get('VpcId')
            self._owner_id = subnet.get('OwnerId')
            self._assign_ipv6_address_on_creation = subnet.get('AssignIpv6AddressOnCreation')
            self._ipv6_cidr_block_association_set = subnet.get('Ipv6CidrBlockAssociationSet')
            self._subnet_arn = subnet.get('SubnetArn')
            self._enable_dns64 = subnet.get('EnableDns64')
            self._ipv6_native = subnet.get('Ipv6Native')
            self._private_dns_name_options_on_launch = subnet.get('PrivateDnsNameOptionsOnLaunch')
        elif self._vpc_id is not None and self._cidr_block is not None and self._availability_zone is not None:
            x = super()._create_subnet(self._vpc_id, self._cidr_block, self._availability_zone)
            if "Error" in x:
                self._error_handler.parse_and_raise(x)
            else:
                self._subnet_id = x["SubnetId"]
                self._cidr_block = x["CidrBlock"]
                self._availability_zone = x["Subnet"]["AvailabilityZone"]
                self._initialize_subnet()

    def describe_route_tables(self):
        # get all route tables attached to the vpc and return each as a rt.RoutingTable

    def create_subnet(self, vpc_id: str, cidr_block: str, availability_zone: str):
        x = super()._create_subnet(vpc_id, cidr_block, availability_zone)
        if "Error" in x:
            self._error_handler.parse_and_raise(x)
        else:
            return Subnet(
                region=self._region,
                subnet_id=x["SubnetId"],
                aws_access_key=self._aws_access_key,
                aws_access_secret_key=self._aws_access_secret_key,
            )

    def delete_subnet(self, subnet_id: str = None) -> dict:
        if subnet_id is not None:
            return super()._delete_subnet(subnet_id)
        else:
            result = super()._delete_subnet(self._subnet_id)
            self.__del__()
            return result

    def disassociate_cidr_block(self, association_id: str) -> dict:
        result = super()._disassociate_subnet_cidr_block(association_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def get_cidr_reservations(self) -> dict:
        result = super()._get_subnet_cidr_reservations(self._subnet_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def modify_subnet_attribute(self, attribute_name: str, attribute_value) -> dict:
        result = super()._modify_subnet_attribute(self._subnet_id, attribute_name, attribute_value)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def __del__(self):
        # This function is invoked when the instance is about to be destroyed.
        # It helps in cleaning up any resources if necessary.
        for attr in list(self.__dict__.keys()):
            delattr(self, attr)

    @property
    def availability_zone(self):
        return self._availability_zone

    @property
    def availability_zone_id(self):
        return self._availability_zone_id

    @property
    def available_ip_address_count(self):
        return self._available_ip_address_count

    @property
    def cidr_block(self):
        return self._cidr_block

    @property
    def default_for_az(self):
        return self._default_for_az

    @property
    def map_public_ip_on_launch(self):
        return self._map_public_ip_on_launch

    @property
    def map_customer_owned_ip_on_launch(self):
        return self._map_customer_owned_ip_on_launch

    @property
    def state(self):
        return self._state

    @property
    def subnet_id(self):
        return self._subnet_id

    @property
    def vpc_id(self):
        return self._vpc_id

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def assign_ipv6_address_on_creation(self):
        return self._assign_ipv6_address_on_creation

    @property
    def ipv6_cidr_block_association_set(self):
        return self._ipv6_cidr_block_association_set

    @property
    def ipv6_native(self):
        return self._ipv6_native

    @property
    def private_dns_name_options_on_launch(self):
        return self._private_dns_name_options_on_launch
