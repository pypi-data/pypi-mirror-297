from setuptools import setup, find_packages
    
setup(
    name='iiris_postgres',
    version='0.0.3',
    description='Generic package which can be used for postgres',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Roopendra',
    author_email='roopendra.naik@informa.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas",
        "psycopg2-binary",
        "sqlalchemy",
    ]
)
