# Hydraclick

Hydraclick is an open-source Python package that seamlessly integrates [Hydra](https://hydra.cc/) and [Click](https://click.palletsprojects.com/) to create production-grade command-line interfaces (CLIs). It leverages Hydra's powerful configuration management with Click's user-friendly CLI creation to provide a robust foundation for building complex CLI applications.

## Features

- **Configuration Management**: Utilize Hydra's dynamic configuration capabilities for flexible CLI options.
- **Structured Logging**: Integrate with flogging for structured and efficient logging.
- **Easy Decorators**: Simple decorators to convert functions into CLI commands.
- **Extensible**: Easily extend and customize to fit your project's needs.
- **Shell Completion**: Support for generating shell completion scripts.

## Installation

Install Hydraclick via pip:

```bash
pip install hydraclick
```

### Supported Python Versions

Hydraclick supports the following Python versions:

- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

### Supported Operating Systems

Hydraclick is compatible with the following operating systems:

- Ubuntu (latest)
- macOS (latest)

## Getting Started

### Basic Usage

Define your function and decorate it with `@hydra_command` to create a CLI command.

```python
from omegaconf import DictConfig
from hydraclick import hydra_command

@hydra_command(config_path="config_folder", config_name="file_without_extension")
def my_function(config: DictConfig):
    print(f"Running with config: {config.pretty()}")
```

### Running the CLI

After defining your function, you can run it from the command line:

```bash
python my_script.py --config-path path/to/config --config-name my_config
```

### Example

Here's a complete example of creating a CLI with Hydraclick:

```python
import sys
from omegaconf import DictConfig
from hydraclick import hydra_command

@hydra_command(config_path="configs", config_name="app_config", as_kwargs=True)
def main(**kwargs):
    print(f"Running with config: {kwargs}")

if __name__ == "__main__":
    main()
```

## API Reference

### `hydra_command`

Decorator to create CLI commands.

```python
import omegaconf

def hydra_command(
        config_path: str | Path | None = None,
        config_name: str | None = "config",
        version_base: str | None = None,
        as_kwargs: bool = False,
        preprocess_config: Callable[[DictConfig], DictConfig] | None = None,
        print_config: bool = True,
        resolve: bool = True,
        use_flogging: bool = True,
        terminal_effect: Callable | None = omegaconf.MISSING,
        **flogging_kwargs: Any,
) -> Callable:
```

## Configuration Options

Hydraclick provides several configuration options to customize your CLI:

- `config_path`: Path to the configuration directory. Passed to [`hydra.main()`](https://hydra.cc/docs/tutorials/basic/your_first_app/config_file/)
- `config_name`: Name of the configuration file. Passed to [`hydra.main()`](https://hydra.cc/docs/tutorials/basic/your_first_app/config_file/)
- `version_base`: Base version of the configuration. Passed to [`hydra.main()`](https://hydra.cc/docs/tutorials/basic/your_first_app/config_file/)
- `as_kwargs`: The mode in which to run the function. If `True`, the function is run with the configuration as keyword arguments. In this case, the configuration is converted to a dictionary before passing it to the function. If `False`, pass the configuration as a single `OmegaConf.DictConfig` object. Defaults to `False`.
- `preprocess_config`: Function to preprocess the configuration. It takes a `DictConfig` object and returns a `DictConfig` object.
- `print_config`: Whether to print the configuration before execution.
- `resolve`: Whether to resolve the configuration.
- `use_flogging`: Whether to use flogging for structured logging.
- `**flogging_kwargs`: Additional keyword arguments for flogging.
- `terminal_effect`: The terminal effect function to use when rendering the command help.

## Logging with Flogging

Hydraclick integrates with [flogging](https://github.com/FragileTech/flogging) for structured logging.
To enable flogging, ensure it's installed:

```bash
pip install hydraclick[flogging]
```

```bash
pip install flogging
```

If `flogging` is not available, Hydraclick will log a warning and disable structured logging.

## Terminal Text Effects

Hydraclick supports terminal text effects using the [Terminal Text Effects](https://chrisbuilds.github.io/terminaltexteffects/) library to enhance the user experience with animated and styled text outputs in the terminal.
Install the library with:
```bash
pip install hydraclick[terminaltexteffects]
```

```bash
pip install terminaltexteffects
```

## Installing all the extras

To install all the extras, use the following command:

```bash
pip install hydraclick[all]
```

## Shell Completion

Hydraclick supports generating shell completion scripts. Use the `--shell-completion` option to generate scripts for your preferred shell.

```bash
cli_app command --shell-completion install=bash > my_script_completion.sh
source my_script_completion.sh
```

## Contribution

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes with clear messages.
4. Submit a pull request detailing your changes.

For major changes, please open an issue first to discuss your ideas.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Support

If you encounter any issues or have questions, feel free to open an issue on the [GitHub repository](https://github.com/yourusername/hydraclick).

## Acknowledgements

- [Hydra](https://hydra.cc/) for powerful configuration management.
- [Click](https://click.palletsprojects.com/) for creating beautiful CLIs.
- [Flogging](https://github.com/FragileTech/flogging) for structured logging.
- [Terminal Text Effects](https://chrisbuilds.github.io/terminaltexteffects) for enhancing terminal help text output.
