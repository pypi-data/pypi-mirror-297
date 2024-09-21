from ._vpc import _vpc
from .errors import ErrorHandler

class NatGateway(_vpc):
    def __init__(self, region: str, nat_gateway_id: str = None, aws_access_key: str = None, aws_access_secret_key: str = None):
        self._nat_gateway_id = nat_gateway_id
        self._region = region
        self._aws_access_key = aws_access_key
        self._aws_access_secret_key = aws_access_secret_key
        self._error_handler = ErrorHandler()

        super().__init__(region=region, aws_access_key=self._aws_access_key, aws_access_secret_key=self._aws_access_secret_key)
        del self._aws_access_key, self._aws_access_secret_key

    def create_nat_gateway(self, subnet_id: str, allocation_id: str, nat_gateway_name: str = "constellation-nat-gateway") -> dict:
        nat_creation_result = super()._create_nat_gateway(subnet_id, allocation_id, nat_gateway_name)

        if "Error" in nat_creation_result:
            self._error_handler.parse_and_raise(nat_creation_result)

        self._nat_gateway_id = nat_creation_result.get('NatGatewayId')
        return nat_creation_result

    def delete_nat_gateway(self) -> dict:
        if not self._nat_gateway_id:
            return {"Error": "NAT Gateway ID is required to delete"}

        delete_result = super()._delete_nat_gateway(self._nat_gateway_id)

        if "Error" in delete_result:
            self._error_handler.parse_and_raise(delete_result)

        return delete_result

    def describe_nat_gateways(self, vpc_id: str = None, subnet_id: str = None) -> dict:
        return super()._describe_nat_gateways(vpc_id, subnet_id)

    def associate_nat_gateway(self, route_table_id: str) -> dict:
        if not self._nat_gateway_id:
            return {"Error": "NAT Gateway ID is required to associate with route table"}

        associate_result = super()._associate_nat_gateway(self._nat_gateway_id, route_table_id)

        if "Error" in associate_result:
            self._error_handler.parse_and_raise(associate_result)

        return associate_result

    def disassociate_nat_gateway(self, route_table_id: str) -> dict:
        disassociate_result = super()._disassociate_nat_gateway(route_table_id)

        if "Error" in disassociate_result:
            self._error_handler.parse_and_raise(disassociate_result)

        return disassociate_result

    @property
    def nat_gateway_id(self):
        return self._nat_gateway_id
