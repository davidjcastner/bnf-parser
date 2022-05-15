import os
import setuptools
import requests


OWNER = 'davidjcastner'
REPO = 'bnf-parser'


def get_previous_releases() -> list:
    '''gets the previous releases from github'''
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/releases'
    response = requests.get(url)
    releases = response.json()
    release_tags = [release['tag_name'] for release in releases]
    return release_tags


def get_version_parts(version: str) -> tuple[int, int, int]:
    '''splits the version into its parts (major, minor, patch)'''
    parts = version.split('.')
    assert len(parts) == 3, 'Version must be in the format major.minor.patch'
    return int(parts[0]), int(parts[1]), int(parts[2])


def is_valid_version(version: str) -> bool:
    '''checks if the version is not used by a previous release and that it is sequential'''
    previous_releases = get_previous_releases()
    # if there are no previous releases, then the version is valid
    if len(previous_releases) == 0:
        return True
    # check if the version is not used by a previous release
    if version in previous_releases:
        return False
    # check if the version is sequential
    major, minor, patch = get_version_parts(version)
    previous_releases = [get_version_parts(release) for release in previous_releases]
    previous_releases.sort(reverse=True)
    previous_major, previous_minor, previous_patch = previous_releases[0]
    # check major version
    if major > previous_major:
        return True
    if major < previous_major:
        return False
    # check minor version
    if minor > previous_minor:
        return True
    if minor < previous_minor:
        return False
    # check patch version
    return patch > previous_patch


def is_valid_changelog(version: str) -> bool:
    '''checks if the changelog notes for the version are present'''
    filename = f'{version}.txt'
    full_path = os.path.join('docs', 'changelog', filename)
    return os.path.exists(full_path)


def main() -> None:
    '''runs setuptools'''

    # grab the version from the version file
    # ensures that the version is the same as release on github
    with open('version.txt', 'r') as f:
        version = f.read().strip()

    # check that the version is not being used by a previous release
    if not is_valid_version(version):
        raise ValueError(f'Version {version} is already in use or not sequential')

    # check for change log notes
    if not is_valid_changelog(version):
        raise ValueError('No changelog notes for this version')

    # use the readme as the long description
    with open('readme.md', 'r') as f:
        long_description = f.read()

    # compile setuptools
    setuptools.setup(
        name=REPO,
        author='David Castner',
        author_email='davidjcastner@gmail.com',
        version=version,
        description='A python library for parsing BNF grammars',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url=f'https://github.com/{OWNER}/{REPO}',
        packages=setuptools.find_packages(),
        classifiers=[],
        python_requires='>=3.10',
    )
