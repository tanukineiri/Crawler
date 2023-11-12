from enum import Enum

class Net_Error(Enum):
    # Common
    COMMON_URLOPEN_ERROR = "errno"
    CONNECTION_REFUSED = "connection refused"

    # <urlopen error _ssl.c:983: The handshake operation timed out>
    OPERATION_TIMED_OUT = "operation timed out"

    # <urlopen error [Errno 8] nodename nor servname provided, or not known>
    NO_SERVNAME_PROVIDED = "nodename nor servname provided"

    # '[SSL: TLSV1_UNRECOGNIZED_NAME] tlsv1 unrecognized name (_ssl.c:1000)'
    UNRECOGNIZED_NAME = "unrecognized name"

    # ssl.SSLError: [SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error (_ssl.c:1000)
    INTERNAL_ERROR = "internal error"