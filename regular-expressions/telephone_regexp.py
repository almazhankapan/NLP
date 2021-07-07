import sys
import re

if len(sys.argv) > 1:
    with open(sys.argv[1]) as infile:
        corpus = infile.read()    
else:
    with open('test_dollar_phone_corpus.txt') as infile:
        corpus = infile.read()

reg_expression = "(\(\d{3}\)) *(\d{3})[- ]?(\d{4})|(\d{3})[- ]?(\d{3})[- ]?(\d{4})"

with open("telephone_output.txt", "w") as outfile:
    for i in re.finditer(reg_expression, corpus, re.M):
        items = i.group(0)
        outfile.write(items + "\n")
        sys.stdout.write(items + "\n")

