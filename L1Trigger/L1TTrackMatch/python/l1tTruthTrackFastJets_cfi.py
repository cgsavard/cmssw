import FWCore.ParameterSet.Config as cms
from . import jetcuts

l1tTruthTrackFastJets = cms.EDProducer("L1TruthTrackFastJetProducer",
    L1PrimaryVertexTag=cms.InputTag("l1tVertexFinder", "L1Vertices"),
    L1TrackInputTag = cms.InputTag("l1tTTTracksFromTrackletEmulation", "Level1TTTracks"),
    MCTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks"),
    trk_zMax = cms.double(15.),       # max track z0 [cm]
    trk_ptMin = cms.double(2.0),      # minimum track pt [GeV]
    trk_etaMax = cms.double(2.4),     # maximum track eta
    trk_nStubMin = cms.int32(4),      # minimum number of stubs in track
    trk_nPSStubMin = cms.int32(-1),   # minimum number of PS stubs in track
    minBias = cms.bool(jetcuts.minbias),        # when running on MinBias sample, use dz cut for PU removal
    deltaZ0Cut = cms.double(jetcuts.dz),     # cluster tracks within |dz|<X, 0.5 normally, 100 to turn off 
    coneSize = cms.double(0.4),       #cone size for anti-kt fast jet
    displaced = cms.bool(False)       # use prompt/displaced tracks
)

l1tTruthTrackFastJetsExtended = cms.EDProducer("L1TruthTrackFastJetProducer",
    L1TrackInputTag = cms.InputTag("l1tTTTracksFromExtendedTrackletEmulation", "Level1TTTracks"),
    MCTruthTrackInputTag = cms.InputTag("TTTrackAssociatorFromPixelDigis", "Level1TTTracks"),
    trk_zMax = cms.double(15.),       # max track z0 [cm]
    trk_ptMin = cms.double(3.0),      # minimum track pt [GeV]
    trk_etaMax = cms.double(2.5),     # maximum track eta
    trk_nStubMin = cms.int32(4),      # minimum number of stubs on track
    trk_nPSStubMin = cms.int32(-1),   # minimum number of stubs in PS modules on track
    coneSize=cms.double(0.4),         #cone size for anti-kt fast jet
    displaced = cms.bool(True)        # use prompt/displaced tracks
)
