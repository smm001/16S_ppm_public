#Copyright 2020 Stefano M. Marino   All rights reserved.
#contact <git_hub_username:sm001>
#This program is a free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 3 of the License, or in case any of the later versions.*
#This program is distributed WITHOUT ANY WARRANTY; see the GNU General Public License for more details.*
#A copy of the GNU General Public License is provided in this distribution

# -*- coding: utf-8 -*-
import re, os,sys

def filter_multiID(nome):
    g=open(nome).readlines()
    d1={}
    l1=[]
    for j in range(len(g)):
        i=g[j]
        if len(i) > 0:
            i2= i[:-1]
            Id=i2.split()[0]
            l1.append(Id)
            annota_l=i2.split("\t")[1:]
            annot=""
            for e in annota_l:
                annot=annot+"\t"+e
            if d1.has_key(Id):
               pass  
            else:
               d1[Id]= annot
    d2={}
    out=open(nome+"_best","w")
    for i in d1:

        if l1.count(i)> 1:
          d2[i]=1  

        out.write(i+d1[i]+"\n")
    out.close()


def filter_blast(top_hits, k):
    hits=open(top_hits).read().split('\n')
    filt_out=''
    for e in hits:
      if len(e) > 1:
       if len(e.split('\t')):
        cov=int(e.split('\t')[2])
        if cov > int(k):
            filt_out=filt_out+e+'\n'
    return filt_out


def filter_blast_percid(top_hits, p):
    hits=open(top_hits).read().split('\n')
    filt_out=''
    for e in hits:
      if len(e) > 1:
       if len(e.split('\t')):
        perc=float(e.split('\t')[-1])
        if perc >= float(p):
            filt_out=filt_out+e+'\n'
    return filt_out


def count_species(name):
    outname=name.replace("strain","species")
    out=open(outname,"w")
    h=open(name).read().split("\n")
    diz_sp={}
    for i0 in h:
       if len(i0)>0:
        n=i0.split()[0]
        if "Candidatus" in i0.split()[1]:
           i0=i0.replace("Candidatus ","Candidatus-")        
        k=i0.split()[1].replace(" ","")
        k2=i0.split()[1]+"_"+i0.split()[2]
        i=k2
        if diz_sp.has_key(i):
            diz_sp[i]=diz_sp[i]+int(n)
        else:
            diz_sp[i]=int(n)
    for i in diz_sp:
        out.write(i+"\t"+str(diz_sp[i])+"\n")

    out.close()

conf=open("configuration.cfg").read().split("\n")
for line in conf:
    if "num_threads=" in line:
        num_threads=int(line.split("num_threads=")[1])
    elif "max_t=" in line: # set in configuration.cfg to 0, for unrestricted blast search
        max_t=int(line.split("max_t=")[1])
    elif "db=" in line:
        db=(line.split("db=")[1])
    elif "blastn=" in line:
        blastn=(line.split("blastn=")[1])
    elif "evalue=" in line:
        evalue=float(line.split("evalue=")[1])
        
    elif "align_coverage_cutoff=" in line:
        align_coverage_cutoff=int(line.split("align_coverage_cutoff=")[1])
    elif "align_perc_id_cutoff=" in line:
        align_perc_id_cutoff=int(line.split("align_perc_id_cutoff=")[1])
    elif "Nanofilt=" in line:
        Nanofilt=int(line.split("Nanofilt=")[1])
    elif "Q_filt=" in line:
        Q_filt=str(line.split("Q_filt=")[1])
    elif "L_filt=" in line:
        L_filt=str(line.split("L_filt=")[1])
    elif "porechop=" in line:
        porechop=int(line.split("porechop=")[1])
    elif "blastn=" in line:
        blastn=(line.split("blastn=")[1])
    elif "porechop_runner=" in line:
        porechop_runner=(line.split("porechop_runner=")[1])
    elif "Nanofilt_runner=" in line:
        Nanofilt_runner=(line.split("Nanofilt_runner=")[1])
    elif "Filtlong_runner=" in line:
        Filtlong_runner=(line.split("Filtlong_runner=")[1])
    elif "max_num_fasta=" in line:
        max_num_fasta=int((line.split("max_num_fasta=")[1]))
    elif "min_num_fasta=" in line:
        min_num_fasta=int((line.split("min_num_fasta=")[1]))



inpQ=sys.argv[1] 
inp2=inpQ.split(".fasta")[0];inp2=inp2.split("/")[-1]

if porechop ==1:
       vp=os.system("python3.4 --version > p34version_temp")
       svp=os.path.getsize("p34version_temp")
       if svp > 0:
             print "--> porecop: using python 3.4 .." ## edit this for any specific version (a working one, however, depends also on g++ version; https://github.com/rrwick/Porechop)
             os.system("python3.4 "+porechop_runner+" -i "+inpQ+" -o "+inpQ+"_t --threads="+str(num_threads))
             os.system("mv "+inpQ+"_t "+inpQ)
       else:
             os.system("python3 "+porechop_runner+" -i "+inpQ+" -o "+inpQ+"_t --threads="+str(num_threads))
             os.system("mv "+inpQ+"_t "+inpQ)
       os.remove("p34version_temp")

if Nanofilt ==1:
       if os.path.exists(Nanofilt_runner):
        os.system("cat "+inpQ+" | "+Nanofilt_runner+" -q "+Q_filt+" -l "+L_filt+" > "+inpQ+"_qc")
        os.system("mv "+inpQ+"_qc "+inpQ)
       else:
          vQ=1-(10**(-(float(Q_filt)/10)))
          print "Filtlong, --min_mean_q = ",vQ
          os.system(Filtlong_runner+" "+inpQ+" --min_mean_q "+str(vQ)+" --min_length "+L_filt+" > "+inpQ+"_qc")
          os.system("mv "+inpQ+"_qc "+inpQ)
    
    
os.system("sed -n '1~4s/^@/>/p;2~4p' "+inpQ+" > "+inp2.split(".fastq")[0]+".fasta")

inpF=inp2.split(".fastq")[0]+".fasta"
inp2=inp2.split(".fastq")[0]




inp2.split(".fastq")[0]+".fasta"


t_n=len(open(inpF).read().split(">")) - 1

if t_n > max_num_fasta:
        t_n=max_num_fasta
else:
        t_n=t_n

if t_n > min_num_fasta: # min number of seqs, set in configuration file, to parse the barcoded ( -- if not for testing purposes, it could be set to 100)
        try:
         os.system("python2 scripts/take_random_subset_fasta.py "+inpF + " "+str(t_n))
         
        except:
         print "could not take random fasta subset "+inpF
        fasta_input_short="analyzed_seqs_"+inpF
        
        #os.system("cp "+inpF+" "+inpF+"_all")
        #inpF=fasta_input_short
        os.system("mv "+fasta_input_short+" "+inpF)
        
        per__id=0
        evalue=str(evalue)

        if max_t > 0:
        ##for max_t
         comando=blastn+" -db "+db+" -query "+inpF+" -num_threads "+str(num_threads)+" -outfmt '6 qseqid evalue qcovhsp salltitles pident' -max_target_seqs "+str(max_t)+" -evalue "+evalue+" > "+inp2+"_unfilter_top_hits.txt"
        elif max_t == 0:
        ##for no max target 
         comando=blastn+" -db "+db+" -query "+inpF+" -num_threads "+str(num_threads)+" -outfmt '6 qseqid evalue qcovhsp salltitles pident' -evalue "+evalue+" > "+inp2+"_unfilter_top_hits.txt"


        os.system(comando)

        nome_temp=inp2+"_unfilter_top_hits.txt"
        f2=filter_multiID(nome_temp)

        koff=align_coverage_cutoff
        p=align_perc_id_cutoff

        f=filter_blast(nome_temp+"_best",koff)
        outo=open("cov_"+str(koff)+"_"+inp2+"_top_hits.txt","w")
        outo.write(f)
        outo.close()

        f=filter_blast_percid("cov_"+str(koff)+"_"+inp2+"_top_hits.txt",p)
        outo=open("cov_"+str(koff)+"_idfilt_"+str(p)+"_"+inp2+"_top_hits.txt","w")
        outo.write(f)
        outo.close()
        os.remove("cov_"+str(koff)+"_"+inp2+"_top_hits.txt")

        os.system("mv cov_"+str(koff)+"_idfilt_"+str(p)+"_"+inp2+"_top_hits.txt "+nome_temp)

        log=open("log_run_fromfasta_pipe_16S_NCBI.log","w")
        log.write("commmand="+comando+"\nblast version = "+blastn+"\nDB="+db+"\nINPUT="+inpF+"\nevalue="+evalue)

        nf0=open(inpF).read().split(">")
        nf=len(nf0)-1
        log.write("\nnum_seqs_analyzed = "+str(nf)+"\n") ### number seqs actually fed to blast


        if koff > 0 or p> 0:
            log.write("\nBlast filtered for Coverage="+str(koff)+ " %identity="+str(p)+"\n")

        os.system("cat "+str(nome_temp)+" | cut -f4 | sort | uniq -c | sort -nr > "+str(inp2)+"_strain_counts.txt")
        nome_x_demo=str(inp2)+"_strain_counts.txt"
        count_species(nome_x_demo)

        ss=nome_x_demo.replace("strain","species")

        os.system("sort -k 2 -nr "+ss+" > "+ss+".sorted")


        inpo=open(ss+".sorted").readlines()
        root_name=""
        outo_name=("Out16S_"+root_name+"_"+ss)
        outo=open(outo_name,"w")
        num_reads=0
        for m in inpo:
                    m=m[:-1]
                    m2=m.split()
                    nm=int(m2[-1])
                    num_reads=num_reads+nm
        sample_name=inp2

        outo.write("#Identification: "+sample_name+", reads="+str(num_reads)+"\n#Genus,species,counts,relative abundance (%)\n")
                    
        for m in inpo:
                    m=m[:-1]
                    num=int(m.split()[-1])
                
                    rel=num/float(num_reads)
                    rel1=round(rel,8)
                    rel1=100*rel1
                    m2=m.split()
                    line=m2[0]+","+str(m2[-1])+","+str(rel1)
                    line=line.replace("_",",")
                    outo.write(line+"\n")

        outo.close()

        ### below, clean up of temporary files, and move output files to output folder

        out=inp2+"_results_fromfasta"

        if os.path.isdir(out):
            os.system("rm -r "+out+"/*")
            pass
        else:
            os.makedirs(out)
        log.close()

        os.system("mv "+outo_name+" "+out)

        os.system("mv log_run_fromfasta_pipe_16S_NCBI.log "+out)
        os.system("rm "+ss+" "+ss+".sorted "+nome_x_demo+" "+nome_temp)

        os.system("mv "+nome_temp+"_best"+" "+out)





