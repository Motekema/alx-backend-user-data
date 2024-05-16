#!/usr/bin/env python3
"""
Regex-ing
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    return re.sub(r'(?:^|(?<=\{}))[^{}]*(?=\{}|$)'.format(
        separator, separator, separator),
        redaction, message)


if __name__ == "__main__":
    fields = ["password", "date_of_birth"]
    messages = ["name=egg;email=eggmin@eggsample.com;password=eggcellent;date_of_birth=12/12/1986;",
                "name=bob;email=bob@dylan.com;password=bobbycool;date_of_birth=03/04/1993;"]
    for message in messages:
        print(filter_datum(fields, 'xxx', message, ';'))
