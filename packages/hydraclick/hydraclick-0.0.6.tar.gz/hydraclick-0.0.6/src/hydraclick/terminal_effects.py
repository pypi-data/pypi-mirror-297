import shutil
from typing import Optional, Callable
import os
import sys

import click
from click import Context, Option


def get_no_terminal_effects() -> bool:
    """Check if terminal effects should be disabled by looking at environment variables.

    This function checks the environment variables `OMEGACLICK_NO_TERMINAL_EFFECTS`
    and `NO_TERMINAL_EFFECTS` to determine if terminal effects should be disabled.
    If no environment variable is set, it returns `False`.

    Returns:
        bool: `True` if terminal effects should be disabled, `False` otherwise.

    Example:
        >>> os.environ["NO_TERMINAL_EFFECTS"] = "true"
        >>> get_no_terminal_effects()
        True

    """
    val = os.environ.get("OMEGACLICK_NO_TERMINAL_EFFECTS", os.environ.get("NO_TERMINAL_EFFECTS"))
    if val is None:
        return False
    return val.lower() in {"true", "1", "yes"}


def config_effect(effect):
    """Configure terminal effects such as print speed and gradient colors.

    This function adjusts the terminal effect's configuration, such as print speed,
    return speed, and gradient colors for rendering.

    Args:
        effect: The terminal effect object to be configured.

    Returns:
        The modified terminal effect object.

    Example:
        >>> effect = SomeEffect()
        >>> config_effect(effect)
        <configured effect>

    """
    from terminaltexteffects.utils.graphics import Color  # noqa: PLC0415

    effect.effect_config.print_speed = 15
    effect.effect_config.print_head_return_speed = 5
    effect.effect_config.final_gradient_stops = (Color("00ffae"), Color("00D1FF"), Color("FFFFFF"))
    return effect


def remove_lines(num_lines: int):
    """Remove the last `num_lines` lines printed in the terminal.

    This function sends ANSI escape codes to move the terminal cursor up and clear
    the last `num_lines` lines from the terminal.

    Args:
        num_lines (int): The number of lines to remove.

    Example:
        >>> remove_lines(3)  # Removes the last 3 printed lines

    """
    for _ in range(num_lines):
        sys.stdout.write("\x1b[1A")  # Move the cursor up one line
        sys.stdout.write("\x1b[2K")  # Clear the entire line
    sys.stdout.flush()


def count_wrapped_lines(text: str, terminal_width: int) -> int:
    """Calculate the number of lines the given text will take when wrapped in the terminal.

    Args:
        text (str): The text to be wrapped.
        terminal_width (int): The width of the terminal in characters.

    Returns:
        int: The number of lines the text will occupy in the terminal.

    Example:
        >>> count_wrapped_lines("This is a long line of text.", 10)
        3

    """
    lines = text.splitlines()
    total_lines = 0
    for line in lines:
        if terminal_width > 0:
            num_terminal_lines = (len(line) + terminal_width - 1) // terminal_width
        else:
            num_terminal_lines = 1
        total_lines += max(num_terminal_lines, 1)
    return total_lines


def display_terminal_effect(value: str, effect_cls=None):
    """Display a terminal effect animation for a given text.

    This function displays a text-based terminal effect using the provided effect class.
    The effect is rendered with custom configurations, and once the animation is complete,
    the effect is cleaned up from the terminal.

    Args:
        value (str): The text to display with the terminal effect.
        effect_cls (optional): The class of the terminal effect to use. Defaults to `Print`.

    Example:
        >>> display_terminal_effect("Hello World!")

    """
    from terminaltexteffects.effects.effect_print import Print  # noqa: PLC0415

    effect_cls = effect_cls or Print
    effect = effect_cls(value)
    effect = config_effect(effect)

    with effect.terminal_output() as terminal:
        for frame in effect:
            terminal.print(frame)

    terminal_width = shutil.get_terminal_size().columns
    n_lines_last_rendered_frame = count_wrapped_lines(frame, terminal_width)
    remove_lines(n_lines_last_rendered_frame)

    last_effect = effect_cls(value)
    last_effect = config_effect(last_effect)
    last_effect.terminal_config.ignore_terminal_dimensions = True
    last_frame = list(last_effect)[-1]

    sys.stdout.write(last_frame.lstrip())
    sys.stdout.write("\n")
    sys.stdout.flush()


def patch_parse_args(terminal_effect: Callable):
    """Patch the Click `parse_args` function to display a terminal effect.

    This function overrides the `parse_args` method of Click's `MultiCommand` to
    display a custom terminal effect for the help message when no arguments are passed.

    Args:
        terminal_effect (Callable): A callable that renders the terminal effect.

    Example:
        >>> patch_parse_args(display_terminal_effect)

    """

    def parse_args(self, ctx: Context, args: list[str]) -> list[str]:
        """Display the help message with terminal effects when no arguments are provided."""
        if not args and self.no_args_is_help and not ctx.resilient_parsing:
            terminal_effect(ctx.get_help())
            ctx.exit()

        rest = super(click.core.MultiCommand, self).parse_args(ctx, args)
        if self.chain:
            ctx.protected_args = rest
            ctx.args = []
        elif rest:
            ctx.protected_args, ctx.args = rest[:1], rest[1:]
        return ctx.args

    click.core.MultiCommand.parse_args = parse_args


def patch_get_help_option(terminal_effect: Callable):
    """Patch the Click `get_help_option` function to display a terminal effect for the help option.

    This function overrides Click's `get_help_option` method to display a terminal
    effect whenever the help message is requested.

    Args:
        terminal_effect (Callable): A callable that renders the terminal effect.

    Example:
        >>> patch_get_help_option(display_terminal_effect)

    """

    def get_help_option(self, ctx: Context) -> Optional["Option"]:
        """Return the help option with a terminal effect callback."""
        from gettext import gettext  # noqa: PLC0415

        help_options = self.get_help_option_names(ctx)

        if not help_options or not self.add_help_option:
            return None

        def show_help(ctx: Context, param: "click.Parameter", value: str) -> None:  # noqa: ARG001
            if value and not ctx.resilient_parsing:
                terminal_effect(ctx.get_help())
                ctx.exit()

        return Option(
            help_options,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=show_help,
            help=gettext("Show this message and exit."),
        )

    click.core.Command.get_help_option = get_help_option


def set_terminal_effect(terminal_effect: Callable):
    """Set a terminal effect animation for displaying help in Click commands.

    This function applies a patch to the Click `parse_args` and `get_help_option`
    methods, so the help message is displayed with the specified terminal effect.

    Args:
        terminal_effect (Callable): A callable that renders the terminal effect.

    Example:
        >>> set_terminal_effect(display_terminal_effect)

    """
    if not get_no_terminal_effects():
        patch_parse_args(terminal_effect)
        patch_get_help_option(terminal_effect)
