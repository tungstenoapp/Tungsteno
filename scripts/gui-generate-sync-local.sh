#!/usr/bin/env bash

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")
SUBMODULE_PATH="$BASEDIR/../submodules/tungnsteno-gui/"
GUI_PATH="$BASEDIR/../tsteno/gui/static"

OLDPWD=$PWD

cd "$SUBMODULE_PATH/app"

if [[ ! -d "$SUBMODULE_PATH/app/node_modules/" ]]; then
    npm install
fi
npm run build

cd "$OLDPWD"

rsync -av --delete "$SUBMODULE_PATH/app/build/" "$GUI_PATH"