from setuptools import setup, find_packages

version = 0.1

setup(
    name='windyr',
    version=version,
    description='windyr',
    long_description='',
    # Get strings for classifiers from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers:
    classifiers=[],
    keywords='',
    author='David Buchmann',
    author_email='davbuchm@cisco.com',
    url='',
    license='',
    packages=find_packages(
        exclude=['ez_setup', 'examples', 'test', 'contrib']),
    package_data={},
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    setup_requires=[],
    dependency_links=[],
    entry_points={},
    scripts=[])
