from setuptools import setup, find_packages

setup(
    name='incident-framework',
    version='0.1.0',
    description='Distributed Incident Management & Observability CLI',
    author='Your Name',
    packages=find_packages(where='cli'),
    package_dir={'': 'cli'},
    install_requires=[
        'click>=8.1.0',
        'rich>=13.0.0',
        'pyyaml>=6.0',
        'python-dateutil>=2.8.2',
    ],
    entry_points={
        'console_scripts': [
            'incident-framework=incident_cli:cli',
        ],
    },
    include_package_data=True,
) 