"""
AWS CloudWatch Logger Module

This module provides a CloudWatch logger implementation using boto3 for AWS
CloudWatch Logs. It allows logging messages with different log levels, and
it can be configured to use CloudWatch or print logs to the console.

Usage:
    - Create an instance of CloudWatchLogger with the desired log level.
    - Use the logger instance to log messages at various levels
      (info, error, warning, debug, critical).
    - The logger can be configured to use CloudWatch or print
      logs to the console.
"""

import os
import time
from datetime import datetime, timedelta

import boto3
from dotenv import load_dotenv

load_dotenv()


def generate_log_stream_name():
    """
    Generate a rounded UTC timestamp for use as a CloudWatch log stream name.

    Returns:
        str: A formatted string representing the rounded UTC timestamp.
    """
    current_time = datetime.utcnow()
    rounded_time = current_time - timedelta(
        minutes=current_time.minute % 20,
        seconds=current_time.second,
        microseconds=current_time.microsecond,
    )

    return rounded_time.strftime("%Y-%m-%dT%H%M%S")


class CloudWatchLogger:
    """
    AWS CloudWatch Logger Class

    This class provides a CloudWatch logger implementation. It
    can be configured to use CloudWatch for logging, and it allows setting
    different log levels.

    Attributes:
        log_level (str): The current log level
        ('info', 'error', 'warning', 'debug', 'critical').
        use_cw (bool): A flag indicating whether to use CloudWatch for logging.
        log_group_name (str): The name of the CloudWatch log group.
        log_stream_name (str): The name of the CloudWatch log stream.

    Methods:
        config(log_group_name=None, log_level=None): Configure the
        logger with new settings.
        set_level(log_level): Set the log level for the logger.
        info(message): Log an informational message.
        error(message): Log an error message.
        warning(message): Log a warning message.
        debug(message): Log a debug message.
        critical(message): Log a critical message.
    """

    _loggers = {}
    _client = None  # Class variable to store the client

    def __init__(self, log_level="all"):
        """
        Initialize the CloudWatchLogger instance.
        """
        self.log_level = log_level
        self.use_cw = os.getenv("USE_CLOUDWATCH", "true").lower() == "true"
        self.log_group_name = None

        if self.use_cw:
            self._initialize_cloudwatch()

    @classmethod
    def get_logger(cls, name, log_level="all"):
        """
        Get a logger instance by name. Create a new one if not exists.
        """
        logger_name = f"{name}_{log_level}"
        if logger_name not in cls._loggers:
            cls._loggers[logger_name] = cls(log_level=log_level)
            cls._loggers[logger_name].config(log_group_name=name)
        return cls._loggers[logger_name]

    @classmethod
    def _initialize_cloudwatch(cls):
        """
        Initialize the AWS CloudWatch client and create the log stream.
        """
        if cls._client is None:
            cls._client = boto3.client(
                "logs",
                region_name=os.getenv("AWS_REGION"),
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
        cls.log_stream_name = generate_log_stream_name()

    def config(self, log_group_name=None, log_level=None):
        """
        Configure the CloudWatchLogger with new settings.

        Args:
            log_group_name (str, optional): The new log group name.
            log_level (str, optional): The new log level.
        """
        if log_group_name:
            self.log_group_name = log_group_name + "/" + os.getenv("ENV_NAME")
            self._create_log_group_if_not_exists(self.log_group_name)
        self._create_log_stream_if_not_exists()

        if log_level is not None:
            self.set_level(log_level)

    def _create_log_group_if_not_exists(self, log_group_name):
        """
        Create the specified log group if it does not exist.

        Args:
            log_group_name (str): The name of the log group to create.
        """
        if log_group_name and self.use_cw:
            try:
                # Use the class variable _client instead of self.client
                self._client.create_log_group(logGroupName=log_group_name)
            except self._client.exceptions.ResourceAlreadyExistsException:
                pass

    def _create_log_stream_if_not_exists(self):
        """
        Create the log stream if it does not exist.
        """
        if self.use_cw:
            try:
                self._client.create_log_stream(
                    logGroupName=self.log_group_name, logStreamName=self.log_stream_name
                )
                self.info(
                    f"Log stream '{self.log_stream_name}' " f"created successfully."
                )
            except self._client.exceptions.ResourceAlreadyExistsException:
                pass

    def set_level(self, log_level):
        """
        Set the log level for the logger.
        """
        log_levels = ["info", "error", "warning", "debug", "critical", "all"]
        if log_level not in log_levels:
            raise ValueError(
                f"Invalid log level. " f"Use one of: {', '.join(log_levels)}"
            )

        self.log_level = log_level
        self.info(f"Log level set to '{log_level}'")

    def _log(self, message):
        """
        Internal method to log a message to CloudWatch or the console.

        Args:
            message (str): The log message to be logged.
        """
        if self.use_cw:
            log_event = {"timestamp": int(time.time()) * 1000, "message": message}
            if self.log_group_name is None:
                raise ValueError(
                    "Log group name is not set. Please set it " "with config method."
                )
            self._client.put_log_events(
                logGroupName=self.log_group_name,
                logStreamName=self.log_stream_name,
                logEvents=[log_event],
            )
        else:
            print(message)

    def info(self, message):
        """
        Log an informational message.
        """
        if self.log_level in ["info", "all"]:
            self._log(f"[INFO] {message}")

    def error(self, message):
        """
        Log an error message.
        """
        if self.log_level in ["error", "all"]:
            self._log(f"[ERROR] {message}")

    def warning(self, message):
        """
        Log a warning message.
        """
        if self.log_level in ["warning", "all"]:
            self._log(f"[WARNING] {message}")

    def debug(self, message):
        """
        Log a debug message.
        """
        if self.log_level in ["debug", "all"]:
            self._log(f"[DEBUG] {message}")

    def critical(self, message):
        """
        Log a critical message.
        """
        if self.log_level in ["critical", "all"]:
            self._log(f"[CRITICAL] {message}")


getLogger = CloudWatchLogger.get_logger
