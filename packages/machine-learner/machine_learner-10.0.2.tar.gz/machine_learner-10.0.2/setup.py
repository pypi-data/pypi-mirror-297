from setuptools import setup, find_packages

setup(
    name='machine_learner',
    version='10.0.2',
    author='Megan Jameson',
    description='A comprehensive Python module for feature engineering, target computation, rolling window modeling, feature selection, and model evaluation, tailored for time-series forecasting and stock price analysis.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/megandevelops/machine_learner',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.21.0',
        'pandas>=1.3.0',
        'scikit-learn>=1.0.0',
        'statsmodels>=0.12.2',
        'ta-lib>=0.4.0',  # If you're using technical indicators like RSI or Bollinger Bands
        'matplotlib>=3.4.0',  # If used for plotting (optional)
        'seaborn>=0.11.0',  # For correlation matrix plotting (optional)
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
)