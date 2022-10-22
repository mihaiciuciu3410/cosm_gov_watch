import sys
import tomli


def load_chains():
    try:
        with open("chains.toml", mode="rb") as chains_file:
            chains = tomli.load(chains_file)
    except IOError:
        sys.exit("Can't load chains.toml.")

    return chains
