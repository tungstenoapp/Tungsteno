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

rsync -av --delete "$SUBMODULE_PATH/public/" "$GUI_PATH"