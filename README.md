# freeds
The free data stack CLI and lib.
The project is managed in `poetry` and uses CLI framework `typer`.

There's a freeds packae on pypi, that might work for you, but we're still in alpha here, you'll probably need to fix some bugs to get things running, so better clone the repo.


Get the "python manager" poetry: https://python-poetry.org/

Preferably using pipx: https://github.com/pypa/pipx

Then, ideally, this should work:

    # get the cli code locally
    git clone https://github.com/jens-koster/FreeDS.git
    # install the cli in dev mode
    cd freeds
    poetry env use 3.11
    poetry install
    # set up freeds in a new freeds root folder
    # I'm aiming to make sure nothing happens outside this folder
    cd ..
    mkdir myfreeds
    cd myfreeds
    # freeds-setup is a cli in freeds and should clone the other repos and install skeleton configs
    freeds-setup
    # freeds dc means call docker-compose in all folders in the current "stack"
    # you can config stacks in the stack.yaml config file,
    # like: postgres, airflow, jupyter server with pyspark, minio S3, spark and redis. To have some spark fun.
    # The one you'll always have to inlcude is the freeds config server,
    # it serves up the config files on http, cause mounting folders in docker is not always doable.

    # so, build all those dockers.
    freeds dc build

    # and fire em up!
    freeds dc up

where it'll all break cause you'll need to edit the configs in local_configs to get anything working.
the minio s3 config is crucial, nothing works without storage.
Also, use the web ui:s to setup credentials for...everything.
Checkout the readme in the-free-data-stack repo (cloned to your "my-freeds” folder) for web gui urls.
One of the things actually provided by freeds is non conflicting ports for the web ui:s...

The setup process is not yet complete and poorly documented.

I'll work on it... but then, Johan, my only user, you've got me on messenger just poke me :-)

oh... I just realised we can have Free Data Stack Haketons.

Haket is one of the last independent pubs in Göteborg, Sweden, serving craft beer with love and friendship (and synth music om Thursdays).

https://www.facebook.com/haketpub/?locale=sv_SE

(I'm handling the rim case of a reader that is not also Johan. (Unlikely but possible))
