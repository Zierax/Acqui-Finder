from setuptools import setup, find_packages

setup(
    name='acqui-finder',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'apify-client',
        'python-dotenv',
    ],
    entry_points={
        'console_scripts': [
            'acquisitions-recon = script:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
