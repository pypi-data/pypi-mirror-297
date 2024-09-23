# setup.py

from setuptools import setup, find_packages

setup(
    name='borsaAPI',  # Paketinizin adı
    version='0.1',
    description='Python kütüphanesi ile BIST hisse verisi çekme API\'si',
    author='Bora Kaya',
    author_email='bora.587@hotmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
