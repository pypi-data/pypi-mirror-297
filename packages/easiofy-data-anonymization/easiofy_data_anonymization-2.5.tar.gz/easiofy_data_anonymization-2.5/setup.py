from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='easiofy-data-anonymization',
    version='2.5',
    description='A FastAPI application for DICOM data anonymization.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Easiofy Pvt Ltd',
    author_email='info@easiofy.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'fastapi',
        'uvicorn',
        'aiohttp',
        'firebase-admin',
        'pydicom',
        'python-multipart',
        'werkzeug',
        'python-dotenv'
    ],
    entry_points={
        'console_scripts': [
            'easiofy-data-anonymization = easiofy_data_anonymization.api:main',
        ],
    },
    package_data={
        'easiofy_data_anonymization': ['encrypted_creds.txt'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
