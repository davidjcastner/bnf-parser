import setuptools
import requests


def main() -> None:
    '''runs setuptools'''

    # grab the version from the version file
    # ensures that the version is the same as release on github
    with open('version.txt', 'r') as f:
        version = f.read().strip()

    # check that the version is not being used by a previous release

    # use the readme as the long description
    with open('readme.md', 'r') as f:
        long_description = f.read()

    # compile setuptools
    setuptools.setup(
        name='bnf-parser',
        author='David Castner',
        author_email='davidjcastner@gmail.com',
        version=version,
        description='A python library for parsing BNF grammars',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/davidjcastner/bnf-parser',
        packages=setuptools.find_packages(),
        classifiers=[],
        python_requires='>=3.10',
    )


if __name__ == '__main__':
    # main()
    # get the releases from github https://api.github.com/repos/OWNER/REPO/releases
    owner = 'davidjcastner'
    repo = 'bnf-parser'
    url = f'https://api.github.com/repos/{owner}/{repo}/releases'
    response = requests.get(url)
    # print the response
    print(response.json())
