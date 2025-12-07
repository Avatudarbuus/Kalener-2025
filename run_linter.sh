#!/bin/bash 

pylint_args=(
    --disable C2401 # Non ASCII names 
    --disable C0303 # Trailing whitespace 
    --disable C0304 # Final newline missing
    --disable C0200 # Consider using enumerate 
    --disable W1514 # Not specyfing encoding
    --disable W0105 # Using triple upperscore strings in other than docstring
    --disable=R # Refactoring related checks 
  )

for f in $(find . -name "*.py" -not -path "./venv/*" -not -path "./__pycache__/*");
do
  pylint "${pylint_args[@]}" "$f"
done

