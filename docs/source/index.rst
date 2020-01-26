.. lambda-layer documentation master file
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

lambda-layer
============

Create AWS Lambda layers for your AWS Lambda python functions!

What are Lambda Layers?
-----------------------

Good question.  Let's ask the
`AWS documentation <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)>`_

   You can configure your Lambda function to pull in additional code and
   content in the form of layers. A layer is a ZIP archive that contains
   libraries, a custom runtime, or other dependencies. With layers, you can
   use libraries in your function without needing to include them in your
   deployment package.

What is `lambda-layer`?
-----------------------
`lambda-layer` is a command-line application you can use to automate the
creation of layers for your python Lambda functions.

Installation
------------

Take a look at :ref:`getting_started_installing`.


Running the CLI
---------------

``lambda-layer`` features a command-line interface (CLI) based on
`Click <https://click.palletsprojects.com/>`_. You can use the ``--help`` flag
to get context help.

Getting Help
------------

.. code-block:: sh

   lambda-layer --help

.. code-block:: coq

   Usage: lambda-layer [OPTIONS] COMMAND [ARGS]...

     Run lambda-layer.

   Options:
     -v, --verbose  Enable verbose output.
     --help         Show this message and exit.

   Commands:
     package  Create configured packages.
     version  Get the library version.
   Creating Packages

Most of the time you’ll probably want to use the ``package`` subcommand.

.. code-block:: sh

   lambda-layer package --help

.. code-block:: coq

   Usage: lambda-layer package [OPTIONS]

     Create configured packages.

   Options:
     -c, --config PATH
     --help             Show this message and exit.

What's Next?
------------

Now that you know how to run the application, you'll want to create a
:ref:`configuration file <lambda_layer_toml>` to describe your packages.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started
   lambda_layer_toml
   api
   development
   requirements



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
