from setuptools import setup

setup(
    name='bang',
    version='0.1',
    py_modules=['bang'],
    install_requires=[
        'Click',
        'numpy',
        'scipy',
        'tqdm',
        'xxhash'
    ],
    entry_points='''
        [console_scripts]
        bang=bang:bang
    ''',
)
