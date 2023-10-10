import FWCore.ParameterSet.Config as cms
from . import jetcuts

l1tTrackFastJets = cms.EDProducer("L1TrackFastJetProducer",
    L1TrackInputTag = cms.InputTag("l1tTTTracksFromTrackletEmulation", "Level1TTTracks"),
    L1PrimaryVertexTag=cms.InputTag("l1tVertexFinder", "L1Vertices"),
    trk_zMax = cms.double(15.),       # max track z0 [cm]
    trk_chi2dofMax = cms.double(jetcuts.chi2dof), # max track chi2/dof, ORIGINALLY 10.
    trk_chi2rzMax = cms.double(10000.),
    trk_chi2rphiMax = cms.double(10000.),
    trk_mvaMin = cms.double(jetcuts.mva),
    tightBarrel = cms.bool(jetcuts.tight_barrel),
    trk_barrelMvaMin = cms.double(jetcuts.barrel_mva),
    barrelMaxDzTrackPV = cms.double(jetcuts.barrel_dz),
    trk_bendChi2Max = cms.double(jetcuts.bendchi2),# max bendChi2 cut, ORIGINALLY 2.2
    trk_ptMin = cms.double(2.0),      # minimum track pt [GeV]
    trk_etaMax = cms.double(2.4),     # maximum track eta, ORIGINALLY 2.5
    trk_nStubMin = cms.int32(4),      # minimum number of stubs in track
    trk_nPSStubMin = cms.int32(-1),   # minimum number of PS stubs in track
    deltaZ0Cut=cms.double(jetcuts.dz),       # cluster tracks within |dz|<X, ORIGINALLY 0.5
    doTightDz = cms.bool(False), # ORIGINALLY FALSE
    trk_ptTightDz = cms.double(10.0),
    trk_dzTightDz = cms.double(0.5),
    doTightChi2 = cms.bool(jetcuts.tightchi2),   # chi2dof < 5 for tracks with PT > 20, ORIGINALLY True
    trk_ptTightChi2 = cms.double(20.0),
    trk_chi2dofTightChi2 = cms.double(5.0),
    coneSize=cms.double(0.4),         #cone size for anti-kt fast jet
    displaced = cms.bool(False)       # use prompt/displaced tracks
)

l1tTrackFastJetsExtended = cms.EDProducer("L1TrackFastJetProducer",
    L1TrackInputTag = cms.InputTag("l1tTTTracksFromExtendedTrackletEmulation", "Level1TTTracks"),
    L1PrimaryVertexTag=cms.InputTag("l1tVertexFinder", "L1Vertices"),
    trk_zMax = cms.double(15.),       # max track z0 [cm]
    trk_chi2dofMax = cms.double(40.),    # max track chi2 for extended tracks
    trk_bendChi2Max = cms.double(2.4),#Bendchi2 cut for extended tracks
    trk_ptMin = cms.double(3.0),      # minimum track pt [GeV]
    trk_etaMax = cms.double(2.5),     # maximum track eta
    trk_nStubMin = cms.int32(4),      # minimum number of stubs on track
    trk_nPSStubMin = cms.int32(-1),   # minimum number of stubs in PS modules on track
    deltaZ0Cut=cms.double(3.0),       #cluster tracks within |dz|<X
    doTightChi2 = cms.bool( True ),   # chi2dof < 5 for tracks with PT > 20
    trk_ptTightChi2 = cms.double(20.0),
    trk_chi2dofTightChi2 = cms.double(5.0),
    coneSize=cms.double(0.4),         #cone size for anti-kt fast jet
    displaced = cms.bool(True)        # use prompt/displaced tracks
)
