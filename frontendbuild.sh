#!/bin/sh

set -ev

npm install -g snyk
npm install
bower install
gulp
