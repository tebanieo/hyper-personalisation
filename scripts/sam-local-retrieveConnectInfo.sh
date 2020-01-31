#!/usr/bin/env bash
set -e
echo "Compiling in progress..."

declare TEMPLATE_FILE="../templates/lambdaOne.yaml.tmpl"

# Clear and recreate the dist dir
echo "Compiling to dist"
rm -rvf dist
mkdir dist

# Compile the template
source config.local.sh
eval "echo \"$(< $TEMPLATE_FILE)\"" > dist/template.local.yaml

echo "Compile successful!"
