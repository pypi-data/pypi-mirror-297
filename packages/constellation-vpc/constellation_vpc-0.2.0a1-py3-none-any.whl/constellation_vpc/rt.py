from _vpc import _vpc
from errors import ErrorHandler

class RoutingTable(_vpc):
    def __init__(self, region: str, route_table_id: str = None, vpc_id: str = None, aws_access_key: str = None,
                 aws_access_secret_key: str = None, aws_session_token: str = None):
        self._route_table_id = route_table_id
        self._vpc_id = vpc_id
        self._region = region
        self._aws_access_key = aws_access_key
        self._aws_access_secret_key = aws_access_secret_key
        self._aws_sts_token = aws_session_token
        self._error_handler = ErrorHandler()

        super().__init__(region=region, aws_access_key=self._aws_access_key,
                         aws_access_secret_key=self._aws_access_secret_key)
        del self._aws_sts_token, self._aws_access_key, self._aws_access_secret_key
        self._initialize_route_table()

    def _initialize_route_table(self):
        if self._route_table_id is not None:
            route_table = super()._describe_route_table(self._route_table_id)
            if "Error" in route_table:
                self._error_handler.parse_and_raise(route_table)
            self._vpc_id = route_table.get('RouteTables', [{}])[0].get('VpcId')
            self._routes = route_table.get('RouteTables', [{}])[0].get('Routes')
        elif self._vpc_id is not None:
            route_table = super()._create_route_table(self._vpc_id)
            if "Error" in route_table:
                self._error_handler.parse_and_raise(route_table)
            self._route_table_id = route_table.get('RouteTableId')
            self._initialize_route_table()

    def create_route_table(self, vpc_id: str) -> dict:
        route_table = super()._create_route_table(vpc_id)
        if "Error" in route_table:
            self._error_handler.parse_and_raise(route_table)
        self._route_table_id = route_table.get('RouteTableId')
        return route_table

    def delete_route_table(self, route_table_id: str = None) -> dict:
        route_table_id = route_table_id or self._route_table_id
        result = super()._delete_route_table(route_table_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def associate_route_table(self, subnet_id: str) -> dict:
        result = super()._associate_route_table(self._route_table_id, subnet_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def disassociate_route_table(self, association_id: str) -> dict:
        result = super()._disassociate_route_table(association_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def create_route(self, destination_cidr_block: str, gateway_id: str = None, nat_gateway_id: str = None) -> dict:
        result = super()._create_route(self._route_table_id, destination_cidr_block, gateway_id, nat_gateway_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def delete_route(self, destination_cidr_block: str) -> dict:
        result = super()._delete_route(self._route_table_id, destination_cidr_block)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def describe_route_table(self, route_table_id: str = None) -> dict:
        route_table_id = route_table_id or self._route_table_id
        result = super()._describe_route_table(route_table_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    @property
    def route_table_id(self):
        return self._route_table_id

    @property
    def vpc_id(self):
        return self._vpc_id

    @property
    def routes(self):
        return self._routes

    def __del__(self):
        # Cleanup resources if needed
        for attr in list(self.__dict__.keys()):
            delattr(self, attr)
