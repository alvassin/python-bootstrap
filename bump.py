#!/usr/bin/env python
import logging
from os import environ
from subprocess import check_output


log = logging.getLogger('' if __name__ == '__main__' else __name__)


VERSION_FILE_TEMPLATE = '''
""" This file is automatically generated by distutils. """

# Follow PEP-0396 rationale
version_info = ({major}, {minor}, {commits}, '{commit_hash}')
__version__ = '{major}.{minor}.{commits}'
'''


def git_version():
    # construct minimal environment
    env = {
        'LANG': 'C',
        'LANGUAGE': 'C',
        'LC_ALL': 'C',
        'PATH': environ.get('PATH'),
        'SYSTEMROOT': environ.get('SYSTEMROOT'),
    }

    env = {k: v for k, v in env.items() if v is not None}

    try:
        output = check_output(['git', 'describe', '--long'], env=env).decode()
    except OSError:
        output = 'v0.0.0-g'

    version, commits, commit_hash = output.lstrip('v').strip().rsplit('-', 2)

    return (
        tuple(map(int, version.split('.'))),
        int(commits),
        commit_hash,
    )


def update_version(filename='version.py'):
    version, commits, commit_hash = git_version()

    major, minor = version

    content = VERSION_FILE_TEMPLATE.format(
        major=major,
        minor=minor,
        commits=commits,
        commit_hash=commit_hash,
    )

    log.info(
        'Writing version %s.%s-%s-%s to %r',
        major, minor, commits, commit_hash,
        filename,
    )

    with open(filename, 'w+') as version_file:
        version_file.write(content.lstrip())


if __name__ == '__main__':
    # Just for manual testing
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('version_file')
    arguments = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    update_version(arguments.version_file)
