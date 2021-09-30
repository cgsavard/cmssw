#!/bin/bash

cd $CMSSW_BASE/../
tar -cf workingArea.tar CMSSW_11_2_0_pre6 --exclude='*.dag.*' --exclude='*tar' --exclude='CMSSW_11_2_0_pre6/src/*root' --exclude='*eps' --exclude='*png' --exclude='*pdf' --exclude='*stdout' --exclude='*stderr' --exclude='*condor' --exclude='CMSSW_11_2_0_pre6/src/datacards/*'
mv workingArea.tar $CMSSW_BASE/src/.
