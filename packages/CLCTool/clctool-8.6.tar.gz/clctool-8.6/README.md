[![Upload Python Package](https://github.com/SpoinkOSDevs/CLCTool/actions/workflows/python-publish.yml/badge.svg)](https://github.com/SpoinkOSDevs/CLCTool/actions/workflows/python-publish.yml)

---

# CLCTool Documentation

## Introduction

Welcome to CLCTool, a powerful and customizable Linux configuration tool designed for flexible system setup and deployment.

### Features

- Modular architecture for maximum scalability and customization.
- Dynamic loading of user-defined modules.
- User-defined functions (UDFs) for encapsulating complex logic.
- Conditional task execution and interactive prompts.

## Installation

### Prerequisites

- Python 3.6 or higher

### Instructions

1. Clone the CLCTool repository:

    ```bash
    git clone https://github.com/SpoinkOSDevs/CLCTool.git
    ```

2. Install requirements

    ```bash
    sudo pip install -r ./requirements.txt --break-system-packages
    ```

4. Change into the CLCTool directory:

    ```bash
    cd CLCTool
    ```

5. Run CLCTool with your desired configuration:

    ```bash
    sudo python clctool.py -i path/to/module -p your_profile -v your_version
    ```

    Replace `path/to/module` with the path to your module file, `your_profile` with the chosen profile, and `your_version` with the desired version.

## Usage

CLCTool provides a simple command-line interface for running your customized installation process. The tool supports various commands and options to tailor the deployment according to your needs.

```bash
 sudo python clctool.py -i path/to/module -p your_profile -v your_version
```

- `-i` or `--modules`: Specify the paths to the ``.fox`` file.
- `-p` or `--profile`: Specify the profile to use.
- `-v` or `--version`: Specify the version.
- `-m` or `--module-args`: Specify additional module-specific arguments as key-value pairs separated by commas

## Configuration

### Module Configuration

Modules are the building blocks of CLCTool. Each module is defined in a `.fox` file containing tasks, UDFs, and configurations.

### User-Defined Functions (UDFs)

UDFs allow encapsulating complex logic and reusing it across different parts of the installation process.

```python
def custom_udf(parameters):
    print(f"Running a custom UDF with parameters: {parameters}")
```

## Issue Tracker Link

- GitHub Issues: [CLCTool Issues](https://github.com/SpoinkOSDevs/CLCTool/issues)

---

## Demo

 Link: [Demo Module](https://github.com/SpoinkOSDevs/CLCTModuleRepo/blob/main/modules/nginx.fox)
