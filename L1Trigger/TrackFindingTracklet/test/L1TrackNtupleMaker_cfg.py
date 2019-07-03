############################################################
# define basic process
############################################################

import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
import os
process = cms.Process("L1TrackNtuple")

#GEOMETRY = "D21"
GEOMETRY = "D41"

 
############################################################
# import standard configurations
############################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')

print "using geometry " + GEOMETRY + " (tilted)"
process.load('Configuration.Geometry.GeometryExtended2023'+GEOMETRY+'Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023'+GEOMETRY+'_cff')

process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:upgradePLS3', '')


############################################################
# input and output
############################################################

Source_Files = cms.untracked.vstring(
    #"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/FEA5D564-937A-8D4B-9C9A-696EFC05AB58.root"
    '/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/106X_upgrade2023_realistic_v2_2023D41noPU-v1/10000/E68AE72E-7F71-CF4E-AF7F-2979EBD6F91E.root'
    )

ttbar_files_nopu = cms.untracked.vstring( #5000 events (1000 each)
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/106X_upgrade2023_realistic_v2_2023D41noPU-v1/10000/F1B6D387-7EA9-0B47-8661-2D444502CD15.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/106X_upgrade2023_realistic_v2_2023D41noPU-v1/10000/E68AE72E-7F71-CF4E-AF7F-2979EBD6F91E.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/106X_upgrade2023_realistic_v2_2023D41noPU-v1/10000/D85CCBFC-E9DE-3544-9300-FEDDF8562DF9.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/106X_upgrade2023_realistic_v2_2023D41noPU-v1/10000/C980D2FD-0E2E-C44E-8438-5A3F7F5A5D7D.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/106X_upgrade2023_realistic_v2_2023D41noPU-v1/10000/8D9A013D-DC9D-AD42-9E4D-5CD2E654AE61.root"
)

ttbar_files_pu200 = cms.untracked.vstring( #2000 events (100 each)
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/FEA5D564-937A-8D4B-9C9A-696EFC05AB58.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/FDC76D16-0161-F847-90F0-8FCD6623D62A.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/F9D30B8C-3A00-F847-9CAF-39F9F8B009ED.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/F982D8E1-0B79-D749-8D98-D2DE6D83759A.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/F71753BF-7C63-FD43-9C8B-3BA0269FA022.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/F16CE05D-0CBC-3749-AC72-D8B406ACD2BF.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/EE838A07-2798-7048-8E11-D21EA25AC75C.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/EC2854AD-F8B2-A54B-9512-9A81B84A1D86.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/EB759FCE-04CB-F740-A898-79B4C27165D6.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/E7F59820-664E-9445-B63D-DF8AABDE5A6F.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/E257FAA4-B837-0243-9FBA-4DE3D5C15841.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/DB7340F7-1235-FC4F-92ED-60D0AF73B6B3.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/DAC96E66-671C-194F-9311-470E17FB9725.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/D9A1601A-311F-3E46-8D30-AF2C219F5E35.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/D7F4ED22-EA9E-D14A-9AD5-6B3822CA7D92.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/D42CAC7C-B132-ED41-8083-23FB8699D61A.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/D2D6A242-59F4-BF4E-A36F-ABBED1AE760A.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/D22B3A99-4766-3040-A887-0CDD96D6B0B4.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/D1C7ABEE-DA0E-2D42-82BE-D51117A7CFDA.root",
"/store/relval/CMSSW_10_6_0_pre4/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_106X_upgrade2023_realistic_v2_2023D41PU200-v1/10000/CEF89EDC-2AF1-5946-8EEB-6B4D0B54557D.root"
)

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(3))

process.source = cms.Source("PoolSource", 
                            fileNames = ttbar_files_nopu,
                            inputCommands = cms.untracked.vstring(
                              'keep *_*_*_*',
                              'drop l1tEMTFHit2016*_*_*_*',
                              'drop l1tEMTFTrack2016*_*_*_*'
                              )
                            )

#process.TFileService = cms.Service("TFileService", fileName = cms.string('ttbar_pu200_loose_1000evt.root'), closeFileFast = cms.untracked.bool(True))
process.TFileService = cms.Service("TFileService", fileName = cms.string('outTest.root'), closeFileFast = cms.untracked.bool(True))



############################################################
# L1 tracking
############################################################

# remake stubs ?
process.load('L1Trigger.TrackTrigger.TrackTrigger_cff')
from L1Trigger.TrackTrigger.TTStubAlgorithmRegister_cfi import *
process.load("SimTracker.TrackTriggerAssociation.TrackTriggerAssociator_cff")

if GEOMETRY != "TkOnly":
    from SimTracker.TrackTriggerAssociation.TTClusterAssociation_cfi import *
    TTClusterAssociatorFromPixelDigis.digiSimLinks = cms.InputTag("simSiPixelDigis","Tracker")
    
process.TTClusterStub = cms.Path(process.TrackTriggerClustersStubs)
process.TTClusterStubTruth = cms.Path(process.TrackTriggerAssociatorClustersStubs)

from L1Trigger.TrackFindingTracklet.Tracklet_cfi import *

### floating-point simulation
#process.load("L1Trigger.TrackFindingTracklet.L1TrackletTracks_cff")
#TTTracksFromTracklet.asciiFileName = cms.untracked.string("output.txt")
#process.TTTracks = cms.Path(process.L1TrackletTracks)
#process.TTTracksWithTruth = cms.Path(process.L1TrackletTracksWithAssociators)

## emulation 
process.load("L1Trigger.TrackFindingTracklet.L1TrackletEmulationTracks_cff")
process.TTTracksEmulation = cms.Path(process.L1TrackletEmulationTracks)
process.TTTracksEmulationWithTruth = cms.Path(process.L1TrackletEmulationTracksWithAssociators)


############################################################
# Define the track ntuple process, MyProcess is the (unsigned) PDGID corresponding to the process which is run
# e.g. single electron/positron = 11
#      single pion+/pion- = 211
#      single muon+/muon- = 13 
#      pions in jets = 6
#      taus = 15
#      all TPs = 1
############################################################

process.L1TrackNtuple = cms.EDAnalyzer('L1TrackNtupleMaker',
                                       MyProcess = cms.int32(1),
                                       DebugMode = cms.bool(False),      # printout lots of debug statements
                                       SaveAllTracks = cms.bool(True),   # save *all* L1 tracks, not just truth matched to primary particle
                                       SaveStubs = cms.bool(False),      # save some info for *all* stubs
                                       SaveTPs = cms.bool(False),
                                       LooseMatch = cms.bool(True),      # allow loosely genuine matching?
                                       L1Tk_nPar = cms.int32(4),         # use 4 or 5-parameter L1 track fit ??
                                       L1Tk_minNStub = cms.int32(4),     # L1 tracks with >= 4 stubs
                                       L1Tk_maxZ0 = cms.double(20.0),
                                       TP_minNStub = cms.int32(4),       # require TP to have >= X number of stubs associated with it
                                       TP_minNStubLayer = cms.int32(4),  # require TP to have stubs in >= X layers/disks
                                       TP_minPt = cms.double(2.0),       # only save TPs with pt > X GeV
                                       TP_maxEta = cms.double(2.5),      # only save TPs with |eta| < X
                                       TP_maxZ0 = cms.double(30.0),      # only save TPs with |z0| < X cm
                                       #L1TrackInputTag = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks"),                 ## TTTrack input
                                       L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks"),         ## TTTrack input
                                       MCTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks"),  ## MCTruth input 
                                       # other input collections
                                       L1StubInputTag = cms.InputTag("TTStubsFromPhase2TrackerDigis","StubAccepted"),
                                       MCTruthClusterInputTag = cms.InputTag("TTClusterAssociatorFromPixelDigis", "ClusterAccepted"),
                                       MCTruthStubInputTag = cms.InputTag("TTStubAssociatorFromPixelDigis", "StubAccepted"),
                                       TrackingParticleInputTag = cms.InputTag("mix", "MergedTrackTruth"),
                                       TrackingVertexInputTag = cms.InputTag("mix", "MergedTrackTruth")
                                       ## tracking in jets stuff (--> requires AK4 genjet collection present!)
                                       )
process.ana = cms.Path(process.L1TrackNtuple)

# use this if you want to re-run the stub making
#process.schedule = cms.Schedule(process.TTClusterStub,process.TTClusterStubTruth,process.TTTracksEmulationWithTruth,process.ana)

# use this if cluster/stub associators not available 
#process.schedule = cms.Schedule(process.TTClusterStubTruth,process.TTTracksEmulationWithTruth,process.ana)

# use this to only run tracking + track associator
#process.schedule = cms.Schedule(process.TTTracksWithTruth,process.ana)            # floating-point simulation
process.schedule = cms.Schedule(process.TTTracksEmulationWithTruth,process.ana)    # emulation

