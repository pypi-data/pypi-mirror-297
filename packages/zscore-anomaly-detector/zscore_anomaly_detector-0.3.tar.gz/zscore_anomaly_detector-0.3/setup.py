from setuptools import setup, find_packages

setup(
    name='zscore_anomaly_detector',
    version='0.3',  # Sürüm numarasını artırın
    packages=find_packages(),
    description='A Python package to detect anomalies using Z-Scores',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Volkan OBAN',  # Buraya isminizi yazın
    author_email='volkanobn@gmail.com',  # Buraya e-posta adresinizi yazın
    url='',  # GitHub URL'si varsa ekleyin, yoksa boş bırakabilirsiniz
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas'
    ],
)

