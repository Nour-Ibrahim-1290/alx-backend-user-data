#!/usr/bin/env python3
"""Personal Data"""

import os
import re
import logging
import mysql.connector
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
        ) -> str:
    """Returns the log message obfuscated
    """
    for field in fields:
        message = re.sub(
            field + "=.*?" + separator,
            field + "=" + redaction + separator,
            message
            )
    return message


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database."""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    db = mysql.connector.connect(
        host=host,
        port=3306,
        user=username,
        password=password,
        database=db_name,
    )
    return db


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns a formatted LogRecord.
        """
        original_message = super().format(record)
        return filter_datum(
            self.fields,
            self.REDACTION,
            original_message,
            self.SEPARATOR
            )


def main():
    """Main function that retrieves and displays user data."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")

    # Create a logger
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter(
        '%(message)s',
        ['name', 'email', 'phone', 'ssn', 'password']
        )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    for row in cursor:
        user_data = {
            'name': row[0],
            'email': row[1],
            'phone': row[2],
            'ssn': row[3],
            'password': row[4],
            'ip': row[5],
            'last_login': row[6],
            'user_agent': row[7]
        }
        logger.info(user_data)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
