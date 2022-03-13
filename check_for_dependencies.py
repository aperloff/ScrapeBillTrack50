#!/bin/env python3

"""This program checks that the needed dependencies are installed on the host machine. It will check dependencies
installed explicitly by pip, those which are bundled with other programs (not explicitly tracked by pip), and
some system dependencies.

Attributes
----------
pip_dependencies : dict
    a set of pip tracked dependencies and some associated dependencies
try_dependencies : list
    a list of dependencies not explicitly tracked by pip, but which are nevertheless used by this module
system_dependencies : list
    a list of system-level, non-python dependencies which are needed for some of the other modules to work

Functions
---------
is_tool(name)
    Checks if `name` is within PATH and is marked as executable
check_for_dependencies()
    Runs the checks for all of the dependencies
"""

import importlib
from shutil import which
import pkg_resources

pip_dependencies = {
    "urllib3" : ["requests"],
    "magiconfig" : [],
    "beautifulsoup4" : [],
    "googlesearch-python" : [],
}

try_dependencies = []
system_dependencies = []

def is_tool(name):
    """Check whether `name` is on PATH and marked as executable.

    Suggested from: https://stackoverflow.com/questions/11210104/check-if-a-program-exists-from-a-python-script
    """
    return which(name) is not None

def check_pip_dependencies(dependency_dict):
    """Checks for the pip-installed dependencies.

    Parameters
    ----------
    dependency_dict : dict
        The keys of the dictionary contain the major dependencies and the values contain a list of the sub-dependencies

    Returns
    -------
    list
        A list of the missing packages
    """

    # pylint: disable=E1133
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted([f"{i.key}" for i in installed_packages])

    missing = []
    for dependency, subdependencies in dependency_dict.items():
        print(f"Checking for {dependency} ... ", end="")
        if dependency not in installed_packages_list:
            missing.append(dependency)
            print("MISSING")
        else:
            print("FOUND")

        for subdependency in subdependencies:
            print(f"\tChecking for {subdependency} ... ", end="")
            if subdependency not in installed_packages_list:
                missing.append(subdependency)
                print("MISSING")
            else:
                print("FOUND")
    return missing

def check_try_dependencies(dependency_list):
    """Checks for the python dependencies not tracked by pip.

    Parameters
    ----------
    dependency_list : list
        The list of modules to try to import to see if they are installed

    Returns
    -------
    list
        A list of the missing modules
    """

    missing = []
    for dependency in dependency_list:
        print(f"Checking for {dependency} ... ", end="")
        try:
            importlib.import_module(dependency)
        except ImportError:
            missing.append(dependency)
            print("MISSING")
        else:
            print("FOUND")
    return missing

def check_system_dependencies(dependency_list):
    """Checks for the system dependencies.

    Parameters
    ----------
    dependency_list : list
        The list of modules to look for

    Returns
    -------
    list
        A list of the missing modules
    """

    missing = []
    for dependency in dependency_list:
        print(f"Checking for {dependency} ... ", end="")
        if not is_tool(dependency):
            missing.append(dependency)
            print("MISSING")
        else:
            print("FOUND")
    return missing

def check_for_dependencies():
    """Checks whether or not the dependencies are installed

    Raises
    ------
    ModuleNotFoundError
        If the number of missing packages isn't zero

    Returns
    -------
    list
        The number of missing packages

    Suggested from: https://www.activestate.com/resources/quick-reads/how-to-list-installed-python-packages/
    """

    missing_pip = check_pip_dependencies(pip_dependencies)
    missing_import = check_try_dependencies(try_dependencies)
    missing_system = check_system_dependencies(system_dependencies)

    n_missing = len(missing_pip) + len(missing_import) + len(missing_system)
    if n_missing > 0:
        raise ModuleNotFoundError("There are missing dependencies!")

    print("\nAll dependencies installed!")

    return n_missing

if __name__ == "__main__":
    check_for_dependencies()
