# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['matrix_content_scanner',
 'matrix_content_scanner.scanner',
 'matrix_content_scanner.servlets',
 'matrix_content_scanner.utils']

package_data = \
{'': ['*'], 'matrix_content_scanner': ['mcs_rust/*']}

install_requires = \
['aiohttp>=3.8.0',
 'attrs>=19.2.0',
 'cachetools>=5.4.0',
 'canonicaljson>=1.6.3',
 'humanfriendly>=10.0',
 'jsonschema>=4.23.0',
 'python-magic>=0.4.15,<0.5',
 'pyyaml>=5.1.1',
 'setuptools_rust>=1.3']

entry_points = \
{'console_scripts': ['matrix-content-scanner = '
                     'matrix_content_scanner.mcs:main']}

setup_kwargs = {
    'name': 'matrix_content_scanner',
    'version': '1.1.0',
    'description': 'A web service for scanning media hosted by a Matrix media repository',
    'long_description': "# Matrix Content Scanner\n\nA web service for scanning media hosted on a Matrix media repository.\n\n## Installation\n\nThis project requires libmagic to be installed on the system. On Debian/Ubuntu:\n\n```commandline\nsudo apt install libmagic1\n```\n\nThen, preferably in a virtual environment, install the Matrix Content Scanner:\n\n```commandline\npip install matrix-content-scanner\n```\n\n## Usage\n\nCopy and edit the [sample configuration file](https://github.com/matrix-org/matrix-content-scanner-python/blob/main/config.sample.yaml).\nEach key is documented in this file.\n\nThen run the content scanner (from within your virtual environment if one was created):\n\n```commandline\npython -m matrix_content_scanner.mcs -c CONFIG_FILE\n```\n\nWhere `CONFIG_FILE` is the path to your configuration file.\n\n## Docker\n\nThis project provides a Docker image to run it, published as\n`vectorim/matrix-content-scanner`.\n\nTo use it, copy the [sample configuration file](/config.sample.yaml) into a dedicated\ndirectory, edit it accordingly with your requirements, and then mount this directory as\n`/data` in the image. Do not forget to also publish the port that the content scanner's\nWeb server is configured to listen on.\n\nFor example, assuming the port for the Web server is `8080`:\n\n```shell\ndocker run -p 8080:8080 -v /path/to/your/config/directory:/data vectorim/matrix-content-scanner\n```\n\n## API\n\nSee [the API documentation](/docs/api.md) for information about how clients are expected\nto interact with the Matrix Content Scanner.\n\n## Migrating from the [legacy Matrix Content Scanner](https://github.com/matrix-org/matrix-content-scanner)\n\nBecause it uses the same APIs and Olm pickle format as the legacy Matrix Content Scanner,\nthis project can be used as a drop-in replacement. The only change (apart from the\ndeployment instructions) is the configuration format:\n\n* the `server` section is renamed `web`\n* `scan.tempDirectory` is renamed `scan.temp_directory`\n* `scan.baseUrl` is renamed `download.base_homeserver_url` (and becomes optional)\n* `scan.doNotCacheExitCodes` is renamed `result_cache.exit_codes_to_ignore`\n* `scan.directDownload` is removed. Direct download always happens when `download.base_homeserver_url`\n  is absent from the configuration file, and setting a value for it will always cause files to be\n  downloaded from the server configured.\n* `proxy` is renamed `download.proxy`\n* `middleware.encryptedBody.pickleKey` is renamed `crypto.pickle_key`\n* `middleware.encryptedBody.picklePath` is renamed `crypto.pickle_path`\n* `acceptedMimeType` is renamed `scan.allowed_mimetypes`\n* `requestHeader` is renamed `download.additional_headers` and turned into a dictionary.\n\nNote that the format of the cryptographic pickle file and key are compatible between\nthis project and the legacy Matrix Content Scanner. If no file exist at that path one will\nbe created automatically.\n\n## Development\n\nIn a virtual environment with poetry (>=1.8.3) installed, run\n```shell\npoetry install\n```\n\nTo run the unit tests, you can use:\n```shell\ntox -e py\n```\n\nTo run the linters and `mypy` type checker, use `./scripts-dev/lint.sh`.\n\n\n## Releasing\n\nThe exact steps for releasing will vary; but this is an approach taken by the\nSynapse developers (assuming a Unix-like shell):\n\n 1. Set a shell variable to the version you are releasing (this just makes\n    subsequent steps easier):\n    ```shell\n    version=X.Y.Z\n    ```\n\n 2. Update `setup.cfg` so that the `version` is correct.\n\n 3. Stage the changed files and commit.\n    ```shell\n    git add -u\n    git commit -m v$version -n\n    ```\n\n 4. Push your changes.\n    ```shell\n    git push\n    ```\n\n 5. When ready, create a signed tag for the release:\n    ```shell\n    git tag -s v$version\n    ```\n    Base the tag message on the changelog.\n\n 6. Push the tag.\n    ```shell\n    git push origin tag v$version\n    ```\n\n 7. Create a *release*, based on the tag you just pushed, on GitHub or GitLab.\n\n 8. Create a source distribution and upload it to PyPI:\n    ```shell\n    python -m build\n    twine upload dist/matrix_content_scanner-$version*\n    ```\n",
    'author': 'Element Backend Team',
    'author_email': 'team-backend-synapse@element.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10.0,<4.0.0',
}
from build_rust import *
build(setup_kwargs)

setup(**setup_kwargs)
