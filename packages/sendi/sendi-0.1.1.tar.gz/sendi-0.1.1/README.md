# Sendi

Sendi is just another xmppsend script.
Sendi is based on python slixmpp library and support fews modern features like HTTP Upload and Omemo.

## Dev install

Install pyinvoke and then:

```shell
pip install invoke
invoke init
```

Run python code:

```shell
invoke build
# Typer Cli
rye run sendi

CONFIG_NAME="user"
CONFIG_PATH="config.toml"
TARGET="receiver@localhost"

rye run sendi $CONFIG_NAME $TARGET --config-file=$CONFIG_PATH --message="Ping !" --file-path=tests/test_image.jpg
```

## Install Using Container(podman):

```shell
CONFIG_NAME="user"
CONFIG_PATH="config.toml"
TARGET="receiver@localhost"
invoke build
invoke build-container
podman run -v $PWD:/mnt  localhost/sendi  $CONFIG_NAME $TARGET --config-file=/mnt/$CONFIG_PATH --message="Ping !" --file-path=/mnt/tests/test_image.jpg
```

# Experimental: Install as Deb using Wheel2deb.

Use this method only if you know what you are doing, this [may break your system](https://wiki.debian.org/fr/DontBreakDebian).
I tested this only in debian-bookworm.

```
invoke init-deb
invoke build-deb
cd deb
ls -la *.deb
# Only 4 lib from the huge number of generated lib are require to make sendi work.
# I prefer to keep debian as standard as possible.
sudo apt install ./python3-twomemo_1.0.4-1~w2d0_all.deb ./python3-oldmemo_1.0.4-1~w2d0_all.deb
sudo apt install ./python3-slixmpp-omemo_1.0.0-1~w2d0_all.deb
sudo apt install ./python3-sendi_0.1.0-1~w2d0_all.deb
```

## FAQ ?

- Why this name, sendi ?

It's an esperanto verb: https://en.wiktionary.org/wiki/sendi

- Why AGPL v3 ?

I used slixmpp, slixmpp-omemo and reuse some part of the old apprise xmpp plugin which as been dropped.
The license rule make possible to release all the stuff only under the agplv3 license which is the slixmpp-omemo one.
