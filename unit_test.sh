#!/bin/zsh

echo
echo Running unit tests...

echo
python3 -B tests/english_card_test.py
python3 -B tests/french_card_test.py
python3 -B tests/japanese_card_test.py
python3 -B tests/vietnamese_card_test.py

python3 -B tests/port_test.py
