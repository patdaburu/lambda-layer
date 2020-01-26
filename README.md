# lambda-layer

Create AWS Lambda layers for your AWS Lambda python functions!

## What are AWS Lambda Layers?

Good question.  Let's ask the [AWS documentation](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html).
> You can configure your Lambda function to pull in additional code and content in the form of layers. A layer is a ZIP archive that contains libraries, a custom runtime, or other dependencies. With layers, you can use libraries in your function without needing to include them in your deployment package.

## What is `lambda-layer`?

`lambda-layer` is a command-line application you can use to automate the creation of layers for your python Lambda functions.

## Considerations

Thank you for checking out this project.  Please be aware that it's still early days and, at present, the application uses the `bash` shell to do its work.  I am hoping to add support for Windows in the future.

## Installation

You can install `lamba-layer` using `pip`.

```sh
pip install lambda-layer
```

## Running the CLI

`lambda-layer` features a command-line interface (CLI) based on [Click](http://click.pocoo.org/5/).  You can use the `--help` flag to get context help.

### Getting Help
```sh
lambda-layer --help
```
```sh
Usage: lambda-layer [OPTIONS] COMMAND [ARGS]...

  Run lambda-layer.

Options:
  -v, --verbose  Enable verbose output.
  --help         Show this message and exit.

Commands:
  package  Create configured packages.
  version  Get the library version.
```

### Creating Packages

Most of the time you'll probably want to use the `package` subcommand.

```sh
lambda-layer package --help
```
```sh
Usage: lambda-layer package [OPTIONS]

  Create configured packages.

Options:
  -c, --config PATH
  --help             Show this message and exit.
```

## Package Configuration

`lambda-layer` uses configuration files written in [TOML](https://github.com/toml-lang/toml) that describe the Lambda Layer packages you want to create.

### Configuration Files

By default, when you run ``lambda-layer`` the application will look for
a file called ``.lambda-layer.toml`` in the current working directory.

#### Layers

A single configuration file can produce many Lambda layer packages.  Each layer that you want to build within a single run should be defined within an array called "layers".

##### name

This is the name of the layer.  It will be part of the final package archive's
name.

##### version

This is the layer package version.  it will be part of the final package
archive's name.

##### packages

List the python packages you want to include in your layer package just as
you would in a
`requirements <https://pip.pypa.io/en/stable/user_guide/#requirements-files>`_
file.


#### Example

```ini
[[layers]]
name = "neural-networking"
version = "0.0.1"
packages = [
    'keras==2.3.1',
    'requests'
]

[[layers]]
name = "number-cruncher"
version = "1.1.0"
packages = [
    'matplotlib',
    'numpy'
]
```


## Project Features

* [lambda_layer](http://lambda-layer.readthedocs.io/)
* a starter [Click](http://click.pocoo.org/5/) command-line application
* automated unit tests you can run with [pytest](https://docs.pytest.org/en/latest/)
* a [Sphinx](http://www.sphinx-doc.org/en/master/) documentation project

## Getting Started

The project's documentation contains a section to help you
[get started](https://lambda-layer.readthedocs.io/en/latest/getting_started.html) as a developer or
user of the library.

## Development Prerequisites

If you're going to be working in the code (rather than just using the library), you'll want a few utilities.

* [GNU Make](https://www.gnu.org/software/make/)
* [Pandoc](https://pandoc.org/)

## Resources

Below are some handy resource links.

* [Project Documentation](http://lambda-layer.readthedocs.io/)
* [Click](http://click.pocoo.org/5/) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.


## Authors

* **Pat Daburu** - *Initial work* - [github](https://github.com/patdaburu)

See also the list of [contributors](https://github.com/patdaburu/lambda_layer/contributors) who participated in this project.

## LicenseMIT License

Copyright (c) patdaburu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.