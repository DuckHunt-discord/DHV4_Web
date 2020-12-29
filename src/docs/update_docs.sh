#!/bin/bash

git submodule update --remote
git add markdown_files
git commit -m "Update docs"
git push