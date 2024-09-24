from distutils.core import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='latlongtimezone_api',
    version='0.1.91',
    license='MIT',
    description='Get timezone, locale, and location based on the IP address to use in your requests',
    author='dormic97',
    author_email='crozz-boy@hotmail.com',
    url='https://github.com/pim97/requests-lat-long-timezone-locale-ip-api',
    keywords=['ip', 'ip-api', 'ip-geolocation', 'ip-location', 'ip-address', 'ip-locator', 'ip-tracker', 'ip-geocoding', 'ip-api-geolocation', 'ip-api-location', 'ip-api-address', 'ip-api-locator', 'ip-api-tracker', 'ip-api-geocoding'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'redis',
        'python-dotenv'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=['geolocation'],
)