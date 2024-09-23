from setuptools import setup, find_packages

setup(
    name='V_page_extract',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'PyPDF2>=1.26.0',  
    ],
    author='Vadym S',
    author_email='olko.soroka3@gmail.com',
    description='page extractor',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown'
)
