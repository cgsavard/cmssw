#!/bin/bash
submitDir=$PWD
branch=$1


if [ ! -e /eos/uscms/store/user/${USER}/testTrunc/ ]
    then
    echo "I need /eos/uscms/store/user/${USER}/testTrunc/"
    exit
fi

source makeTar.sh                # package up code to transfer to worker nodes
cd $submitDir
 
#To test a single one
#outputDir="MC"
#trunc=$outputDir
#condor_submit batchExecute.jdl exec_name="truncOpt_$trunc" arguments="${outputDir} L1TrackNtupleMaker_cfg.py $trunc"

#Looping through all options
declare -a truncOptions=("IR" "MC" "ME" "MP" "PR" "TC" "TE" "TP" "TRE" "VMR" "All" "None")
#declare -a truncOptions=("TC" "All" "None")
for trunc in ${truncOptions[@]}; do
  outputDir=$trunc
  echo "outputDir ${outputDir}"
  condor_submit batchExecute.jdl exec_name="truncOpt_$trunc" arguments="${outputDir} L1TrackNtupleMaker_cfg.py $trunc"
done
