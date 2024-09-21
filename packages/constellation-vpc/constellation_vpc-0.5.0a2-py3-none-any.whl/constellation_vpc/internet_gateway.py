
from ._vpc import _vpc
from .errors import ErrorHandler

class InternetGateway(_vpc):
    def __init__(self, region: str, igw_id: str = None, aws_access_key: str = None, aws_access_secret_key: str = None):
        self._igw_id = igw_id
        self._region = region
        self._aws_access_key = aws_access_key
        self._aws_access_secret_key = aws_access_secret_key
        self._error_handler = ErrorHandler()

        super().__init__(region=region, aws_access_key=self._aws_access_key, aws_access_secret_key=self._aws_access_secret_key)
        del self._aws_access_key, self._aws_access_secret_key

    def create_internet_gateway(self, igw_name: str = "constellation-igw") -> dict:
        igw_creation_result = super()._create_internet_gateway(igw_name)

        if "Error" in igw_creation_result:
            return igw_creation_result

        return igw_creation_result

    def attach_internet_gateway(self, vpc_id: str) -> dict:
        if not self._igw_id:
            return {"Error": "Internet Gateway ID is required to attach to VPC"}

        attach_result = super()._attach_internet_gateway(self._igw_id, vpc_id)

        if "Error" in attach_result:
            return attach_result

        return attach_result

    def detach_internet_gateway(self, vpc_id: str) -> dict:
        if not self._igw_id:
            return {"Error": "Internet Gateway ID is required to detach from VPC"}

        detach_result = super()._detach_internet_gateway(self._igw_id, vpc_id)

        if "Error" in detach_result:
            return detach_result

        return detach_result

    def delete_internet_gateway(self) -> dict:
        if not self._igw_id:
            return {"Error": "Internet Gateway ID is required to delete"}

        delete_result = super()._delete_internet_gateway(self._igw_id)

        if "Error" in delete_result:
            return delete_result

        return delete_result

    def describe_internet_gateways(self, vpc_id: str = None) -> dict:
        return super()._describe_internet_gateways(vpc_id)

