//////////////////////////////////////////////////////////////////////
//                                                                  //
//  Analyzer for making mini-ntuple for L1 track performance plots  //
//                                                                  //
//////////////////////////////////////////////////////////////////////

////////////////////
// FRAMEWORK HEADERS
#include "FWCore/PluginManager/interface/ModuleDef.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

///////////////////////
// DATA FORMATS HEADERS
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Common/interface/Ref.h"

#include "DataFormats/L1TrackTrigger/interface/TTTypes.h"
#include "DataFormats/L1TrackTrigger/interface/TTCluster.h"
#include "DataFormats/L1TrackTrigger/interface/TTStub.h"
#include "DataFormats/L1TrackTrigger/interface/TTTrack.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingParticle.h"
#include "SimDataFormats/TrackingAnalysis/interface/TrackingVertex.h"
#include "SimDataFormats/TrackingHit/interface/PSimHitContainer.h"
#include "SimDataFormats/TrackingHit/interface/PSimHit.h"
#include "SimTracker/TrackTriggerAssociation/interface/TTClusterAssociationMap.h"
#include "SimTracker/TrackTriggerAssociation/interface/TTStubAssociationMap.h"
#include "SimTracker/TrackTriggerAssociation/interface/TTTrackAssociationMap.h"
#include "Geometry/Records/interface/StackedTrackerGeometryRecord.h"

#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/GenJet.h"

////////////////////////////
// DETECTOR GEOMETRY HEADERS
#include "MagneticField/Engine/interface/MagneticField.h"
#include "MagneticField/Records/interface/IdealMagneticFieldRecord.h"
#include "Geometry/TrackerGeometryBuilder/interface/TrackerGeometry.h"
#include "Geometry/Records/interface/TrackerDigiGeometryRecord.h"
#include "Geometry/TrackerGeometryBuilder/interface/RectangularPixelTopology.h"
#include "Geometry/CommonDetUnit/interface/GeomDetType.h"
#include "Geometry/CommonDetUnit/interface/GeomDet.h"

#include "Geometry/CommonTopologies/interface/PixelGeomDetUnit.h"
#include "Geometry/CommonTopologies/interface/PixelGeomDetType.h"
#include "Geometry/TrackerGeometryBuilder/interface/PixelTopologyBuilder.h"
#include "Geometry/Records/interface/StackedTrackerGeometryRecord.h"

////////////////
// PHYSICS TOOLS
#include "CommonTools/UtilAlgos/interface/TFileService.h"

//My additions
#include "DataFormats/L1TCorrelator/interface/TkJet.h"
#include "DataFormats/L1TCorrelator/interface/TkJetFwd.h"
#include "DataFormats/L1Trigger/interface/TkJetWord.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/L1TCorrelator/interface/TkEtMiss.h"
#include "DataFormats/L1TCorrelator/interface/TkEtMissFwd.h"
#include "DataFormats/L1TCorrelator/interface/TkHTMiss.h"
#include "DataFormats/L1TCorrelator/interface/TkHTMissFwd.h"
#include "DataFormats/L1Trigger/interface/Vertex.h"
#include "DataFormats/L1Trigger/interface/VertexWord.h"
#include "DataFormats/L1Trigger/interface/EtSum.h"
#include "L1Trigger/L1TTrackMatch/interface/L1TkEtMissEmuAlgo.h"
#include "L1Trigger/L1TTrackMatch/interface/L1TkHTMissEmulatorProducer.h"

///////////////
// ROOT HEADERS
#include <TROOT.h>
#include <TCanvas.h>
#include <TTree.h>
#include <TFile.h>
#include <TF1.h>
#include <TH2F.h>
#include <TH1F.h>
#include <TLorentzVector.h>

//////////////
// STD HEADERS
#include <memory>
#include <string>
#include <iostream>

//////////////
// NAMESPACES
using namespace std;
using namespace edm;

//////////////////////////////
//                          //
//     CLASS DEFINITION     //
//                          //
//////////////////////////////

class L1VertexNtupleMaker : public edm::one::EDAnalyzer<edm::one::SharedResources> {
private:
  // ----------constants, enums and typedefs ---------
  typedef TTTrack<Ref_Phase2TrackerDigi_> L1Track;
  typedef edm::Ptr<L1Track> L1TrackPtr;
  typedef std::vector<L1TrackPtr> L1TrackPtrCollection;
  typedef std::vector<L1Track> L1TrackCollection;
  typedef edm::Ref<L1TrackCollection> L1TrackRef;
  typedef std::vector<L1TrackRef> L1TrackRefCollection;

public:
  // Constructor/destructor
  explicit L1VertexNtupleMaker(const edm::ParameterSet& iConfig);
  ~L1VertexNtupleMaker() override;

  // Mandatory methods
  void beginJob() override;
  void endJob() override;
  void analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) override;

  // Other member functions
  int getSelectedTrackIndex(const L1TrackRef& trackRef,
                            const edm::Handle<L1TrackRefCollection>& selectedTrackRefs) const;

private:
  //-----------------------------------------------------------------------------------------------
  // Containers of parameters passed by python configuration file
  edm::ParameterSet config;

  int MyProcess;       // 11/13/211 for single electrons/muons/pions, 6/15 for pions from ttbar/taus, 1 for inclusive
  bool DebugMode;      // lots of debug printout statements

  edm::InputTag RecoVertexInputTag;
  edm::InputTag RecoVertexEmuInputTag;
  edm::InputTag GenParticleInputTag;

  edm::EDGetTokenT<std::vector<reco::GenParticle>> GenParticleToken_;
  edm::EDGetTokenT<l1t::VertexCollection> L1VertexToken_;
  edm::EDGetTokenT<l1t::VertexWordCollection> L1VertexEmuToken_;

  //-----------------------------------------------------------------------------------------------
  // tree & branches for mini-ntuple
  bool available_;  // ROOT file for histograms is open.
  TTree* eventTree;

  // primary vertex
  std::vector<float>* m_pv_L1reco;
  std::vector<float>* m_pv_L1reco_sum;
  std::vector<float>* m_pv_L1reco_emu;
  std::vector<float>* m_pv_MC;
  std::vector<int>* m_MC_lep;
};

//////////////////////////////////
//                              //
//     CLASS IMPLEMENTATION     //
//                              //
//////////////////////////////////

//////////////
// CONSTRUCTOR
L1VertexNtupleMaker::L1VertexNtupleMaker(edm::ParameterSet const& iConfig) : config(iConfig) {
  MyProcess = iConfig.getParameter<int>("MyProcess");
  DebugMode = iConfig.getParameter<bool>("DebugMode");
 
  RecoVertexInputTag = iConfig.getParameter<InputTag>("RecoVertexInputTag");
  RecoVertexEmuInputTag = iConfig.getParameter<InputTag>("RecoVertexEmuInputTag");
  GenParticleInputTag = iConfig.getParameter<InputTag>("GenParticleInputTag");

  GenParticleToken_ = consumes<std::vector<reco::GenParticle>>(GenParticleInputTag);
  L1VertexToken_ = consumes<l1t::VertexCollection>(RecoVertexInputTag);
  L1VertexEmuToken_ = consumes<l1t::VertexWordCollection>(RecoVertexEmuInputTag);

  usesResource(TFileService::kSharedResource);
}

/////////////
// DESTRUCTOR
L1VertexNtupleMaker::~L1VertexNtupleMaker() {}

//////////
// END JOB
void L1VertexNtupleMaker::endJob() {
  // things to be done at the exit of the event Loop
  //  edm::LogVerbatim("Tracklet") << "L1VertexNtupleMaker::endJob";
}

////////////
// BEGIN JOB
void L1VertexNtupleMaker::beginJob() {
  // things to be done before entering the event Loop
  //  edm::LogVerbatim("Tracklet") << "L1VertexNtupleMaker::beginJob";

  //-----------------------------------------------------------------------------------------------
  // book histograms / make ntuple
  edm::Service<TFileService> fs;
  available_ = fs.isAvailable();
  if (not available_)
    return;  // No ROOT file open.

  //initialize
  m_pv_L1reco = new std::vector<float>;
  m_pv_L1reco_sum = new std::vector<float>;
  m_pv_L1reco_emu = new std::vector<float>;
  m_pv_MC = new std::vector<float>;
  m_MC_lep = new std::vector<int>;

  // ntuple
  eventTree = fs->make<TTree>("eventTree", "Event tree");
  eventTree->Branch("pv_L1reco", &m_pv_L1reco);
  eventTree->Branch("pv_L1reco_sum", &m_pv_L1reco_sum);
  eventTree->Branch("pv_L1reco_emu", &m_pv_L1reco_emu);
  eventTree->Branch("MC_lep", &m_MC_lep);
  eventTree->Branch("pv_MC", &m_pv_MC);
}

//////////
// ANALYZE
void L1VertexNtupleMaker::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup) {
  if (not available_)
    return;  // No ROOT file open.

  if (!(MyProcess == 13 || MyProcess == 11 || MyProcess == 211 || MyProcess == 6 || MyProcess == 15 ||
        MyProcess == 1)) {
    edm::LogVerbatim("Tracklet") << "The specified MyProcess is invalid! Exiting...";
    return;
  }

  // clear variables
  m_pv_L1reco->clear();
  m_pv_L1reco_sum->clear();
  m_pv_L1reco_emu->clear();
  m_pv_MC->clear();
  m_MC_lep->clear();

  // -----------------------------------------------------------------------------------------------
  // retrieve various containers
  // -----------------------------------------------------------------------------------------------

  //Gen particles
  edm::Handle<std::vector<reco::GenParticle> > GenParticleHandle;
  iEvent.getByToken(GenParticleToken_, GenParticleHandle);

  //Vertex
  edm::Handle<l1t::VertexCollection> L1TkPrimaryVertexHandle;
  iEvent.getByToken(L1VertexToken_, L1TkPrimaryVertexHandle);
  std::vector<l1t::Vertex>::const_iterator vtxIter;

  edm::Handle<l1t::VertexWordCollection> L1TkPrimaryVertexEmuHandle;
  iEvent.getByToken(L1VertexEmuToken_, L1TkPrimaryVertexEmuHandle);
  std::vector<l1t::VertexWord>::const_iterator vtxEmuIter;

  //Loop over gen particles  
  if (GenParticleHandle.isValid()) {
    vector<reco::GenParticle>::const_iterator genpartIter;

    float zvtx_gen = -999;
    for (genpartIter = GenParticleHandle->begin(); genpartIter != GenParticleHandle->end(); ++genpartIter) {
      int status = genpartIter->status();
      if (status != 1)
        continue;
      zvtx_gen = genpartIter->vz();  //for gen vertex
    }

    m_pv_MC->push_back(zvtx_gen);
  
  } else {
    edm::LogWarning("DataNotFound") << "\nWarning: GenParticleHandle not found in the event" << std::endl;
  }

  //Primary reco vertex
  if (L1TkPrimaryVertexHandle.isValid()) {
    for (vtxIter = L1TkPrimaryVertexHandle->begin(); vtxIter != L1TkPrimaryVertexHandle->end(); ++vtxIter) {
      m_pv_L1reco->push_back(vtxIter->z0());
      m_pv_L1reco_sum->push_back(vtxIter->pt());
    }
  } else
    edm::LogWarning("DataNotFound") << "\nWarning: L1TkPrimaryVertexHandle not found" << std::endl;

  if (L1TkPrimaryVertexEmuHandle.isValid()) {
    for (vtxEmuIter = L1TkPrimaryVertexEmuHandle->begin(); vtxEmuIter != L1TkPrimaryVertexEmuHandle->end();
         ++vtxEmuIter) {
      m_pv_L1reco_emu->push_back(vtxEmuIter->z0());
    }
  } else
    edm::LogWarning("DataNotFound") << "\nWarning: L1TkPrimaryVertexEmuHandle not found" << std::endl;

  eventTree->Fill();
}  // end of analyze()

int L1VertexNtupleMaker::getSelectedTrackIndex(const L1TrackRef& trackRef,
                                                    const edm::Handle<L1TrackRefCollection>& selectedTrackRefs) const {
  auto it = std::find_if(selectedTrackRefs->begin(), selectedTrackRefs->end(), [&trackRef](L1TrackRef const& obj) {
    return obj == trackRef;
  });
  if (it != selectedTrackRefs->end())
    return std::distance(selectedTrackRefs->begin(), it);
  else
    return -1;
}

///////////////////////////
// DEFINE THIS AS A PLUG-IN
DEFINE_FWK_MODULE(L1VertexNtupleMaker);
