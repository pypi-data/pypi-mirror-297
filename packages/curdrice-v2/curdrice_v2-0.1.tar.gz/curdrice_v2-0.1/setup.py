from setuptools import setup

with open("README.md") as r:
    Long_desc = "\n" + r.read()

setup(
    name = 'curdrice-v2',
    version = '0.1',
    description = 'A ML model training automation tool',
    long_description_content_type = "text/markdown",
    long_description = Long_desc,
    packages = ['curdrice'],
    include_package_data = True,
    install_requires = ['click','numpy','pandas', 'scikit-learn', 'openpyxl', 'scikit-learn-extra', 'mlxtend', 'joblib', 'tabulate'],
    classifiers = [
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'License :: OSI Approved :: MIT License'
            ],
    license = 'MIT',
    entry_points = '''
    [console_scripts]
    curdrice = curdrice.main:curdrice
    '''
)