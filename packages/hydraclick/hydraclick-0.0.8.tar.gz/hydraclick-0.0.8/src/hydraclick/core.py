import functools
import logging
import sys
from pathlib import Path
from typing import Callable, Any

import hydra
import omegaconf
from omegaconf import DictConfig, OmegaConf
from unittest.mock import patch

from hydraclick import set_terminal_effect
from hydraclick.display_config import display_config
from hydraclick.options import (
    hydra_args_argument,
    hydra_help_option,
    version_option,
    show_config_option,
    resolve_option,
    package_option,
    info_option,
    run_option,
    multirun_option,
    config_path_option,
    config_dir_option,
    config_name_option,
    shell_completion_option,
)
from hydraclick.terminal_effects import display_terminal_effect

_logger = logging.getLogger(__name__)

try:
    import flogging

    FLOGGING_AVAILABLE = True
except ImportError:
    FLOGGING_AVAILABLE = False


def wrap_kwargs_and_config(
    function: Callable,
    as_kwargs: bool = False,
    print_config: bool = True,
    preprocess_config: Callable[[DictConfig], DictConfig] | None = None,
    resolve: bool = True,
):
    """Wrap a function to run as a hydra command."""

    @functools.wraps(function)
    def wrapper(config):
        if preprocess_config:
            config = preprocess_config(config)
        if isinstance(config, DictConfig) and resolve:
            try:
                OmegaConf.resolve(config)
            except Exception as e:
                display_config(config, logger=_logger)
                raise e
        if print_config:
            display_config(config, logger=_logger)
        if not as_kwargs:
            return function(config)
        conf_dict = OmegaConf.to_container(config, resolve=resolve)
        return function(**conf_dict)

    return wrapper


def build_hydra_args(
    hydra_help: bool,
    version: bool,
    show_config: str,
    resolve: bool,
    package: str,
    info: bool,
    run: bool,
    multirun: bool,
    config_path: str,
    config_name: str,
    config_dir: str,
    shell_completion: bool,
    hydra_args: tuple[str, ...] | None = None,
) -> tuple[str, ...]:
    """Compose the arguments for the hydra command."""
    _logger.debug(f"Hydra args: {hydra_args}")
    hydra_args_ = []
    if hydra_help:
        hydra_args_.append("--hydra-help")
    if version:
        hydra_args_.append("--version")
    if show_config:
        hydra_args_.extend(("--cfg", show_config))
    if resolve:
        hydra_args_.append("--resolve")
    if package:
        hydra_args_.extend(("--package", f"{package}"))
    if info:
        hydra_args_.append("--info")
    if run:
        hydra_args_.append("--run")
    if multirun:
        hydra_args_.append("--multirun")
    if config_path:
        hydra_args_.extend(("--config-path", f"{config_path}"))
    if config_name:
        hydra_args_.extend(("--config-name", f"{config_name}"))
    if config_dir:
        hydra_args_.extend(("--config-dir", f"{config_dir}"))
    if shell_completion:
        hydra_args_.extend(("--shell-completion", f"{shell_completion}"))
    _logger.debug(f"Hydra args after composition: {hydra_args}")
    return (*hydra_args_, *hydra_args)


def get_default_dir() -> str:
    """Get the default directory for the hydra config."""
    curr_dir = Path().cwd()
    # if there is a `config` folder inside curr_dir, return its path, otherwise return curr_dir
    return str(curr_dir / "config") if (curr_dir / "config").exists() else str(curr_dir)


def run_hydra(
    function: Callable,
    hydra_args: tuple[str, ...],
    config_path: str | None = None,
    config_name: str | None = "config",
    version_base: str | None = None,
    use_flogging: bool = True,
    **flogging_kwargs: Any,
) -> Any:
    """Run a function as a Hydra app.

    Args:
        function (Callable): The function to be executed as a Hydra command. This function \
            should accept a `DictConfig` object as its argument.
        hydra_args (tuple[str, ...]): The arguments to pass to the Hydra command.
        config_path (str | None, optional): The path to the configuration directory. If not \
            specified, the default directory is used, which is the current working \
            directory/config. Defaults to None.
        config_name (str | None, optional): The name of the configuration file \
            (without the `.yaml` or `.yml` extension). Defaults to "config".
        version_base (str | None, optional): The base version of the configuration. \
            Defaults to None.
        use_flogging (bool, optional): Whether to use the `flogging` library for \
            structured logging. Defaults to True.
        **flogging_kwargs (Any, optional): Additional keyword arguments to pass to \
            the `flogging.setup` function.

    Returns:
        Then return value of the function.

    """

    @hydra.main(config_path=config_path, config_name=config_name, version_base=version_base)
    @functools.wraps(function)
    def _run_hydra_function(loaded_config: DictConfig):
        if use_flogging:
            flogging.setup(**flogging_kwargs)
        return function(loaded_config)

    with patch("sys.argv", [sys.argv[0], *list(hydra_args)]):
        return _run_hydra_function()


def command_api(
    function: Callable[[DictConfig | dict[str, Any]], Any],
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
    """Integrate Hydra's configuration management capabilities with a Click-based CLI.

    Args:
        function (Callable[[DictConfig], Any]): The function to be executed as a Hydra command. \
            This function should accept a `DictConfig` object as its argument.
        config_path (str | Path | None, optional): The path to the configuration directory. \
            If not specified, the default directory is used.
        config_name (str | None, optional): The name of the configuration file \
            (without the `.yaml` or `.yml` extension). Defaults to `"config"`.
        version_base (str | None, optional): The base version of the configuration. \
            Defaults to `None`.
        as_kwargs (bool, optional): The mode in which to run the function. \
            If `True`, the function is run with the configuration as keyword arguments. In \
            this case the configuration is converted to a dictionary before passing it to the \
            function. Defaults to `False`.
        preprocess_config (Callable[[DictConfig], DictConfig] | None, optional): A function \
            to preprocess the configuration before passing it to the main function. \
            Defaults to `None`.
        print_config (bool, optional): Whether to print the configuration before \
            running the function. Defaults to `True`.
        resolve (bool, optional): Whether to resolve the configuration before running the \
            function. Defaults to `True`.
        use_flogging (bool, optional): Whether to use the `flogging` library for structured \
            logging. Defaults to `True`.
        terminal_effect(Callable | None, optional): The terminal effect function to use when \
            rendering the command help.
        **flogging_kwargs (Any, optional): Additional keyword arguments to pass to the \
            `flogging.setup` function.

    Returns:
        Callable: A Click-compatible command function that can be used as a CLI command.

    Example:
        ```python
        from omegaconf import DictConfig

        def my_function(config: DictConfig):
            print(config.pretty())

        click_command = command_api(
            function=my_function,
            config_path="path/to/config",
            config_name="my_config",
            version_base="1.0",
            run_mode="config",
            preprocess_config=None,
            print_config=True,
            resolve=True,
            use_flogging=True,
            allow_trailing_dot=True
        )
        ```

        In this example, `my_function` is wrapped by `command_api` to create a Click-compatible \
        command. The configuration is loaded from the specified `config_path` and `config_name`, \
        and the function is executed with the resolved configuration.

    Notes:
        - The `command_api` function uses several Hydra and Click decorators to provide \
            a rich CLI experience.
        - If `use_flogging` is enabled but the `flogging` library is not available, \
            a warning is logged, and `flogging` is disabled.
        - The `preprocess_config` function, if provided, allows for custom preprocessing of the \
            configuration before it is passed to the main function.

    """
    if terminal_effect == omegaconf.MISSING:
        terminal_effect = display_terminal_effect
    if terminal_effect is not None:
        set_terminal_effect(terminal_effect)
    config_path = get_default_dir() if config_path is None else str(config_path)
    if config_name is not None:
        config_name = str(config_name).replace(".yaml", "").replace(".yml", "")
    if use_flogging and not FLOGGING_AVAILABLE:
        _logger.warning(
            "Flogging is not available. Run `pip install flogging` to use the structured logging."
        )
        use_flogging = False
    if not flogging_kwargs:
        flogging_kwargs = {"allow_trailing_dot": True}

    @hydra_args_argument
    @hydra_help_option
    @version_option
    @show_config_option
    @resolve_option
    @package_option
    @info_option
    @run_option
    @multirun_option
    @config_path_option
    @config_name_option
    @config_dir_option
    @shell_completion_option
    @functools.wraps(function)
    def click_compatible(
        hydra_help: bool,
        version: bool,
        show_config: str,
        resolve_: bool,
        package: str,
        info: bool,
        run: bool,
        multirun: bool,
        config_path_: str,
        config_name_: str,
        config_dir: str,
        shell_completion: bool,
        hydra_args: tuple[str, ...] | None = None,
    ):
        nonlocal \
            print_config, \
            as_kwargs, \
            preprocess_config, \
            resolve, \
            config_path, \
            config_name, \
            version_base, \
            use_flogging, \
            flogging_kwargs
        if show_config:
            print_config = False
        true_func = wrap_kwargs_and_config(
            function, as_kwargs, print_config, preprocess_config, resolve
        )
        hydra_args = build_hydra_args(
            hydra_help,
            version,
            show_config,
            resolve_,
            package,
            info,
            run,
            multirun,
            config_path_,
            config_name_,
            config_dir,
            shell_completion,
            hydra_args,
        )
        return run_hydra(
            true_func,
            hydra_args=hydra_args,
            config_path=config_path,
            config_name=config_name,
            version_base=version_base,
            use_flogging=use_flogging,
            **flogging_kwargs,
        )

    return click_compatible


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
    """Integrate Hydra's configuration management capabilities with a Click-based CLI.

    Args:
        config_path (str | Path | None, optional): The path to the configuration directory. \
            If not specified, the default directory is used.
        config_name (str | None, optional): The name of the configuration file \
            (without the `.yaml` or `.yml` extension). Defaults to `"config"`.
        version_base (str | None, optional): The base version of the configuration. \
            Defaults to `None`.
        as_kwargs (bool, optional): The mode in which to run the function. \
            If `True`, the function is run with the configuration as keyword arguments. In \
            this case the configuration is converted to a dictionary before passing it to the \
            function. Defaults to `False`.
        preprocess_config (Callable[[DictConfig], DictConfig] | None, optional): A function to \
            preprocess the configuration before passing it to the main function. \
            Defaults to `None`.
        print_config (bool, optional): Whether to print the configuration before \
            running the function. Defaults to `True`.
        resolve (bool, optional): Whether to resolve the configuration before running \
            the function. Defaults to `True`.
        use_flogging (bool, optional): Whether to use the `flogging` library for structured \
            logging. Defaults to `True`.
        terminal_effect(Callable | None, optional): The terminal effect function to use when \
            rendering the command help.
        **flogging_kwargs (Any, optional): Additional keyword arguments to pass to the \
            `flogging.setup` function.

    Returns:
        Callable: A Click-compatible command function that can be used as a CLI command.

    Notes:
        - The `command_api` function uses several Hydra and Click decorators to provide \
            a rich CLI experience.
        - If `use_flogging` is enabled but the `flogging` library is not available, \
            a warning is logged, and `flogging` is disabled.
        - The `preprocess_config` function, if provided, allows for custom preprocessing of the \
            configuration before it is passed to the main function.

    """

    def decorator(function: Callable):
        return command_api(
            function,
            config_path=config_path,
            config_name=config_name,
            version_base=version_base,
            use_flogging=use_flogging,
            as_kwargs=as_kwargs,
            print_config=print_config,
            preprocess_config=preprocess_config,
            resolve=resolve,
            terminal_effect=terminal_effect,
            **flogging_kwargs,
        )

    return decorator
