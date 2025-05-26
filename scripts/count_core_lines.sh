#!/bin/bash

DIR="core"

echo "Counting lines in .py and .html files under $DIR ..."

LINE_COUNT=$(find "$DIR" \( -name "*.py" -o -name "*.html" \) -type f -exec cat {} + | wc -l)

echo "Total lines in .py and .html files inside '$DIR': $LINE_COUNT"

