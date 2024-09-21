from setuptools import setup, find_packages
import platform

common_requires = [
    'requests==2.28.2',
    'web3==7.2.0',
    ]

if platform.system() == 'Windows':
    platform_specific_requires = [
        'certifi==2022.12.7',
        'psutil==6.0.0',
        'pycryptodome==3.20.0',
    ]

elif platform.system() == 'Darwin':
    platform_specific_requires = [
        'Pillow==9.5.0',
        'PyQt5==5.15.10',
        'pyzipper==0.3.6',
    ]

install_requires = common_requires + platform_specific_requires

setup(
    name='CryptoAiTools',
    version='0.6',
    description='A Python toolkit to create and manage crypto trading bots',
    author='CryptoAi',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'crypto-bot=CryptoAiTools.bot_creator:main',
            'run-base=CryptoAiTools.base:run_base',
        ],
    },
)
