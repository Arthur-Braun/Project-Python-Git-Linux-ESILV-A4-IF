#!/bin/bash

URL="https://www.exchangerates.org.uk/Euros-to-South-Korean-Won-currency-conversion-page.html"

PAGE=$(curl -s "$URL")

TEXT=$(echo "$PAGE" | grep -oP '<span id="shd2b;">\K[^<]*(?=</span>)')

echo $TEXT > output.txt

sudo python3 scriptdash.py

