# SendSafely Python SDK (INTERNAL)
Install Python 3 or higher if not already installed
```
python3 --version
```
```
brew install python
```
The Python command to install pip (as pip3) and Setuptools
```
python3 -m pip install --upgrade setuptools
```
To create a source distribution
```
python3 setup.py sdist --dist-dir=dist
```
To install the source distribution
```
python3 -m pip install ./dist/sendsafely-x.y.z.tar.gz
```
To run unittests, update SendSafely instance in the test/*.py scripts, and then run the following from /src:
```
python3 -m unittest tests/*.py
```
To run integration scripts, cd to /scripts and run the python script with the following command
```
python3 sendsafely_python_example.py
```
_When testing, create and activate a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html) and then install the source distribution_
```
python3 -m venv /test/dir
source test/dir/bin/activate
```
To create pydocs, run
```
pydoc3 -w SendSafely sendsafely/*.py
```
Remove absolute path names from generated HTML prior to sharing with customer

## Prepare for public release
1) Bump version in setup.py
2) Run prepare_python_api.sh
3) In Python public repo directory, run build.sh
4) Test package upload and install by uploading to https://test.pypi.org/ and installing in virtual environment. 
4a) In virtual environment, run test script to verify working as expected.
5) Upload package to pypi
 
```buildoutcfg
./prepare_python_api.sh
```

