#!/bin/bash
pyinstaller app.py --log-level=DEBUG --hidden-import packaging.requirements --add-data tsteno/:tsteno
