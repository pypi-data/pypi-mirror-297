from setuptools import setup, find_packages

setup(
    name='MondayShareableLinks',
    version='2.0.0',
    packages=find_packages(),
    install_requires=[
        'selenium', 
        'chromedriver-py'
    ],
    author='Chamundeshwawri',
    author_email='chamsund@cisco.com',
    description='A package for disabling Monday Shareable links',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'MondayShareableLinks=MondayShareableLinks.DisableShareLinks:main',
        ],
    }
)