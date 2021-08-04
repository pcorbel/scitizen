# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime
from functools import reduce
from typing import Any, Optional


def deep_get(dictionary: dict, path: str, default: Any = None) -> Any:
    """Safely parse a dict to return the value located at the given path.

    Args:
      dictionary:
        The dictionary to get the value from.
      path:
        The path of the value to fetch.
      default:
        The default value to return if no value is found.

    Returns:
      The value found in the dictionary path, or the default one if
      nothing is found.
    """

    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        path.split("."),
        dictionary,
    )


def md5(item: Any) -> str:
    """Compute the MD5 hash of an object.

    Args:
      item:
        The object to compute the MD5 hash on.

    Returns:
      The MD5 hash of the object.
    """

    return hashlib.md5(str(item).encode()).hexdigest()


def to_isoformat(item: str) -> str:
    """Compute the ISO formatted representation of a timestamp.

    Args:
      item:
        The timestamp to be formatted.

    Returns:
      The ISO formatted representation of the timestamp.
    """
    if item is not None:
        return datetime.fromtimestamp(float(item)).isoformat()


def get_active_task_state(code: int) -> Optional[str]:
    """Translate an active task state code to a human-readable state.

    Official mapping is available
    `here <https://github.com/BOINC/boinc/blob/master/py/Boinc/boinc_db.py>`.

    Args:
      code:
        The code of the activate task state.

    Returns:
      The human-readable state related to the code.
    """

    states = {
        0: "UNINITIALIZED",
        1: "EXECUTING",
        2: "EXITED",
        3: "SIGNALED",
        4: "EXIT_UNKNOWN",
        5: "ABORT_PENDING",
        6: "ABORTED",
        7: "COULDNT_START",
        8: "QUIT_PENDING",
        9: "SUSPENDED",
        10: "COPY_PENDING",
    }
    return states.get(int(code))


def get_scheduler_state(code: int) -> Optional[str]:
    """Translate an schduler state code to a human-readable state.

    Official mapping is available
    `here <https://github.com/BOINC/boinc/blob/master/py/Boinc/boinc_db.py>`.

    Args:
      code:
        The code of scheduler state.

    Returns:
      The human-readable state related to the code.
    """

    states = {
        0: "UNINITIALIZED",
        1: "PREEMPTED",
        2: "SCHEDULED",
    }
    return states.get(int(code))


def get_result_state(code: int) -> Optional[str]:
    """Translate an result state code to a human-readable state.

    Official mapping is available
    `here <https://github.com/BOINC/boinc/blob/master/py/Boinc/boinc_db.py>`.

    Args:
      code:
        The code of result state.

    Returns:
      The human-readable state related to the code.
    """

    states = {
        0: "NEW",
        1: "FILES_DOWNLOADING",
        2: "FILES_DOWNLOADED",
        3: "COMPUTE_ERROR",
        4: "FILES_UPLOADING",
        5: "FILES_UPLOADED",
        6: "ABORTED",
        7: "UPLOAD_FAILED",
    }
    return states.get(int(code))


def get_exit_statement(code: int) -> Optional[str]:
    """Translate an exit code to an human-readable statement.

    Official mapping is available
    `here <https://github.com/BOINC/boinc/blob/master/lib/error_numbers.h>`.

    Args:
      code:
        The exit code.

    Returns:
      The human-readable statement related to the code.
    """

    statements = {
        192: "EXIT_STATEFILE_WRITE",
        193: "EXIT_SIGNAL",
        194: "EXIT_ABORTED_BY_CLIENT",
        195: "EXIT_CHILD_FAILED",
        196: "EXIT_DISK_LIMIT_EXCEEDED",
        197: "EXIT_TIME_LIMIT_EXCEEDED",
        198: "EXIT_MEM_LIMIT_EXCEEDED",
        199: "EXIT_CLIENT_EXITING",
        200: "EXIT_UNSTARTED_LATE",
        201: "EXIT_MISSING_COPROC",
        202: "EXIT_ABORTED_BY_PROJECT",
        203: "EXIT_ABORTED_VIA_GUI",
        204: "EXIT_UNKNOWN",
        205: "EXIT_OUT_OF_MEMORY",
        206: "EXIT_INIT_FAILURE",
        207: "EXIT_NO_SUB_TASKS",
        208: "EXIT_SUB_TASK_FAILURE",
        -100: "ERR_SELECT",
        -102: "ERR_READ",
        -103: "ERR_WRITE",
        -104: "ERR_FREAD",
        -105: "ERR_FWRITE",
        -106: "ERR_IO",
        -107: "ERR_CONNECT",
        -108: "ERR_FOPEN",
        -109: "ERR_RENAME",
        -110: "ERR_UNLINK",
        -111: "ERR_OPENDIR",
        -112: "ERR_XML_PARSE",
        -113: "ERR_GETHOSTBYNAME",
        -114: "ERR_GIVEUP_DOWNLOAD",
        -115: "ERR_GIVEUP_UPLOAD",
        -116: "ERR_NULL",
        -117: "ERR_NEG",
        -118: "ERR_BUFFER_OVERFLOW",
        -119: "ERR_MD5_FAILED",
        -120: "ERR_RSA_FAILED",
        -121: "ERR_OPEN",
        -122: "ERR_DUP2",
        -123: "ERR_NO_SIGNATURE",
        -124: "ERR_THREAD",
        -125: "ERR_SIGNAL_CATCH",
        -126: "ERR_QUIT_REQUEST",
        -127: "ERR_UPLOAD_TRANSIENT",
        -128: "ERR_UPLOAD_PERMANENT",
        -129: "ERR_IDLE_PERIOD",
        -130: "ERR_ALREADY_ATTACHED",
        -131: "ERR_FILE_TOO_BIG",
        -132: "ERR_GETRUSAGE",
        -133: "ERR_BENCHMARK_FAILED",
        -134: "ERR_BAD_HEX_FORMAT",
        -135: "ERR_USER_REJECTED",
        -136: "ERR_DB_NOT_FOUND",
        -137: "ERR_DB_NOT_UNIQUE",
        -138: "ERR_DB_CANT_CONNECT",
        -139: "ERR_GETS",
        -140: "ERR_SCANF",
        -141: "ERR_STRCHR",
        -142: "ERR_STRSTR",
        -143: "ERR_READDIR",
        -144: "ERR_SHMGET",
        -145: "ERR_SHMCTL",
        -146: "ERR_SHMAT",
        -147: "ERR_FORK",
        -148: "ERR_EXEC",
        -149: "ERR_NOT_EXITED",
        -150: "ERR_NOT_IMPLEMENTED",
        -151: "ERR_GETHOSTNAME",
        -152: "ERR_NETOPEN",
        -153: "ERR_SOCKET",
        -154: "ERR_FCNTL",
        -155: "ERR_AUTHENTICATOR",
        -156: "ERR_SCHED_SHMEM",
        -157: "ERR_ASYNCSELECT",
        -158: "ERR_BAD_RESULT_STATE",
        -159: "ERR_DB_CANT_INIT",
        -160: "ERR_NOT_UNIQUE",
        -161: "ERR_NOT_FOUND",
        -162: "ERR_NO_EXIT_STATUS",
        -163: "ERR_FILE_MISSING",
        -164: "ERR_NESTED_UNHANDLED_EXCEPTION_DETECTED",
        -165: "ERR_SEMGET",
        -166: "ERR_SEMCTL",
        -167: "ERR_SEMOP",
        -168: "ERR_FTOK",
        -169: "ERR_SOCKS_UNKNOWN_FAILURE",
        -170: "ERR_SOCKS_REQUEST_FAILED",
        -171: "ERR_SOCKS_BAD_USER_PASS",
        -172: "ERR_SOCKS_UNKNOWN_SERVER_VERSION",
        -173: "ERR_SOCKS_UNSUPPORTED",
        -174: "ERR_SOCKS_CANT_REACH_HOST",
        -175: "ERR_SOCKS_CONN_REFUSED",
        -176: "ERR_TIMER_INIT",
        -177: "ERR_RSC_LIMIT_EXCEEDED",
        -178: "ERR_INVALID_PARAM",
        -179: "ERR_SIGNAL_OP",
        -180: "ERR_BIND",
        -181: "ERR_LISTEN",
        -182: "ERR_TIMEOUT",
        -183: "ERR_PROJECT_DOWN",
        -184: "ERR_HTTP_ERROR",
        -185: "ERR_RESULT_START",
        -186: "ERR_RESULT_DOWNLOAD",
        -187: "ERR_RESULT_UPLOAD",
        -189: "ERR_INVALID_URL",
        -190: "ERR_MAJOR_VERSION",
        -191: "ERR_NO_OPTION",
        -192: "ERR_MKDIR",
        -193: "ERR_INVALID_EVENT",
        -194: "ERR_ALREADY_RUNNING",
        -195: "ERR_NO_APP_VERSION",
        -196: "ERR_WU_USER_RULE",
        -197: "ERR_ABORTED_VIA_GUI",
        -198: "ERR_INSUFFICIENT_RESOURCE",
        -199: "ERR_RETRY",
        -200: "ERR_WRONG_SIZE",
        -201: "ERR_USER_PERMISSION",
        -202: "ERR_SHMEM_NAME",
        -203: "ERR_NO_NETWORK_CONNECTION",
        -204: "ERR_IN_PROGRESS",
        -205: "ERR_BAD_EMAIL_ADDR",
        -206: "ERR_BAD_PASSWD",
        -207: "ERR_NONUNIQUE_EMAIL",
        -208: "ERR_ACCT_CREATION_DISABLED",
        -209: "ERR_ATTACH_FAIL_INIT",
        -210: "ERR_ATTACH_FAIL_DOWNLOAD",
        -211: "ERR_ATTACH_FAIL_PARSE",
        -212: "ERR_ATTACH_FAIL_BAD_KEY",
        -213: "ERR_ATTACH_FAIL_FILE_WRITE",
        -214: "ERR_ATTACH_FAIL_SERVER_ERROR",
        -215: "ERR_SIGNING_KEY",
        -216: "ERR_FFLUSH",
        -217: "ERR_FSYNC",
        -218: "ERR_TRUNCATE",
        -219: "ERR_WRONG_URL",
        -220: "ERR_DUP_NAME",
        -221: "ERR_ABORTED_BY_PROJECT",
        -222: "ERR_GETGRNAM",
        -223: "ERR_CHOWN",
        -224: "ERR_FILE_NOT_FOUND",
        -225: "ERR_BAD_FILENAME",
        -226: "ERR_TOO_MANY_EXITS",
        -227: "ERR_RMDIR",
        -228: "ERR_CHILD_FAILED",
        -229: "ERR_SYMLINK",
        -230: "ERR_DB_CONN_LOST",
        -231: "ERR_CRYPTO",
        -232: "ERR_ABORTED_ON_EXIT",
        -233: "ERR_UNSTARTED_LATE",
        -234: "ERR_MISSING_COPROC",
        -235: "ERR_PROC_PARSE",
    }
    return statements.get(int(code))
