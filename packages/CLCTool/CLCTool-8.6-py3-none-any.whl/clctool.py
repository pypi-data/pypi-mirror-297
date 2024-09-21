import argparse
import subprocess
import yaml
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_command(command):
    """Run a shell command with error handling."""
    try:
        subprocess.run(command, shell=True, check=True)
        logging.info(f"Command '{command}' executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command '{command}': {e}")

def install_package(package):
    """Install a package using apt-get."""
    run_command(f"apt-get install -y {package}")

def enable_service(service):
    """Enable and start a system service."""
    run_command(f"systemctl enable {service}")
    run_command(f"systemctl start {service}")

def configure_firewall(rules):
    """Configure firewall rules using ufw."""
    for rule in rules:
        run_command(f"ufw allow {rule}")

def run_task(task, parameters, udfs):
    """Run a specified task based on action type."""
    for action in task:
        action_type, action_data = action.popitem()
        formatted_data = str(action_data).format(**parameters)
        if action_type == 'command':
            run_command(formatted_data)
        elif action_type == 'install_package':
            install_package(formatted_data)
        elif action_type == 'enable_service':
            enable_service(formatted_data)
        elif action_type == 'configure_firewall':
            configure_firewall([str(rule).format(**parameters) for rule in action_data])
        elif action_type == 'prompt':
            prompt_value = input(formatted_data)
            parameters[action['parameter']] = prompt_value
        elif action_type == 'udf':
            udf_name = formatted_data
            if udf_name in udfs:
                udfs[udf_name](parameters)
        else:
            logging.warning(f"Unknown action type: {action_type}")

def load_module(module_path):
    """Load a module from a YAML file."""
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    try:
        with open(module_path, 'r') as file:
            module_data = yaml.safe_load(file)
        logging.info(f"Module '{module_name}' loaded successfully.")
        return module_name, module_data
    except Exception as e:
        logging.error(f"Error loading module '{module_path}': {e}")
        return None, None

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='CLCTool - Custom Linux configuration tool')
    parser.add_argument('-i', '--input', help='Specify the path to a module .fox file for standalone execution')
    parser.add_argument('-p', '--profile', help='Specify the profile to use', default='default')
    parser.add_argument('-v', '--version', help='Specify the version', default='1.0')
    parser.add_argument('-m', '--module-args', help='Specify additional module-specific arguments as key-value pairs separated by commas')
    return parser.parse_args()

def main():
    args = parse_args()
    parameters = {
        'profile': args.profile,
        'version': args.version,
    }

    if args.input:
        module_name, module_data = load_module(args.input)
        if module_data:
            run_task(module_data.get('tasks', []), parameters, module_data.get('udfs', {}))
    else:
        logging.info("No module specified. Use the -i option to provide a module .fox file.")

if __name__ == "__main__":
    main()
