from setuptools import setup, find_packages

setup(
    name='django-erp-os-framework',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'django>=4.2',
    ],
    entry_points={
        'console_scripts': [
            'startproject_with_erp_os=apps.design.management.commands.startproject_with_erp_os:Command.handle',
        ],
    },
)
