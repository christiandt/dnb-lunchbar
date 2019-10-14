#!/usr/bin/env bash
set -x
read -p 'Identity: ' identity
codesign --deep --force --verbose --sign "${identity}" dist/LunchBar.app
codesign --verify -vvvv dist/LunchBar.app/
#spctl -a -vvvv dist/LunchBar.app/