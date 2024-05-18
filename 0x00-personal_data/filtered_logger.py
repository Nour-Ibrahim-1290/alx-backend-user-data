#!/usr/bin/env python3
"""Personal Data"""

import re


def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        message = re.sub(
            field + "=.*?" + separator,
            field + "=" + redaction + separator,
            message
            )
    return message
