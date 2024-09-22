### PyEnvloaderMeta - metaclass for automatically loading and converting environment variables into class attributes.

- It simplifies the process of managing environment variables by leveraging type annotations and the `python-dotenv` package.
- Features - Automatically loads environment variables from a `.env` file.
- Converts environment variables to specified types using type annotations.
- Raises errors if required environment variables are missing or cannot be converted.

## Installation You can install `pyenvloader` from PyPI using pip:

`pip install pyenvloadermeta`

## Usage

To use `pyenvloadermeta`, define a class with `pyenvloadermeta.EnvLoaderMeta` as the metaclass and specify the environment variables with type annotations. Here’s an example:

1. Create a `.env` file in your project directory:

.env

```
API_ID=123456
API_HASH=dfdafdfasdff
BOT_TOKEN=fasdfasfdafsd
OZ=11.2
POKEMON=["Pikachu", "Raichu's"]
```

2. Define your class using `EnvLoaderMeta`:

```
from pyenvloadermeta import EnvLoaderMeta

class Env(metaclass=EnvLoaderMeta):
	API_ID: int
	API_HASH: str
	BOT_TOKEN: str
	OZ: float
	POKEMON: list[str]
```

3. Access the environment variables as class attributes:

```
print(Env.API_ID)
print(Env.API_HASH)
print(Env.BOT_TOKEN)
print(Env.OZ)
print(Env.POKEMON)
```
