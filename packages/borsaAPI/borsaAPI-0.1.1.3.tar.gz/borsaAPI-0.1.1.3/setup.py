from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='borsaAPI',  # Paketinizin adı
    version='0.1.1.3',  # Sürüm numarası
    description='Python kütüphanesi ile hisse verisi çekme API\'si',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Bora Kaya',
    author_email='borakaya8@gmail.com',
    packages=find_packages(),  # Paketlenecek modülleri bulur
    include_package_data=True,  # Paketlemedeki dosyaları dahil eder
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
