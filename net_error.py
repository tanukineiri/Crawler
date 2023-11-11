from enum import Enum

class Net_Error(Enum):
    # Common
    COMMON_URLOPEN_ERROR = "errno"
    CONNECTION_REFUSED = "connection refused"

    # <urlopen error [Errno 8] nodename nor servname provided, or not known>
    NO_SERVNAME_PROVIDED = "nodename nor servname provided"

    # '[SSL: TLSV1_UNRECOGNIZED_NAME] tlsv1 unrecognized name (_ssl.c:1000)'
    UNRECOGNIZED_NAME = "unrecognized name"