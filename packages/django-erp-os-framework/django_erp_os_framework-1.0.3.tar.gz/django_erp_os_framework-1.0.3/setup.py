import os
from setuptools import setup, find_packages

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            if not filename.startswith('.'):  # 排除隐藏文件
                paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('django-erp-os-framework')

setup(
    name='django-erp-os-framework',
    version='1.0.3',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': extra_files},
    install_requires=[
        'django>=4.2',
    ],
    entry_points={
        'console_scripts': [
            'startproject_with_erp_os=design.management.commands.startproject_with_erp_os:Command.handle',
        ],
    },
)
