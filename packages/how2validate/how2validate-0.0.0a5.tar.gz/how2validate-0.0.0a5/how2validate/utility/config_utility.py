import configparser

# Global variable to hold the configuration
config = None

# Function to initialize and load the configuration file
def init_config():
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')

# Function to get the package name from the DEFAULT section
def get_package_name():
    if config:
        return config.get('DEFAULT', 'package_name')
    else:
        raise ValueError("Configuration not initialized. Call init_config() first.")

# Function to get the active secret status from the SECRET section
def get_active_secret_status():
    if config:
        return config.get('SECRET', 'secret_active')
    else:
        raise ValueError("Configuration not initialized. Call init_config() first.")

# Function to get the inactive secret status from the SECRET section
def get_inactive_secret_status():
    if config:
        return config.get('SECRET', 'secret_inactive')
    else:
        raise ValueError("Configuration not initialized. Call init_config() first.")
    
# Function to get the version from the DEFAULT section
def get_version():
    if config:
        return config.get('DEFAULT', 'version')
    else:
        raise ValueError("Configuration not initialized. Call init_config() first.")

# Initialization block to load the config when the module is imported or run
init_config()
