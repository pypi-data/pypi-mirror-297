# python-library

https://pypi.org/project/biginsight

# biginsight python package

# dependencies usages
(twine) securely upload the package to PyPI
(whee) for distributing files

# publish
python setup.py sdist bdist_wheel
twine upload dist/* -u __token__ -p <token>

# Installation
pip install biginsight