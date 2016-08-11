# ------------------------------------------------------------------------------
# Originally code from: http://gitlab.com/aurelien-lourot/importdir
# Extended to treat modules more like plugins.
# ------------------------------------------------------------------------------

import os
import re
import sys

# ------------------------------------------------------------------------------
# Interface
# ------------------------------------------------------------------------------


def do(path, env, plugindb):
    """ Imports all modules residing directly in directory "path" into the
        provided environment (usually the callers environment). A typical call:
        importdir.do("example_dir", globals())
    """
    __do(path, env, plugindb)

# -----------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------

# File name of a module:
__module_file_regexp = "(.+)\.py(c?)$"


def __get_module_names_in_dir(path):
    """ Returns a set of all module names residing directly in directory "path".
    """
    result = set()

    # Looks for all python files in the directory (not recursively)
    #   and adds their names to result:
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            regexp_result = re.search(__module_file_regexp, entry)
            if regexp_result:  # is a module file name
                result.add(regexp_result.groups()[0])
    return result


def __do(path, env, plugindb):
    """ Implements do().
    """
    sys.path.append(path)  # adds provided directory to list we can import from
    for module_name in sorted(__get_module_names_in_dir(path)):
        plugin = env[module_name] = __import__(module_name)
        callplugin = getattr(plugin, 'setup')
        # The setup function will return the values we care about.
        pluginspecs = callplugin()
        if 'cooldown' not in pluginspecs:
            pluginspecs['cooldown'] = 60
        # The result is a tuple that contains all our required data.
        plugindb.insert({'name': module_name,
                         'act_on_event': pluginspecs['act_on_event'],
                         'regex': pluginspecs['regex'],
                         'cooldown': pluginspecs['cooldown']})
