#!/usr/bin/env bash

echo "Create virtual environment"
virtualenv --python=python3 DBTPenv

echo "Activate environment"
source DBTPenv/bin/activate
which python
python --version

echo "Upgrading pip"
pip install --upgrade pip
echo "Installing packages"
pip install jupyter ipython-sql

echo "Done, deactivating the virtual environment"
deactivate
