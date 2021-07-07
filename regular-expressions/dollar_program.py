import sys
import re

if len(sys.argv) > 1:
    with open(sys.argv[1]) as infile:
        corpus = infile.read()    
else:
    with open('test_dollar_phone_corpus.txt') as infile:
        corpus = infile.read()
        
reg_expression = "(\$[ ]?([\d\,]+)([\.\d*](\d*))?([ ]?(thousand|million|billion|trillion))?)|(((one|five|half|t\'ree|three|fifteen|twenty|four|seven|six|eleven|twelve|two)[ ]?)?((hundred|hun\'red)[ ]?)?(thousand[ ]?)?([\w\.\,\']+)([ ]*([Dd]ollars|[dD]ollar|[^\w]cents)))" 

with open("dollar_output.txt", "w") as outfile:
    for i in re.finditer(reg_expression, corpus, re.M):
        items = i.group(0)
        items=items.strip('.')
        outfile.write(items + "\n")
        sys.stdout.write(items + "\n")



