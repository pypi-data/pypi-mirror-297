`` # pyenvloader  `pyenvloader` is a Python package that provides a metaclass for automatically loading and converting environment variables into class attributes. It simplifies the process of managing environment variables by leveraging type annotations and the `python-dotenv` package.  ## Features  - Automatically loads environment variables from a `.env` file. - Converts environment variables to specified types using type annotations. - Raises errors if required environment variables are missing or cannot be converted.  ## Installation  You can install `pyenvloader` from PyPI using pip:  ```bash pip install pyenvloader ``

## Usage

To use `pyenvloader`, define a class with `pyenvloader.EnvLoader` as the metaclass and specify the environment variables with type annotations. Here’s an example:

1.  Create a `.env` file in your project directory:

    env

    `API_ID=123456 API_HASH=your_api_hash BOT_TOKEN=your_bot_token OZ=11.2`

2.  Define your class using `EnvLoader`:

    python

    `from pyenvloader import EnvLoader  class Env(metaclass=EnvLoader):     API_ID: int     API_HASH: str     BOT_TOKEN: str     OZ: float`

3.  Access the environment variables as class attributes:

    python

    `print(Env.API_ID)      # 123456 print(Env.API_HASH)    # your_api_hash print(Env.BOT_TOKEN)   # your_bot_token print(Env.OZ)          # 11.2`

## Contributing

If you want to contribute to `pyenvloader`, you can:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature-branch`).
3.  Make your changes.
4.  Commit your changes (`git commit -am 'Add new feature'`).
5.  Push to the branch (`git push origin feature-branch`).
6.  Create a new Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or issues, please contact Praveen.

`### Key Sections:  - **Features**: Summarizes what the package does. - **Installation**: Instructions for installing the package. - **Usage**: Examples of how to use the package. - **Contributing**: Guidelines for contributing to the project. - **License**: License information. - **Contact**: Contact information for further queries.  Feel free to adjust the content based on any additional features or specific details about your package!`
