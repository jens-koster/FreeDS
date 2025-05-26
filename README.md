# tfds-cli
The free data stack CLI.

The CLI is intended top be a small collection of utilities to
* run docker compose commands on the stack in the relevant order
* provide direct access to the config files for testing and for the config api server
* deploy notebook files to s3
* basic stack operations like inspecting the available stacks and activating a stack
* testing stack health by running a real but minimal operations on each known plugin
* setup tfds for first use

The project is managed in poetry and CLI framework is typer.
