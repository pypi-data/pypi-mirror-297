import setuptools
from nblock import __version__ as nblock_version

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='nblock',
    version=nblock_version,
    maintainer_email = "fredzenobius@gmail.com",
    description='nblock for nsearch',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
    install_requires=[
        'selenium==3.141.0',
        'urllib3==1.26.12',
        'requests',
        'pyperclip',
        'chromedriver-autoinstaller',
        'fake-useragent',
        'tqdm',
    ],
)   