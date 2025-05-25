# tfds-cli
The free data stack CLI and python api.

The CLI is intended top be a small collection of utilities to
* run docker compose commands on the stack in the relevant order
* provide direct access to the config files for testing and for the config api server
* deploy notebook files to s3
* basic stack operations like inspecting the available stacks and activating a stack
* testing stack health by running a real but minimal operations on each known plugin
* setup tfds for first use

This package is designed to have no dependecies on the stack and in some places might not work in a tfds container.

There is another package designed for use in notebooks and stack plugins.

The project is managed in poetry and CLI framework is the builtin argparse.

# Development
## PySpark
We keep the package form installing pysparkand assume there will be a pyspark wherever it gets installed. This avoids messing with spark versions, which is a pain.
To maintain and test the spark parts of the package you need to install the spark dependencies in the poetry venv:

    poetry run pip install pyspark==3.5.5
    poetry run pip install delta-spark==3.3.0

You can check the Dockerfile for the tfds Spark plugin to see whet version is currently in development:
https://github.com/jens-koster/the-free-data-stack/blob/main/spark/Dockerfile

## linting

    poetry run pre-commit run --files $(find src -type f)
