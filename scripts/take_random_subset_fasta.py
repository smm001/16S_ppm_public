#Copyright 2020 Stefano M. Marino   All rights reserved.
#contact <git_hub_username:sm001>
#This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License, or in case any of the later versions.*
#This program is distributed WITHOUT ANY WARRANTY; see the GNU General Public License for more details.*
#A copy of the GNU General Public License is provided in this distribution

import sys, random
l1=[]
nome=sys.argv[1]
lun=0  ## filter by length 
subsample_size=sys.argv[2]
numero=int(subsample_size)
g=open(nome).read().split(">")
for i in g:
    if len(i) > 1:
        i2=i.split("\n")
        seq=i2[1]
        if 1==1:
        #if len(seq) >=int(lun):
           l1.append(">"+i)
o=""
random.shuffle(l1)
if numero > len(l1):
        numero=len(l1)
for i in range(int(numero)):
 try:
    s=l1[i]
    o=o+s
 except IndexError:
     pass 
out=open("analyzed_seqs_"+nome,"w")
out.write(o)
out.close()
