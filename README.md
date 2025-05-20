# tfds-cli
The free data stack CLI and python api.

The CLI is intended top be a small collection of utilities to
* run docker compose commands on the stack in the relevant order
* provide direct access to the config files for testing
* deploy notebook files to s3
* other basic stack operations like inspecting the availabel stacks and activating a stack.

The project is managed in poetry and CLI framework is the builtin argparse.