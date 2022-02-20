from setuptools import setup

setup(
    name='TinyAutoML',
    version='0.1',
    packages=['tests', 'support', 'support.constants', 'support.SupportClasses', 'examples', 'Estimator'],
    url='https://github.com/g0bel1n/TinyAutoML',
    license='MIT',
    author='g0bel1n',
    author_email='lucas.saban@ensae.fr',
    install_requires = ['pandas',
                        'scikit-learn',
                        'tqdm',
                        'numpy',
                        'statsmodels',
                        'matplotlib',
                        'xgboost'],
    description='Combinaison of ML models for binary classification. Academic Project.',
    download_url = 'https://github.com/g0bel1n/TinyAutoML/archive/refs/tags/v0.1.tar.gz',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Students',
        'License :: OSI Approved :: MIT License',

    ],
    # I explain this later on

)
