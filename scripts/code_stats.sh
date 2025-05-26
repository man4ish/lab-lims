#!/bin/bash

# Count lines in .py and .html files under core/
find core/ -type f \( -name "*.py" -o -name "*.html" \) -exec wc -l {} + | tee >(tail -n 1)

