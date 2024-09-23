from setuptools import setup, find_packages
    
setup(
    name='iiris_custom_logger',
    version='0.0.7',
    description='Generic package which can be used for logging purpose',
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
        "asgi-correlation-id"
    ],
)
