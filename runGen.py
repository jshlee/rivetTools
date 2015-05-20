#!/usr/bin/env python

import os, sys, time

raw_f = sys.argv[1]
tot_eve = int(sys.argv[2])
max_num = int(sys.argv[3])
min_pt = int(sys.argv[4])
max_pt = int(sys.argv[5])
n_f = tot_eve/max_num
if n_f == 0:
  n_f = 1
time_dir = raw_f[:-3] +"_Pt_%dTo%d_%d"%(min_pt, max_pt, tot_eve)+time.strftime("_%d%b%Y_%HH%MM",time.localtime())
os.mkdir(time_dir)
itime_dir = os.getcwd()+"/"+time_dir

ana_path = os.getcwd()

script_head ="""#PBS -S /bin/bash
#PBS -N GEN_%s_%03d
#PBS -l nodes=1:ppn=1,walltime=72:00:00
#PBS -o $PBS_JOBID.$PBS_O_HOST.out
#PBS -e $PBS_JOBID.$PBS_O_HOST.err
#PBS -m abe
#PBS -V

#echo $PBS_O_HOST
cat $PBS_NODEFILE
#echo $PBS_TASKNUM

source /pnfs/etc/profile.d/cmsset_default.sh
cd /pnfs/user/hyunyong/CMSSW_7_2_0_pre3/src
eval `scramv1 runtime -sh`
"""

mc_name = ana_path.split("/")[-1]
for x in xrange(n_f):
  x = x+501
  tmp_cmd = open(itime_dir+"/q_%03d.cmd"%x,'w')
  tmp_cmd.write(script_head%(raw_f[:-3],x))
  tmp_cmd.write("\ncd "+itime_dir+"\n")
  tmp_cmd.write("cmsRun "+ana_path+"/"+raw_f+" %d %d %d %d"%(max_num, x, min_pt, max_pt))
  tmp_cmd.close()
os.chdir(itime_dir)
for x in xrange(n_f):
  x = x+501
  os.system("qsub -q kcms "+itime_dir+"/q_%03d.cmd"%x)

 
