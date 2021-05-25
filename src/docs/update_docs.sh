#!/bin/bash

git submodule update --remote --depth 1
git add docs_markdown/*
git commit -m "Update docs"
git push