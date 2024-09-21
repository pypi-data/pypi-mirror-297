from setuptools import setup, find_packages

setup(
    name='django-erp-os-framework',
    version='1.0.5',
    packages=find_packages(where='django-erp-os-framework'),
    include_package_data=True,
    package_data={'django-erp-os-framework': ['*', '**/*']},
    install_requires=[
        'django>=4.2',
    ],
    entry_points={
        'console_scripts': [
            'startproject_with_erp_os=design.management.commands.startproject_with_erp_os:Command.handle',
        ],
    },
)
