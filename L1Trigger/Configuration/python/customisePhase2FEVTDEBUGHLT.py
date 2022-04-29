import FWCore.ParameterSet.Config as cms

def customisePhase2FEVTDEBUGHLT(process):
    process.FEVTDEBUGHLTEventContent.outputCommands.append('drop l1tPFCandidates_*_*_L1')
    return process
