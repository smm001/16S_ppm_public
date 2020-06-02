#Copyright 2020 Stefano M. Marino   All rights reserved.
#contact <git_hub_username:sm001>
#This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License, or in case any of the later versions.*
#This program is distributed WITHOUT ANY WARRANTY; see the GNU General Public License for more details.*
#A copy of the GNU General Public License is provided in this distribution

import os, sys
print ("command format: python run_from_fasta.py input.fasta")
try:
    inp=sys.argv[1]
except:
    inp="error_no_input"
    print (" warning: NO FASTQ input provided..")
    
conf=open("configuration.cfg").read().split("\n")

for line in conf:

    if "script_fromfastQ=" in line:
        script_fromfastQ=line.split("script_fromfastQ=")[1]

os.system("python2 scripts/"+script_fromfastQ+" "+inp)

