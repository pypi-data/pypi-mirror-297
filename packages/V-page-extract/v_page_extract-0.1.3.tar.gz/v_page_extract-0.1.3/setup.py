from setuptools import setup, find_packages

setup(
    name='V_page_extract',
    version='0.1.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hib_hib = V_page_extract.main: hibernate',
        ],
    },
    install_requires=[
        'PyPDF2>=1.26.0',  
        "matplotlib>=3.0.0",
        "numpy>=1.18.0",
        "os"
    ],
    author='Vadym S',
    author_email='olko.soroka3@gmail.com',
    description='page extractor',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)


