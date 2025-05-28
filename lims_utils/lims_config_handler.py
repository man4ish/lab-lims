"""
Module: configuration_manager.py

This module provides a utility class, `ConfigurationManager`, for managing configuration 
settings using environment variables and command-line arguments. It simplifies the 
process of setting, retrieving, and updating key configuration options such as 
`config_file` and `environment`.

Key Features:
- Set configuration values in environment variables
- Retrieve current configuration as a dictionary
- Update configuration via command-line arguments using `argparse`

Classes:
    ConfigurationManager: Handles reading, setting, and updating configuration options.

Example Usage (Command Line):
    python configuration_manager.py --config-file config.yaml --environment production

Environment Variables Set:
    CONFIG_FILE: Path to the configuration file
    ENVIRONMENT: The current execution environment (e.g., dev, staging, production)
"""

import os
import argparse
from typing import Dict, Optional

class ConfigurationManager:
    """
    Utility class for managing configuration settings using environment variables.
    """

    def set_config(self, config_file: str, environment: str) -> None:
        """
        Sets the 'config_file' and 'environment' options as environment variables.

        Args:
            config_file (str): New value for the 'config_file' option.
            environment (str): New value for the 'environment' option.

        Returns:
            None
        """
        os.environ['CONFIG_FILE'] = config_file
        os.environ['ENVIRONMENT'] = environment

    def get_config(self) -> Dict[str, Optional[str]]:
        """
        Retrieves the 'config_file' and 'environment' options from environment variables.

        Returns:
            dict: A dictionary containing 'config_file' and 'environment' options.
        """
        return {
            "config_file": os.getenv('CONFIG_FILE', None),
            "environment": os.getenv('ENVIRONMENT', None)
        }

    def update_config(self) -> None:
        """
        Updates configuration options via command-line arguments.

        This method utilizes the argparse module to parse command-line arguments for updating
        'config_file' and 'environment' options. It calls the set_config method to apply the changes
        and prints the updated configuration options.

        Command-line Arguments:
            --config-file, -c: New value for the 'config_file' option.
            --environment, -e: New value for the 'environment' option.

        Example:
            To update configuration options via command line:
            ```
            python script.py --config-file new_config.ini --environment production
            ```

        Prints:
            - 'Configuration set up successfully.' if both 'config_file' and 'environment' options'
             are provided.
            - 'Please provide values for both --config-file and --environment options.' otherwise.

        Returns:
            None
        """
        parser = argparse.ArgumentParser(
            description='Update configuration options'
        )
        parser.add_argument(
            '--config-file',
            '-c',
            type=str,
            required=True,
            help='New value for config_file option'
        )
        parser.add_argument(
             '--environment', 
             '-e', 
             type=str,
             required=True,
             help='New value for environment option'
        )
        args = parser.parse_args()

        if args.config_file and args.environment:
            self.set_config(args.config_file, args.environment)
            print('Configuration set up successfully.')
        else:
            print('''
            Please provide values for both --config-file and --environment options.
            ''')

        print("After setting config:")
        print(self.get_config())

if __name__ == "__main__":
    config_manager = ConfigurationManager()
    config_manager.update_config()