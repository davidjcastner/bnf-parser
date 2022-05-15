# collection of tests for the package itself
# keeps the package organized

import os
import re
import requests

OWNER = 'davidjcastner'
REPO = 'bnf-parser'


def test_version_syntax() -> None:
    '''tests if the string in the version file matches the correct syntax'''
    with open('version.txt', 'r') as f:
        version = f.read()
    assert re.match(r'^\d+\.\d+\.\d+$', version)


def _get_current_version() -> str:
    '''gets the current version from the version file'''
    assert os.path.isfile('version.txt'), 'Version file does not exist'
    with open('version.txt', 'r') as f:
        version = f.read()
    return version


def _get_previous_releases() -> list:
    '''gets the previous releases from github'''
    url = f'https://api.github.com/repos/{OWNER}/{REPO}/releases'
    response = requests.get(url)
    releases = response.json()
    release_tags = [release['tag_name'] for release in releases]
    return release_tags


def _get_version_parts(version: str) -> tuple[int, int, int]:
    '''splits the version into its parts (major, minor, patch)'''
    parts = version.split('.')
    assert len(parts) == 3, 'Version must be in the format major.minor.patch'
    return int(parts[0]), int(parts[1]), int(parts[2])


def test_is_sequential_version() -> None:
    '''checks if the version is not used by a previous release and that it is sequential'''
    # get the current version from the version file
    version = _get_current_version()
    # get the previous releases from github
    previous_releases = _get_previous_releases()
    # if there are no previous releases, then the version is valid and no tests are needed
    if len(previous_releases) == 0:
        return
    # check if the version is not used by a previous release
    assert version not in previous_releases, f'Version {version} is already used by a previous release'
    # check if the version is sequential
    major, minor, patch = _get_version_parts(version)
    # check that each is greater than or equal to zero
    assert major >= 0, 'Major version must be greater than or equal to zero'
    assert minor >= 0, 'Minor version must be greater than or equal to zero'
    assert patch >= 0, 'Patch version must be greater than or equal to zero'
    # transform the previous releases into tuples of (major, minor, patch)
    previous_releases = [_get_version_parts(release) for release in previous_releases]
    previous_releases.sort(reverse=True)
    previous_major, previous_minor, previous_patch = previous_releases[0]
    # check major version
    # if the major version is greater than the previous major version, then the version is valid
    if major > previous_major:
        return
    # if the major version is less than the previous major version, then the version is invalid
    assert major == previous_major, f'Version {version} is not sequential'
    # check minor version
    # if the minor version is greater than the previous minor version, then the version is valid
    if minor > previous_minor:
        return
    # if the minor version is less than the previous minor version, then the version is invalid
    assert minor == previous_minor, f'Version {version} is not sequential'
    # check patch version
    # if the patch version is greater than the previous patch version, then the version is valid
    # if at this point, than the patch is the determining factor for sequentiality
    assert patch > previous_patch, f'Version {version} is not sequential'


def test_is_changelog() -> None:
    '''checks if the changelog file is not empty'''
    # get the current version from the version file
    version = _get_current_version()
    changelog = os.path.join('docs', 'changelog', f'{version}.txt')
    assert os.path.isfile(changelog), f'Changelog for version {version} does not exist, missing {changelog}'
    # check that the file is not empty
    with open(changelog, 'r') as f:
        text = f.read().strip()
    assert len(text) > 0, f'Changelog for version {version} is empty'
