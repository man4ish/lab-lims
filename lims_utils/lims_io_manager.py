"""
Module for establishing and managing connections to a LIMS database.

This module defines functionality for connecting to a Laboratory Information Management System (LIMS)
database using SQLAlchemy. It includes the `LimsConnector` class, which initializes the connection
based on environment variables and provides an interface for database interactions.

Classes:
    LimsConnector: Handles the setup and management of the LIMS database connection.

Attributes:
    Base: SQLAlchemy's declarative base class used for ORM mappings.
"""

import os
import configparser
from typing import Dict, Union
from urllib.parse import quote_plus
import sqlalchemy
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import yaml

Base = declarative_base()

class LimsConnector:
    """
    A class to manage the connection to a LIMS database.

    Attributes:
        environment (str): The environment name to use from the configuration file.
        engine (sqlalchemy.engine.base.Engine): The SQLAlchemy engine for database connection.
    """

    def __init__(self) -> None:
        """
        Initialize LimsConnector with environment variables or default values.

        Args:
            config_file_path (str): Optional path to the configuration file.
        """
        self.environment: str = os.getenv('LIMS_ENVIRONMENT', 'production')
        self.config_file_path = self.get_config_file_path()
        print(f"Config file path: {self.config_file_path}")
        self.engine: sqlalchemy.engine.base.Engine = None

    def get_config_file_path(self) -> str:
        """
        Get the path to the configuration file.

        Returns:
            str: Path to the configuration file.
        """
        if os.getenv('CONFIG_FILE'):
            return os.getenv('CONFIG_FILE')
        # Fallback to environment variable DATABASE_YML_PATH
        return os.getenv('DATABASE_YML_PATH', 'database.yml')


    def initiate_db(self) -> sqlalchemy.engine.base.Engine:
        """Load database configuration from the secure file or local file"""
        secure_file_path = self.config_file_path

        print(f"Loading configuration from: {secure_file_path}")

        # Read the contents of the secure file
        with open(secure_file_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)[self.environment]

        username = config.get('username')
        password = config.get('password')
        hostname = config.get('host')
        database = config.get('database')
        ssl_ca_path = config.get('sslca')

        if None in [username, password, hostname, database, ssl_ca_path]:
            raise ValueError("Database configuration not properly loaded from YAML file.")

        # Replace placeholder in ssl_ca_path with actual SSL certificate path
        with open(ssl_ca_path, 'r', encoding='utf-8') as ssl_ca_file:
            ssl_ca = ssl_ca_file.read()

        ssl_args: Dict[str, Union[str, Dict[str, str]]] = \
            {'ssl_ca': ssl_ca} if ssl_ca else {}

        connect_args: Dict[str, Dict[str, Union[str, Dict[str, str]]]] = {
            'ssl': ssl_args
        } if ssl_args else {}

        engine: sqlalchemy.engine.base.Engine = sqlalchemy.create_engine(
            f"mysql+pymysql://{username}:{quote_plus(password)}@{hostname}/{database}",
            connect_args=connect_args
        )
        self.engine = engine
        return engine

    def get_session(self) -> Session:
        """
        Create a new session using the initialized engine.

        Returns:
            Session: A new SQLAlchemy session.
        """
        if self.engine is None:
            raise ValueError(
                "Database engine is not initialized. Call initiate_db first."
            )
        return sessionmaker(bind=self.engine)()

    def load_config_from_file(self, file_path: str) -> Dict[str, Dict[str, str]]:
        """
        Load database configuration from a YAML file.

        Args:
            file_path (str): Path to the YAML file containing database configuration.

        Returns:
            dict: Database configuration loaded from the YAML file.
        """
        with open(file_path, 'r', encoding='utf-8') as config_file:
            return yaml.safe_load(config_file)