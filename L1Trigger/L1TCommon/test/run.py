# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: step2 --python_filename=rerun_step2_L1_onMCL1_FEVTHLTDEBUG.py --no_exec -s L1 --datatier GEN-SIM-DIGI-RAW -n 1 --era Phase2_timing --eventcontent FEVTDEBUGHLT --filein file:/afs/cern.ch/user/r/rekovic/release/CMSSW_9_3_2/src/step2_DIGI_PU200_10ev.root --conditions 93X_upgrade2023_realistic_v2 --beamspot HLLHC14TeV --geometry Extended2023D17 --fileout file:step2_ZEE_PU200_1ev_rerun-L1-L1Ntuple.root --customise=L1Trigger/L1TNtuples/customiseL1Ntuple.L1NtupleEMU
import FWCore.ParameterSet.Config as cms
import sys
import os

from Configuration.StandardSequences.Eras import eras

process = cms.Process('L1',eras.Phase2_trigger)

GEOM = 'D41'

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023'+GEOM+'Reco_cff') #NEED TO CHANGE GEOM NUMBER BASED ON SAMPLES
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('L1Trigger.TrackFindingTracklet.L1TrackletTracks_cff')
process.load('L1Trigger.VertexFinder.VertexProducer_cff')
process.load('L1Trigger.TwoLayerJets.TwoLayerJets_cfi')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(3)
)

# Input source
Source_Files = cms.untracked.vstring(
'file:root://cms-xrd-global.cern.ch//store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/106X_upgrade2023_realistic_v2_2023D41noPU-v1/10000/F1B6D387-7EA9-0B47-8661-2D444502CD15.root'
)

process.source = cms.Source("PoolSource", fileNames = Source_Files,
    secondaryFileNames = cms.untracked.vstring(),
inputCommands = cms.untracked.vstring("keep *", 
        "drop l1tHGCalTowerMapBXVector_hgcalTriggerPrimitiveDigiProducer_towerMap_HLT",
        "drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT",
        "drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT",
        "drop l1tEMTFHit2016s_simEmtfDigis__HLT",
        "drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT",
        "drop l1tEMTFTrack2016s_simEmtfDigis__HLT")
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step2 nevts:1'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '100X_upgrade2023_realistic_v1', '')


process.L1TrackTrigger_step = cms.Path(process.L1TrackletTracksWithAssociators)
process.VertexProducer_step = cms.Path(process.VertexProducer)
process.TwoLayerJets_step = cms.Path(process.TwoLayerJets)

# correct input tag name
process.VertexProducer.L1TracksInputTag = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks")
process.TwoLayerJets.L1TracksInputTag = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks")

# Path and EndPath definitions
#process.L1simulation_step = cms.Path(process.SimL1Emulator)
#process.endjob_step = cms.EndPath(process.endOfProcess)
#process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

############################################################  
# Define the track ntuple process, MyProcess is the (unsigned) 
# PDGID corresponding to the process which is run
# e.g. single electron/positron = 11
#      single pion+/pion- = 211
#      single muon+/muon- = 13
#      pions in jets = 6
#      taus = 15
#      all TPs = 1
############################################################

process.L1TrackVtxJetsNtuple = cms.EDAnalyzer('L1TrackVtxJetsNtupleMaker',
        MyProcess = cms.int32(1),
        DebugMode = cms.bool(False), # printout debug statements
        SaveAllTracks = cms.bool(True), # save *all* L1 tracks
        SaveStubs = cms.bool(False), # save some info for *all* stubs
        LooseMatch = cms.bool(False), # "loose" MCtruth association
        L1Tk_nPar = cms.int32(4), # use 4 or 5-parameter L1 tack fit
        L1Tk_minNStub = cms.int32(4), # L1 tracks with >= 4 stubs  
        TP_minNStub = cms.int32(4), # require TP to have >= X number of stubs associated with it
        TP_minNStubLayer = cms.int32(4),  # require TP to have stubs in >= X layers/disks
        TP_minPt = cms.double(2.0),       # only save TPs with pt > X \GeV
        TP_maxEta = cms.double(2.4),      # only save TPs with |eta| <\X
        TP_maxZ0 = cms.double(30.0),      # only save TPs with |z0| < \X cm
        L1TrackInputTag = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks"), ## TTTrack input  
        MCTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks"), ## MCTruth input
        # other input collections
        L1StubInputTag = cms.InputTag("TTStubsFromPhase2TrackerDigis","StubAccepted"),
        MCTruthClusterInputTag=cms.InputTag("TTClusterAssociatorFromPixelDigis", "ClusterAccepted"),
        MCTruthStubInputTag = cms.InputTag("TTStubAssociatorFromPixelDigis", "StubAccepted"),
        TrackingParticleInputTag = cms.InputTag("mix", "MergedTrackTruth"),
        TrackingVertexInputTag = cms.InputTag("mix", "MergedTrackTruth"),
        TwoLayerTkJetInputTag = cms.InputTag("TwoLayerJets" , "L1TwoLayerJets"),
        RecoVertexInputTag = cms.InputTag("VertexProducer","l1vertextdr"),
        genParticleToken = cms.InputTag("genParticles")
                                       )

process.Ntuple_step = cms.Path(process.L1TrackVtxJetsNtuple)

#process.TFileService = cms.Service("TFileService", fileName = cms.string('TTbar_upgrade2023_noPU_Ntuple.root'), closeFileFast = cms.untracked.bool(True))
process.TFileService = cms.Service("TFileService", fileName = cms.string('outTest.root'), closeFileFast = cms.untracked.bool(True))


# Schedule definition
process.schedule = cms.Schedule(process.L1TrackTrigger_step,process.VertexProducer_step,process.TwoLayerJets_step,process.Ntuple_step)


