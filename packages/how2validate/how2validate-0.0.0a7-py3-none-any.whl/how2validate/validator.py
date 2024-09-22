import argparse
import logging

from how2validate.utility.config_utility import get_active_secret_status, get_inactive_secret_status, get_package_name, get_version
from how2validate.utility.tool_utility import format_serviceprovider, format_services, format_string, get_secretprovider, get_secretservices, redact_secret, update_tool, validate_choice
from how2validate.utility.log_utility import setup_logging
from how2validate.handler.validator_handler import validator_handle_service

# Call the logging setup function
setup_logging()

# Custom formatter to remove choices display but keep custom help text
class CustomHelpFormatter(argparse.RawTextHelpFormatter):
    def _get_help_string(self, action):
        help_msg = action.help
        if action.choices:  # Remove choices from help string if present
            help_msg = help_msg.split(" (choices:")[0]
        return help_msg

def parse_arguments():
    parser = argparse.ArgumentParser(
    prog="How2Validate Tool",
    description="Validate various types of secrets for different services.",
    usage="%(prog)s",
    epilog="Ensuring the authenticity of your secrets.",
    formatter_class=CustomHelpFormatter)

    # Retrieve choices from environment variable
    provider = get_secretprovider()
    services = get_secretservices()

    # Define arguments
    parser.add_argument('-provider',  type=lambda s: validate_choice(s, provider), required=False,
                        help=f"Secret provider to validate secrets\nSupported providers:\n{format_serviceprovider()}")
    parser.add_argument('-service',  type=lambda s: validate_choice(s, services), required=False,
                        help=f"Service / SecretType to validate secrets\nSupported services:\n{format_services()}")
    parser.add_argument('-secret', required=False,
                        help="Pass Secrets to be validated")
    parser.add_argument('-r', '--response', action='store_true',
                        help=f"Prints {get_active_secret_status()}/ {get_inactive_secret_status()} upon validating secrets.")
    parser.add_argument('-report', action='store_false', default=False,
                        help=f"Reports validated secrets over E-mail")
    parser.add_argument('-v', '--version', action='version', version=f'How2Validate Tool version {get_version()}', 
                        help='Expose the version')
    parser.add_argument('--update', action='store_true',
                        help='Hack the tool to the latest version.')

    return parser.parse_args()

def validate(provider,service, secret, response, report):
    
    logging.info(f"Started validating secret...")
    result = validator_handle_service(format_string(service), secret, response, report)
    logging.info(f"{result}")
    return f"{result}"

def main(args=None):
    if args is None:
        args = parse_arguments()

    if args.update:
        try:
            logging.info("Initiating tool update...")
            update_tool()
            logging.info("Tool updated successfully.")
        except Exception as e:
            logging.error(f"Error during tool update: {e}")
        return

    if not args.provider or not args.service or not args.secret:
        logging.error("Missing required arguments: -Provider, -Service, -Secret")
        logging.error("Use '-h' or '--help' for usage information.")
        return

    try:
        logging.info(f"Initiating validation for service: {args.service} with secret: {redact_secret(args.secret)}")
        result = validate(args.provider, args.service, args.secret, args.response, args.report)
        logging.info("Validation completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during validation: {e}")
        print(f"Error: {e}")