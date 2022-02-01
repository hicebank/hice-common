import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='hice_common',
    version='0.0.4',
    author='hicebank.ru',
    author_email='tingaev@hicebank.ru',
    description='Phone number validator via pydantic',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hicebank/hice_common',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={
        "hice_common": ["py.typed"],
    },
)
