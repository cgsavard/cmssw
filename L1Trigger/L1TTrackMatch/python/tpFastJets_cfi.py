import FWCore.ParameterSet.Config as cms
from . import jetcuts

tpFastJets = cms.EDProducer("TPFastJetProducer",
    L1PrimaryVertexTag=cms.InputTag("l1tVertexFinder", "L1Vertices"),
    TrackingParticleInputTag = cms.InputTag("mix", "MergedTrackTruth"),
    MCTruthStubInputTag = cms.InputTag("TTStubAssociatorFromPixelDigis", "StubAccepted"),
    tp_ptMin = cms.double(2.0),       # minimum tp pt [GeV]
    tp_etaMax = cms.double(2.4),      # maximum tp eta
    tp_zMax = cms.double(15.),        # max tp z0 [cm]
    tp_nStubMin = cms.int32(4),       # minimum number of stubs
    tp_nStubLayerMin = cms.int32(4),  # minimum number of layers with stubs 
    minBias = cms.bool(jetcuts.minbias),        # when running on MinBias sample, use dz cut for PU removal
    deltaZ0Cut=cms.double(jetcuts.dz),       # cluster tracks within |dz|<X, 0.5 normally, 100 to turn off
    coneSize=cms.double(0.4),         # cone size for anti-kt fast jet 
)
