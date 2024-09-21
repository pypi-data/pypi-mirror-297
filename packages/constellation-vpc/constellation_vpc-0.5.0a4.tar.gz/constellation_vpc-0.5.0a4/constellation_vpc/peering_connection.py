from ._vpc import _vpc
from .errors import ErrorHandler

class PeeringConnection(_vpc):
    def __init__(self, region: str, peering_connection_id: str = None, aws_access_key: str = None, aws_access_secret_key: str = None):
        self._peering_connection_id = peering_connection_id
        self._region = region
        self._aws_access_key = aws_access_key
        self._aws_access_secret_key = aws_access_secret_key
        self._error_handler = ErrorHandler()

        super().__init__(region=region, aws_access_key=self._aws_access_key, aws_access_secret_key=self._aws_access_secret_key)
        del self._aws_access_key, self._aws_access_secret_key

    def create_peering_connection(self, vpc_id: str, peer_vpc_id: str, peer_region: str = None, peer_owner_id: str = None, peering_name: str = "constellation-peering-connection") -> dict:
        result = super()._create_vpc_peering_connection(vpc_id, peer_vpc_id, peer_region, peer_owner_id, peering_name)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        self._peering_connection_id = result.get('VpcPeeringConnectionId')
        return result

    def accept_peering_connection(self) -> dict:
        if not self._peering_connection_id:
            return {"Error": "VPC Peering Connection ID is required to accept the connection"}

        result = super()._accept_vpc_peering_connection(self._peering_connection_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def delete_peering_connection(self) -> dict:
        if not self._peering_connection_id:
            return {"Error": "VPC Peering Connection ID is required to delete the connection"}

        result = super()._delete_vpc_peering_connection(self._peering_connection_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def describe_peering_connections(self, vpc_id: str = None, peer_vpc_id: str = None) -> dict:
        vpc_id = vpc_id or self._vpc_id  # Use self._vpc_id if vpc_id is None
        peer_vpc_id = peer_vpc_id or self._peer_vpc_id  # Use self._peer_vpc_id if peer_vpc_id is None

        result = super()._describe_vpc_peering_connections(peering_connection_id=self._peering_connection_id, vpc_id=vpc_id, peer_vpc_id=peer_vpc_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def reject_peering_connection(self) -> dict:
        if not self._peering_connection_id:
            return {"Error": "VPC Peering Connection ID is required to reject the connection"}

        result = super()._reject_vpc_peering_connection(self._peering_connection_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    def describe_peering_connection_requests(self, vpc_id: str = None) -> dict:
        vpc_id = vpc_id or self._vpc_id  # Use self._vpc_id if vpc_id is None
        result = super()._describe_vpc_peering_connection_requests(vpc_id)
        if "Error" in result:
            self._error_handler.parse_and_raise(result)
        return result

    @property
    def peering_connection_id(self):
        return self._peering_connection_id
