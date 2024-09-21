from _vpc import _vpc
from errors import ErrorHandler

class VPC(_vpc):
    def __init__(self, region: str, vpc_id: str = None, aws_access_key: str = None, aws_access_secret_key: str = None,
                 aws_session_token: str = None, vpc_cidr_block: str = None):
        self._vpc_id = vpc_id
        self._region = region
        self._aws_access_key = aws_access_key
        self._aws_access_secret_key = aws_access_secret_key
        self._aws_sts_token = aws_session_token
        self._vpc_cidr_block = vpc_cidr_block
        self._error_handler = ErrorHandler()

        super().__init__(region=region, aws_access_key=self._aws_access_key,
                         aws_access_secret_key=self._aws_access_secret_key, aws_sts_session_token=self._aws_sts_token)
        del self._aws_sts_token, self._aws_access_key, self._aws_access_secret_key
        self._initialize_vpc()

    def _initialize_vpc(self):
        if self._vpc_id is not None:
            vpc = super()._describe_vpc(self._vpc_id)
            if "Error" in vpc:
                self._error_handler.parse_and_raise(vpc)
            self._cidr_block = vpc.get('CidrBlock')
            self._is_default = vpc.get('IsDefault')
            self._state = vpc.get('State')
            self._owner_id = vpc.get('OwnerId')
        elif self._vpc_cidr_block is not None:
            vpc = super()._create_vpc(self._vpc_cidr_block)
            if "Error" in vpc:
                self._error_handler.parse_and_raise(vpc)
            self._vpc_id = vpc.get('VpcId')
            self._initialize_vpc()

    def create_vpc(self, cidr_block: str) -> dict:
        vpc = super()._create_vpc(cidr_block)
        if "Error" in vpc:
            self._error_handler.parse_and_raise(vpc)
        self._vpc_id = vpc.get('VpcId')
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

    @property
    def cidr_block(self):
        return self._cidr_block

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
    def vpc_id(self):
        return self._vpc_id

    def __del__(self):
        # Cleanup resources if needed
        for attr in list(self.__dict__.keys()):
            delattr(self, attr)


if __name__ == '__main__':
    vpc = VPC('us-west-2', vpc_id="vpc-017f9600d16474436")
    print(vpc.describe_vpc())
