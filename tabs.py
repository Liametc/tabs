#! /tools/SITE/scripts/python2.7

"""
"""

import argparse
import json
import os
import git

json_folder_mapping_path = os.path.join(
    os.path.dirname(__file__),
    'folder_mapping.json'
)


def get_json_dictionary(json_path):
    """."""
    def unicode_to_str(data):
        if isinstance(data, unicode):
            return str(data)
        if isinstance(data, dict):
            dictionary = {}
            for key, value in data.iteritems():
                dictionary[unicode_to_str(key)] = unicode_to_str(value)
            return dictionary
        return data
    file_ = file(json_path, 'r')
    return json.load(file_, object_hook=unicode_to_str)


class Tabs(object):

    """."""

    tab_template = '{tab} --working-directory={dir} --title={title}'

    def __init__(self, json_dict):
        """."""
        self.mapping = json_dict
        self._command = 'Terminal'

    @property
    def command(self):
        """."""
        return self._command

    def append_command(self, string):
        """."""
        self._command += string

    def build_tab_string(self, name, first_tab=True):
        """
        Build the command for this tab.

        :param mapping: The name and path dictionary
        """
        tab = ' --tab' if not first_tab else ''
        path = self.mapping.get(name)
        if not path:
            print 'Ignoring "{0}": does not exist.'.format(name)
            return
        return self.tab_template.format(
            tab=tab,
            dir=path,
            title=name
        )

    def git_pull(self, repo_path):
        """."""
        try:
            repo = git.repo.base.Repo(repo_path)
        except git.exc.InvalidGitRepositoryError:
            print 'Cannot pull {0}'.format(repo_path)
            return
        name = repo.active_branch.name
        remote = git.remote.Remote(repo, name)
        remote.pull(progress=git.remote.RemoteProgress())

    def run(self, names=[], list_=False, all_=False, pull=False):
        """."""
        if (list_ or not names) and not all_:
            print 'Available Modules:'
            print '\n'.join(self.mapping.keys())
            return
        if all_:
            names = self.mapping.keys()
        if isinstance(names, str):
            names = [names]
        first_line = True
        for name in names:
            line = self.build_tab_string(name, first_line)
            if not line:
                continue
            if pull:
                self.git_pull(self.mapping[name])
            self.append_command(line)
            first_line = False
        os.system(self.command)


def argument_parser(testArgs=None, choices=[]):
    """Create the argument parser."""
    description = (
        'Tabs is a convenient way to open a new Terminal session'
        ' with multiple tabs relating to the modules you desire.'
        ' It will also pull any changes from the git repo for you.'
        )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-m',
        '--modules',
        type=str,
        nargs='*',
        help='Names of the modules you want to open.'
    )
    parser.add_argument(
        '-l',
        '--list-modules',
        action='store_true',
        help='List the available modules.',
    )
    parser.add_argument(
        '-a',
        '--all-modules',
        action='store_true',
        help='Open all the available modules.'
    )
    parser.add_argument(
        '-p',
        '--pull',
        action='store_true',
        help='Pull any changes on the associated git repos'
    )
    return parser.parse_args(testArgs)


if __name__ == '__main__':
    json_dict = get_json_dictionary(json_folder_mapping_path)
    args = argument_parser(choices=json_dict.keys())
    tab = Tabs(json_dict)
    tab.run(args.modules, args.list_modules, args.all_modules, args.pull)
