#!/usr/bin/env bash

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")
SUBMODULE_PATH="$BASEDIR/../submodules/tungnsteno-gui/"
GUI_PATH="$BASEDIR/../tsteno/gui/static"

OLDPWD=$PWD

cd "$SUBMODULE_PATH"

npm install
grunt

cd "$OLDPWD"

rm -rf "$GUI_PATH"
echo rsync "$SUBMODULE_PATH/public" "$GUI_PATH"