class NotEqualMatrixError(Exception):
    "Raised when input matrix is not NxN"
    pass

class NotInRegionError(Exception):
    "Raised subregion is not in region"
    pass

class InvalidPercentRange(Exception):
    "Raised when inputting percent decimal over 0-1"
    pass