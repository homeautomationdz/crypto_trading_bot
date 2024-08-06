from setuptools import setup, find_packages

setup(
    name='crypto_trading_bot',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas',
        'python-binance',
        'matplotlib',
        'python-telegram-bot',
        # Add other dependencies here
    ],
)
