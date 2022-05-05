############################################################
# define basic process
############################################################

import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
import os

############################################################
# edit options here
############################################################
L1TRK_INST ="MyL1TrackJets" ### if not in input DIGRAW then we make them in the above step
process = cms.Process(L1TRK_INST)

############################################################
# import standard configurations
############################################################

process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.INFO.limit = cms.untracked.int32(0) # default: 0

############################################################
# input and output
############################################################

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))

readFiles = cms.untracked.vstring(
#    '/store/relval/CMSSW_11_3_0_pre3/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU_113X_mcRun4_realistic_v3_2026D49PU200_rsb-v1/00000/00260a30-734a-4a3a-a4b0-f836ce5502c6.root'
'/store/mc/Phase2HLTTDRWinter20DIGI/TT_TuneCP5_14TeV-powheg-pythia8/GEN-SIM-DIGI-RAW/PU200_110X_mcRun4_realistic_v3-v2/110000/005E74D6-B50E-674E-89E6-EAA9A617B476.root'
)
secFiles = cms.untracked.vstring()

process.source = cms.Source ("PoolSource",
                            fileNames = readFiles,
                            secondaryFileNames = secFiles,
                            duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
                            )


process.TFileService = cms.Service("TFileService", fileName = cms.string('vtx_ttbar200PU.root'), closeFileFast = cms.untracked.bool(True))


############################################################
# L1 tracking: remake stubs?
############################################################
process.load('L1Trigger.VertexFinder.VertexProducer_cff')
process.load("L1Trigger.L1TTrackMatch.L1GTTInputProducer_cfi")
process.load("L1Trigger.TrackFindingTracklet.L1HybridEmulationTracks_cff")



############################################################
# Primary vertex
############################################################
process.L1VertexFinder = process.VertexProducer.clone()
process.pPV = cms.Path(process.L1VertexFinder)
process.L1VertexFinderEmulator = process.VertexProducer.clone()
process.L1VertexFinderEmulator.VertexReconstruction.Algorithm = "fastHistoEmulation"
process.L1VertexFinderEmulator.l1TracksInputTag = cms.InputTag("L1GTTInputProducer","Level1TTTracksConverted")
process.pPVemu = cms.Path(process.L1VertexFinderEmulator)

process.TTTracksEmu = cms.Path(process.L1HybridTracks)
process.TTTracksEmuWithTruth = cms.Path(process.L1HybridTracksWithAssociators)
process.pL1GTTInput = cms.Path(process.L1GTTInputProducer)


############################################################
# Define the track ntuple process, MyProcess is the (unsigned) PDGID corresponding to the process which is run
# e.g. single electron/positron = 11
#      single pion+/pion- = 211
#      single muon+/muon- = 13
#      pions in jets = 6
#      taus = 15
#      all TPs = 1
############################################################

process.L1TrackNtuple = cms.EDAnalyzer('L1VertexNtupleMaker',
        MyProcess = cms.int32(1),
        DebugMode = cms.bool(False),      # printout lots of debug statements
        GenParticleInputTag = cms.InputTag("genParticles",""),
        RecoVertexInputTag=cms.InputTag("L1VertexFinder", "l1vertices"),
        RecoVertexEmuInputTag=cms.InputTag("L1VertexFinderEmulator", "l1verticesEmulation"),
)

process.ntuple = cms.Path(process.L1TrackNtuple)

process.out = cms.OutputModule( "PoolOutputModule",
                                fastCloning = cms.untracked.bool( False ),
                                fileName = cms.untracked.string("test.root" )
		               )
process.pOut = cms.EndPath(process.out)


process.schedule = cms.Schedule(process.TTTracksEmuWithTruth, process.pL1GTTInput, process.pPV, process.pPVemu)
#process.schedule = cms.Schedule(process.pPV, process.pPVemu, process.ntuple)
#process.schedule = cms.Schedule(process.pPV, process.ntuple)
