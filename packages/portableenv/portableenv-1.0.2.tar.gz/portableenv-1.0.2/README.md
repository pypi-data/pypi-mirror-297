# portableenv

`portableenv` is a Python CLI tool that allows you to create virtual environments using an embedded Python interpreter. This makes it easy to manage isolated Python environments without relying on the system-wide Python installation.

## Features

- **Seamless Virtual Environment Creation**: Creates virtual environments using the embedded Python interpreter, ensuring portability and isolation from system-wide installations.
- **Simple CLI Interface**: Provides a command-line interface similar to `virtualenv` for ease of use.

## Installation

Install `portableenv` via pip:

```bash
pip install portableenv
```

## Usage

### Create a Virtual Environment

To create a virtual environment using the embedded Python interpreter, use the following command:

```bash
portableenv myenv
```

This will create a virtual environment named `myenv` using the embedded Python, currently Python 3.10.9.

### Specifying a Different Python Version (Future Feature)

In future releases, you will be able to specify different Python versions:

```bash
portableenv myenv --python 3.9
```

## Requirements

- Python 3.8 or higher
- `virtualenv` library (automatically installed with this package)
- Internet connection for the initial download of the embedded Python interpreter

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes.

## Author

- [AbdulRahim](https://github.com/abdulrahimpds)

## Links

- [GitHub Repository](https://github.com/abdulrahimpds/portableenv)
- [PyPI Package](https://pypi.org/project/portableenv)