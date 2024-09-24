
#### 1.4 `setup.py`
from setuptools import setup, find_packages

setup(
    name='zscore_anomaly_detector',
    version='0.1',
    packages=find_packages(),
    description='A Python package to detect anomalies using Z-Scores',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='',  # GitHub URL'si yoksa bu alanı boş bırakabilirsiniz
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Geçerli bir lisans sınıfı
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas'
    ],
)

