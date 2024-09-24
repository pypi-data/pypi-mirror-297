
from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
  name='latlongtimezone_api',
  version='0.1.8',
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'An API wrapper for Scrappey.com written in Python (cloudflare bypass & solver)',   # Give a short description about your library
  author = 'dormic97',                   # Type in your name
  author_email = 'crozz-boy@hotmail.com',      # Type in your E-Mail
  url = 'https://github.com/pim97/requests-lat-long-timezone-locale-ip-api',   # Provide either the link to your github or to your website
  keywords=['ip', 'ip-api', 'ip-geolocation', 'ip-location', 'ip-address', 'ip-locator', 'ip-tracker', 'ip-geocoding', 'ip-api-geolocation', 'ip-api-location', 'ip-api-address', 'ip-api-locator', 'ip-api-tracker', 'ip-api-geocoding'],
  long_description=long_description,
  long_description_content_type='text/markdown',
  install_requires=[            # I get to this in a second
          'requests'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)