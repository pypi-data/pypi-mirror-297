from setuptools import setup, find_packages

setup(
    name='django-erp-os-framework',
    version='1.0.4',
    packages=find_packages(where='django_erp_os_framework'),    include_package_data=True,
    package_data={'django_erp_os_framework': ['*', '**/*']},
    install_requires=[
        'django>=4.2',
    ],
    entry_points={
        'console_scripts': [
            'startproject_with_erp_os=design.management.commands.startproject_with_erp_os:Command.handle',
        ],
    },
)
