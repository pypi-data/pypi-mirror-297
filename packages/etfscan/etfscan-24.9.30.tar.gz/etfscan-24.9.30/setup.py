from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='etfscan',
    version='24.9.30',
    url='https://gitlab.esrf.fr/night_rail/applications/tools/etfscan',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'create_etf = etfscan.create_etf:main',
        ],
    },
    install_requires=[
        'wheel',
        'nxtomomill',
        'scipy',
        'numpy',
        'namedlist'
    ],
    author='Alessandro Mirone',
    author_email='alessandro@example.com',
    description='Library and tool for handling ETF files.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
    ],
)

