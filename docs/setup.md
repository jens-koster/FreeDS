# FreeDS setup

## create the root repo dir
open a terminal and navigate to it

## install freeds package
### 1. use pipx
becasue it's generally a good idea.

    pipx install freeds

### 2. pip + venv
works fine as well
(todo: code to do this)

## run `freeds init`
It will perform the following actions:


#### Clone the freeds repos:
* the-free-data-stack - the main plugin repo
* freeds-lab-databrickish - sample lab
* freeds-config - config files

#### Create directory structure
    freeds
        config
            configs (symlink to repo)
            locals
        airflow
            dags (symlink)
            plugins (symlink)
            ...
        spark
        data
        ...

#### Create credentials
You'll be asked to choose username and password for airflow, minio S3 etc. These will be stored in local config files.

## Docker setup
### Create docker network
### run `freeds dc build`
### run `freeds dc up`
### run `freeds dc selfcheck --no-nb --no-airflow`
### run `freeds nb deploy`
