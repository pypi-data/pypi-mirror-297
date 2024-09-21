import re as _re

class SubnetError(Exception):
    def __init__(self, operation, message, *args):
        self.operation = operation
        self.message = message
        super().__init__(message, *args)

class SubnetCIDR_Conflicts(SubnetError):
    def __init__(self, operation, original_message, *args):
        cidr_match = _re.search(r"'(.*?)'", original_message)
        if (cidr_match := _re.search(r"'(.*?)'", original_message)):
            cidr = cidr_match.group(1)
            formatted_message = f"The CIDR {cidr} conflicts with another subnet"
        else:
            formatted_message = "The CIDR conflicts with another subnet"

        super().__init__(operation, formatted_message, *args)
        self.error_code = "InvalidSubnet.Conflict"

class SubnetCIDR_InvalidRange(SubnetError):
    def __init__(self, operation, original_message, *args):
        range_match = _re.search(r"'(.*?)'", original_message)
        if range_match:
            ip_range = range_match.group(1)
            formatted_message = f"The IP range {ip_range} is invalid or out of range"
        else:
            formatted_message = "The IP range is invalid or out of range"

        super().__init__(operation, formatted_message, *args)
        self.error_code = "InvalidSubnet.Range"

class ErrorHandler:
    def parse_and_raise(self, error):
        # Extract the error message
        error_message = error.get('Error', '')

        # Use _regex to extract the error code and operation from the error message
        code_match = _re.search(r'\((.*?)\)', error_message)
        operation_match = _re.search(r'when calling the (.*?) operation', error_message)

        if code_match and operation_match:
            error_code = code_match.group(1)
            operation = operation_match.group(1)

            # Raise the appropriate error based on the error code
            if error_code == "InvalidSubnet.Conflict":
                raise SubnetCIDRConflicts(operation, error_message)
            elif error_code == "InvalidSubnet.Range":
                raise SubnetRangeError(operation, error_message)
            else:
                raise SubnetError(operation, error_message)
        else:
            raise SubnetError("UnknownOperation", error_message)
