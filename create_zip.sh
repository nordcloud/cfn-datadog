#!/usr/bin/env bash

set -ex
rm -rf package_dir
mkdir package_dir
cp -a cfn_datadog package_dir/
cp index.py package_dir
cp timeboard_index.py package_dir
pip install -r requirements.txt -t package_dir
pushd package_dir
zip -r datadog_lambda.zip .
popd
mv package_dir/datadog_lambda.zip .