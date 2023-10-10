///////////////////////////////////////////////////////////////////////////
//                                                                       //
// Producer of TkJet,                                                    //
// Cluster L1 tracks using fastjet                                       //
//                                                                       //
///////////////////////////////////////////////////////////////////////////

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "DataFormats/Common/interface/Handle.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/CommonDetUnit/interface/PixelGeomDetUnit.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "DataFormats/Math/interface/LorentzVector.h"

// L1 objects
#include "DataFormats/L1TrackTrigger/interface/TTTypes.h"
#include "DataFormats/L1TCorrelator/interface/TkJet.h"
#include "DataFormats/L1TCorrelator/interface/TkJetFwd.h"
#include "DataFormats/L1Trigger/interface/Vertex.h"
#include "DataFormats/L1TrackTrigger/interface/TTStub.h"

// truth object
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimTracker/TrackTriggerAssociation/interface/TTStubAssociationMap.h"

// geometry
#include "Geometry/Records/interface/TrackerTopologyRcd.h"
#include "DataFormats/TrackerCommon/interface/TrackerTopology.h"

#include <fastjet/JetDefinition.hh>

#include <string>
#include "TMath.h"
#include "TH1.h"

using namespace l1t;
using namespace edm;
using namespace std;

//////////////////////////////
//                          //
//     CLASS DEFINITION     //
//                          //
//////////////////////////////

class TPFastJetProducer : public edm::stream::EDProducer<> {
public:

  explicit TPFastJetProducer(const edm::ParameterSet&);
  ~TPFastJetProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  //virtual void beginJob();
  void produce(edm::Event&, const edm::EventSetup&) override;
  //virtual void endJob();

  // track selection criteria
  const float tpPtMin_;
  const float tpEtaMax_;
  const float tpZMax_;
  const int tpNStubMin_;
  const int tpNStubLayerMin_;
  const bool minBias_;
  const float coneSize_;        // Use anti-kt with this cone size
  const float deltaZ0Cut_;

  edm::EDGetTokenT<std::vector<TrackingParticle> > trackingParticleToken_;
  edm::EDGetTokenT<TTStubAssociationMap<Ref_Phase2TrackerDigi_> > ttStubMCTruthToken_;
  edm::EDGetTokenT<VertexCollection> pvToken_;
  edm::ESGetToken<TrackerTopology, TrackerTopologyRcd> tTopoToken_;
};

// constructor
TPFastJetProducer::TPFastJetProducer(const edm::ParameterSet& iConfig)
    : tpPtMin_((float)iConfig.getParameter<double>("tp_ptMin")),
      tpEtaMax_((float)iConfig.getParameter<double>("tp_etaMax")),
      tpZMax_((float)iConfig.getParameter<double>("tp_zMax")),
      tpNStubMin_((int)iConfig.getParameter<int>("tp_nStubMin")),
      tpNStubLayerMin_((int)iConfig.getParameter<int>("tp_nStubLayerMin")),
      minBias_((bool)iConfig.getParameter<bool>("minBias")),
      coneSize_((float)iConfig.getParameter<double>("coneSize")),
      deltaZ0Cut_((float)iConfig.getParameter<double>("deltaZ0Cut")),
      trackingParticleToken_(consumes<std::vector<TrackingParticle> >(iConfig.getParameter<edm::InputTag>("TrackingParticleInputTag"))),
      ttStubMCTruthToken_(consumes<TTStubAssociationMap<Ref_Phase2TrackerDigi_> >(iConfig.getParameter<edm::InputTag>("MCTruthStubInputTag"))),
      pvToken_(consumes<VertexCollection>(iConfig.getParameter<edm::InputTag>("L1PrimaryVertexTag"))),
      tTopoToken_(esConsumes<TrackerTopology, TrackerTopologyRcd>(edm::ESInputTag("", ""))) {
  produces<TkJetCollection>("TPFastJets");
}

// destructor
TPFastJetProducer::~TPFastJetProducer() {}

// producer
void TPFastJetProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  std::unique_ptr<TkJetCollection> TPFastJets(new TkJetCollection);

  // Tracking particles
  edm::Handle<std::vector<TrackingParticle>> TrackingParticleHandle;
  iEvent.getByToken(trackingParticleToken_, TrackingParticleHandle);
  std::vector<TrackingParticle>::const_iterator iterTP;

  // MC truth association maps
  edm::Handle<TTStubAssociationMap<Ref_Phase2TrackerDigi_> > MCTruthTTStubHandle;
  iEvent.getByToken(ttStubMCTruthToken_, MCTruthTTStubHandle);

  // Tracker Topology
  const TrackerTopology& tTopo = iSetup.getData(tTopoToken_);

  // Reco PV
  edm::Handle<l1t::VertexCollection> L1PrimaryVertexHandle;
  iEvent.getByToken(pvToken_, L1PrimaryVertexHandle);
  float recoVtx = L1PrimaryVertexHandle->begin()->z0();

  fastjet::JetDefinition jet_def(fastjet::antikt_algorithm, coneSize_);
  std::vector<fastjet::PseudoJet> JetInputs;

  unsigned int this_tp = 0;
  for (iterTP = TrackingParticleHandle->begin(); iterTP != TrackingParticleHandle->end(); iterTP++) {
    edm::Ptr<TrackingParticle> tp_ptr(TrackingParticleHandle, this_tp);
    this_tp++;

    float tp_pt = iterTP->pt();
    float tp_eta = iterTP->eta();
    float tp_charge = iterTP->charge();
    //float tp_vz = iterTP->vz(); // parent vtx z
    float tp_z0 = iterTP->z0(); // track z with respect to (0,0,0)
    int tp_eventid = iterTP->eventId().event();

    std::vector<edm::Ref<edmNew::DetSetVector<TTStub<Ref_Phase2TrackerDigi_> >, TTStub<Ref_Phase2TrackerDigi_> > >
      theStubRefs = MCTruthTTStubHandle->findTTStubRefs(tp_ptr);
    int nStubTP = (int)theStubRefs.size();

    // how many layers/disks have stubs?
    int hasStubInLayer[11] = {0};
    for (auto& theStubRef : theStubRefs) {
      DetId detid(theStubRef->getDetId());

      int layer = -1;
      if (detid.subdetId() == StripSubdetector::TOB) {
        layer = static_cast<int>(tTopo.layer(detid)) - 1;  //fill in array as entries 0-5
      } else if (detid.subdetId() == StripSubdetector::TID) {
        layer = static_cast<int>(tTopo.layer(detid)) + 5;  //fill in array as entries 6-10
      }

      //treat genuine stubs separately (==2 is genuine, ==1 is not)
      if (MCTruthTTStubHandle->findTrackingParticlePtr(theStubRef).isNull() && hasStubInLayer[layer] < 2)
        hasStubInLayer[layer] = 1;
      else
        hasStubInLayer[layer] = 2;
    }

    int nStubLayerTP = 0;
    int nStubLayerTP_g = 0;
    for (int isum : hasStubInLayer) {
      if (isum >= 1)
        nStubLayerTP += 1;
      if (isum == 2)
        nStubLayerTP_g += 1;
    }

    if (tp_pt < tpPtMin_)  // Save CPU by applying these cuts here.
      continue;
    if (tp_charge == 0.)
      continue;
    if (fabs(tp_eta) > tpEtaMax_)
      continue;
    if (nStubTP < tpNStubMin_)
      continue;
    if (nStubLayerTP < tpNStubLayerMin_)
      continue;
    if (fabs(tp_z0) > tpZMax_)
      continue;
    if ((std::abs(recoVtx - tp_z0) > deltaZ0Cut_) && minBias_)
      continue;
    if (!minBias_ && tp_eventid>0)
      continue;

    fastjet::PseudoJet psuedoJet(iterTP->px(),
                                 iterTP->py(),
                                 iterTP->pz(),
                                 iterTP->energy());
    JetInputs.push_back(psuedoJet);                     // input tracks for clustering
    JetInputs.back().set_user_index(this_tp - 1);  // save track index in the collection
  }                                                     // end loop over tracks

  fastjet::ClusterSequence cs(JetInputs, jet_def);  // define the output jet collection
  std::vector<fastjet::PseudoJet> JetOutputs =
      fastjet::sorted_by_pt(cs.inclusive_jets(0));  // output jet collection, pT-ordered

  for (unsigned int ijet = 0; ijet < JetOutputs.size(); ++ijet) {
    math::XYZTLorentzVector jetP4(
        JetOutputs[ijet].px(), JetOutputs[ijet].py(), JetOutputs[ijet].pz(), JetOutputs[ijet].modp());
    float sumpt = 0;
    float avgZ = 0;
    std::vector<edm::Ptr<TrackingParticle> > tpPtrs;
    std::vector<fastjet::PseudoJet> fjConstituents = fastjet::sorted_by_pt(cs.constituents(JetOutputs[ijet]));

    for (unsigned int i = 0; i < fjConstituents.size(); ++i) {
      auto index = fjConstituents[i].user_index();
      edm::Ptr<TrackingParticle> tpPtr(TrackingParticleHandle, index);
      tpPtrs.push_back(tpPtr);  // tracking particles in the jet
      sumpt = sumpt + tpPtr->pt();
      avgZ = avgZ + tpPtr->pt() * tpPtr->z0();
    }
    avgZ = avgZ / sumpt;
    edm::Ref<JetBxCollection> jetRef;
    std::vector<edm::Ptr<TTTrack<Ref_Phase2TrackerDigi_>> > dummyL1TrackPtrs; // can't create TkJet with tps
    TkJet tpJet(jetP4, dummyL1TrackPtrs, avgZ, fjConstituents.size(), 0, 0, 0, false);
    //TkJet tpJet(jetP4, jetRef, dummyL1TrackPtrs, avgZ);
    TPFastJets->push_back(tpJet);
  }  //end loop over Jet Outputs

  iEvent.put(std::move(TPFastJets), "TPFastJets");
}

//void TPFastJetProducer::beginJob() {}

//void TPFastJetProducer::endJob() {}

void TPFastJetProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(TPFastJetProducer);
