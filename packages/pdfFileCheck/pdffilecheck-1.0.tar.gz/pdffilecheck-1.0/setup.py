from setuptools import setup, find_packages

setup(
    name='pdfFileCheck',
    version='1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'pdfFileCheck=pdfFileCheck.check:check_pdf',
        ],
    },
    author='Abu Said',
    author_email='bananaspritz@protonmail.com',
    description='A package to check if a file is a real PDF and report its size in KB and MB.',
    url='https://github.com/said7388',
)