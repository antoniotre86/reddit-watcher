#!/bin/bash

pip install -r requirements.txt --target ./package
cd package
zip -r ../deployment-package.zip .
cd ..
zip -g deployment-package.zip lambda_function.py
zip -r9 deployment-package.zip ./reddit_watcher
