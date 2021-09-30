#!/bin/sh
echo "Starting job on "`date` # to display the start date
echo "Running on "`uname -a` # to display the machine where the job is running
echo "System release "`cat /etc/redhat-release` # and the system release
# Can also do 'lsb_release -d' or 'lsb_release -r'
echo "CMSSW on Condor"

# check arguments
export USER=$(whoami)
export CMSSWVER="CMSSW_11_2_0_pre6"
export CMSSWLOC="slc7_amd64_gcc900"
export CMSSWXRD=""

echo ""
echo "parameter set:"
echo "CMSSWVER: $CMSSWVER"
if [ -n "$CMSSWLOC" ]; then
    echo "CMSSWLOC: $CMSSWLOC"
fi
echo ""

# to get condor-chirp from CMSSW
export PATH="/usr/libexec/condor:$PATH"
# environment setup
source /cvmfs/cms.cern.ch/cmsset_default.sh

output_dir=$1
executable=$2
args1=$3


tar -xf workingArea.tar
cd CMSSW_11_2_0_pre6/src/
#eval `scramv1 runtime -sh`
eval `scramv1 b ProjectRename`
#eval `cmsenv`
#eval `echo scram b -j 8`
scramv1 b ProjectRename
cmsenv
scram b -j 8
eval `echo cmsRun L1Trigger/TrackFindingTracklet/test/$executable $args1`

ls *root

for file in $(ls *root)
do
    xrdcp -f $file root://cmseos.fnal.gov//store/user/${USER}/testTrunc/$output_dir/$file
done
