from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='requests-lat-long-timezone-locale-ip-api',  # Replace with your package name
    version='0.1.1',  # Replace with your package version
    author='dormic97',
    author_email='crozz-boy@hotmail.com',
    description='Get timezone, locale, and location from IP address to use in your requests',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pim97/requests-lat-long-timezone-locale-ip-api.git',  # Replace with your repo URL
    packages=find_packages(),
    keywords=['ip', 'ip-api', 'ip-geolocation', 'ip-location', 'ip-address', 'ip-locator', 'ip-tracker', 'ip-geocoding', 'ip-api-geolocation', 'ip-api-location', 'ip-api-address', 'ip-api-locator', 'ip-api-tracker', 'ip-api-geocoding', 'ip-api-geolocation', 'ip-api-location', 'ip-api-address', 'ip-api-locator', 'ip-api-tracker', 'ip-api-geocoding'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Replace with your license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Replace with your required Python version
    install_requires=[
        'requests',
        'redis',
        'python-dotenv'
    ],
)