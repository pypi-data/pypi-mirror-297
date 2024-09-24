# Terminal Text Effects

Hydraclick supports terminal text effects using the [Terminal Text Effects](https://chrisbuilds.github.io/terminaltexteffects/) library to enhance the user experience with animated and styled text outputs in the terminal.

## Configuring Terminal Text Effects

Terminal text effects can be customized by adjusting print speeds, return speeds, and gradient colors. To apply terminal effects in Hydraclick, you can use the `terminal_effect` parameter provided in the `hydra_command` decorator.

Example of setting terminal effects:

```python
from hydraclick import hydra_command, set_terminal_effect, display_terminal_effect
from terminaltexteffects.utils.graphics import Color

# Configure the effect
def config_effect(effect):
    effect.effect_config.print_speed = 15
    effect.effect_config.print_head_return_speed = 5
    effect.effect_config.final_gradient_stops = (Color("00ffae"), Color("00D1FF"), Color("FFFFFF"))
    return effect

# Set the terminal effect globally
set_terminal_effect(display_terminal_effect)

@hydra_command(config_path="config", config_name="my_config", terminal_effect=display_terminal_effect)
def my_function(config):
    print(f"Running with config: {config.pretty()}")
```

In this example, the `set_terminal_effect` function applies the terminal effect to help messages and command execution, providing animated and styled output.

## Disabling Terminal Effects

To disable terminal effects globally, set the following environment variables:

- `OMEGACLICK_NO_TERMINAL_EFFECTS`
- `NO_TERMINAL_EFFECTS`

Setting either of these to `true`, `1`, or `yes` will disable all terminal effects:

```bash
export OMEGACLICK_NO_TERMINAL_EFFECTS=true
```

Hydraclick detects these variables and disables the effects accordingly.

## Example Usage

Hydraclick's CLI help messages and commands can be displayed with terminal effects. The `display_terminal_effect` function shows a text-based animation:

```python
from hydraclick import display_terminal_effect

display_terminal_effect("Hello, world!")
```

By passing `display_terminal_effect` into the `hydra_command` decorator as the `terminal_effect` parameter, the terminal effects are automatically applied to your CLI.

## Using the `terminal_effect` Parameter in `hydra_command`

The `hydra_command` decorator allows you to specify a terminal effect through the `terminal_effect` parameter. When provided, it ensures the help messages and CLI output are animated with the specified effect.

Example of using `hydra_command` with terminal effects:

```python
from hydraclick import hydra_command, display_terminal_effect

@hydra_command(config_path="config", config_name="app_config", terminal_effect=display_terminal_effect)
def my_function(config):
    print(f"Running with config: {config.pretty()}")
```

This integrates terminal effects seamlessly into your CLI, adding visual appeal and dynamic text output.
