# ScrapeBillTrack50

[![Lint Code](https://github.com/aperloff/ScrapeBillTrack50/actions/workflows/lint.yml/badge.svg)](https://github.com/aperloff/ScrapeBillTrack50/actions/workflows/lint.yml) [![Deploy images](https://github.com/aperloff/ScrapeBillTrack50/actions/workflows/deploy_images.yml/badge.svg)](https://github.com/aperloff/ScrapeBillTrack50/actions/workflows/deploy_images.yml)

For each legislator in a list, do a [Google](https://www.google.com/) search for the relevant [Bill Track 50](https://www.billtrack50.com/) webpage and then search that webpage for specific information.

*Note: Right now the code is setup only to return the scheduler information for each legislator.*

To report a bug or request a feature, please [file an issue](https://github.com/aperloff/ScrapeBillTrack50/issues/new/choose).

Table of Contents
=================
<!-- MarkdownTOC autolink="true" -->

- [Installation](#installation)
  - [Local Installation](#local-installation)
  - [Available Docker Images](#available-docker-images)
- [Command Line Interface](#command-line-interface)
  - [Basic example](#basic-example)
  - [Options](#options)
- [Using Docker](#using-docker)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
  - [Unit Testing](#unit-testing)
  - [Linting](#linting)

<!-- /MarkdownTOC -->

## Installation

### Local Installation
If you wish to install the dependencies yourself and only wish to checkout the code and download the needed input data, then you may use the following commands.

```bash
git clone git@github.com:aperloff/ScrapeBillTrack50.git
```

### Available Docker Images

If you'd rather use a clean environment, there is an available set of Docker image ([aperloff/scrapebilltrack50](https://hub.docker.com/r/aperloff/scrapebilltrack50)) with the following tags:

  - `latest`: Contains all of the necessary dependencies and the ScrapeBillTrack50 code.
  
Further information about using these images will be given below (see [Using Docker](#using-docker)).


## Command Line Interface

### Basic example

```python
python3 ScrapeBillTrack50.py -C configs/assignments.py
```

The output will be an image file.

### Options

The command line options available are:

  - `-d, --debug`: Shows some extra information in order to debug this program (default = False)
  - `-l, --legislators [files]`: A list of the legislator names in the format '<first> <last>'

## Using Docker

There are a few workflows available when using the Docker images:

1. You may choose to use the `latest` image as a clean environment.
2. An alternative mode has you checkout the code locally, but use one of the Docker images to provide the necessary dependencies. In this case, the code within the image will automatically be replaced by your local version using a bind mount. This method is most useful for people wishing to develop a new feature for the repository, but who want to avoid installing the dependencies on their local machine. The resulting images will be copied back to the host machine. To run in this mode, a helper script has been developed to wrap up all of the Docker complexities. Simply run:

    ```bash
    .docker/run.sh -C configs/assignments.py
    ```
    **Note**: To use this running mode, you will need to have permission to bind mount the local directory and the local user will need permission to write to that directory as well. This is typically not a problem unless the repository has been checked out inside a restricted area of the operating system or the permissions on the directory have been changed.

## Dependencies

Required dependencies:
  - `Python 3`
  - [`magiconfig`](https://pypi.org/project/magiconfig/) ([GitHub](https://github.com/kpedro88/magiconfig/)): Used to read Python configuration files.
    - Can be installed using the command `pip3 install --no-cache-dir magiconfig`
  googlesearch-python
  urllib3
  beautifulsoup4

There is a script available to make sure all of the needed dependencies are installed:
```bash
python3 check_for_dependencies.py
```

Optional dependencies:
  - [`PyLint`](https://pylint.org/) ([GitHub](https://github.com/PyCQA/pylint), [PyPI](https://pypi.org/project/pylint/)): Used for linting Python modules.
  - [`pytest`](https://docs.pytest.org/en/stable/) ([GitHub](https://github.com/pytest-dev/pytest/), [PyPI](https://pypi.org/project/pytest/)): Used for unit testing Python modules.

## Contributing

Pull requests are welcome, but please submit a proposal issue first, as the library is in active development.

Current maintainers:

  - Alexx Perloff

### Unit Testing

Unit testing is performed using [`PyTest`](https://docs.pytest.org/en/stable/). You are of course allowed to install this programs locally. However, a shell script has been setup to make this procedure as easy as possible.

To run the python unit/integration tests, you will need to have PyTest installed. To create a local virtual environment with PyTest installed, use the following commands from within the repository's base directory:

```bash
./test/pytest_control.sh -s
```

You only have to run that command when setting up the virtual environment the first time. You can then run the tests by using the command:

```bash
./test/pytest_control.sh
```

You should see an output similar to:

```bash
======================================================== test session starts ========================================================
platform darwin -- Python 3.9.10, pytest-7.0.1, pluggy-1.0.0
rootdir: <path to ScrapeBillTrack50>
collected 2 items

test/test.py ..                                                                                                               [100%]

======================================================== 2 passed in 13.34s =========================================================
```

You can pass addition options to PyTest using the -o flag. For example, you could run the following command to increase the verbosity of PyTest:

```bash
./test/pytest_control.sh -o '--verbosity=3'
```

Other helpful pytest options include:

  - `-rP`: To see the output of successful tests. This is necessary because by default all of the output from the various tests is captured by PyTest.
  - `-rx`: To see the output of failed tests (default).
  - `-k <testname>`: Will limit the tests run to just the test(s) specified. The `<testname>` can be a class of tests or the name of a specific unit test function.

To remove the virtual environment use the command:

```bash
./test/pytest_control.sh -r
```

which will simply remove the `test/venv` directory.


### Linting

Linting is done using [`PyLint`](https://pylint.org/). The continuous integration jobs on GitHub will run these linters as part of the PR validation process. You may as well run them in advance in order to shorten the code review cycle. PyLint can be run as part of the Python unit testing process using the command:

```bash
test/pytest_control.sh -l
```
