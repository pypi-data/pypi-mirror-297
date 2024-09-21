from setuptools import setup, find_packages

setup(
    name='mini-network-administrator-tools',
    version='0.1',
    packages=find_packages(),
    install_requires=[
            'scapy'
        ],
    description='Un package Python exemple',
    author='Ton Nom',
    author_email='ayenaaurel15@gmail.com',
    url='https://github.com/toncompte/mon_package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
