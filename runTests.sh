#!/bin/bash

source ./Configuration
source bin/activate

cd tests
python3 all_tests.py
