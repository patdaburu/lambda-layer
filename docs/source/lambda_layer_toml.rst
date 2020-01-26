.. _lambda_layer_toml:

.. toctree::
    :glob:

********************
Configuration Files
********************

``lambda-layer`` configuration files are written in
`toml <https://github.com/toml-lang/toml>`_.

By default, when you run ``lambda-layer`` the application will look for
a file called ``.lambda-layer.toml`` in the current directory (though you
can supply an alternate path if you like).

======
Layers
======

A single configuration file can produce many
`AWS Lambda Layer <https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html>`_
packages.  Each layer that you want to build within a single run should be
defined within an array called "layers".

name
====

This is the name of the layer.  It will be part of the final package archive's
name.

version
=======

This is the layer package version.  it will be part of the final package
archive's name.

packages
========

List the python packages you want to include in your layer package just as
you would in a
`requirements <https://pip.pypa.io/en/stable/user_guide/#requirements-files>`_
file.


=======
Example
=======

.. code-block:: ini

    [[layers]]
    name = "my-first-layer"
    version = "0.0.1"
    packages = [
        'keras==2.3.1',
        'requests'
    ]

    [[layers]]
    name = "another-layer"
    version = "1.1.0"
    packages = [
        'matplotlib',
        'numpy'
    ]

