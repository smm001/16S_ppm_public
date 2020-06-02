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
    print (" warning: NO FASTA input provided..")
    
conf=open("configuration.cfg").read().split("\n")

for line in conf:
    if "script_BC=" in line:
        script_BC=line.split("script_BC=")[1]
    if "script_noBC=" in line:
        script_noBC=line.split("script_noBC=")[1]
    if "script_fromfasta=" in line:
        script_fromfasta=line.split("script_fromfasta=")[1]

os.system("python2 scripts/"+script_fromfasta+" "+inp)

