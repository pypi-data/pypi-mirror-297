from setuptools import setup, find_packages
    
setup(
    name='iiris_redshift',
    version='0.0.5',
    description='Generic package which can be used for redshift',
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
