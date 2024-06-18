from CRABClient.UserUtilities import config#, getUsernameFromSiteDB
config = config()

config.General.workArea = 'crab_output'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'L1TrackNtupleMaker_cfg.py'

# ---TTbar 200PU---
config.General.requestName = 'TTbar_200PU_D88_extended' 
config.Data.inputDataset = '/TT_TuneCP5_14TeV-powheg-pythia8/Phase2Spring23DIGIRECOMiniAOD-PU200_L1TFix_Trk1GeV_131X_mcRun4_realistic_v9-v1/GEN-SIM-DIGI-RAW-MINIAOD'
config.Data.outputDatasetTag = 'TTbar_200PU_D88_extended'
config.Data.totalUnits = 100 
config.Data.unitsPerJob = 5

# ---DispMu 0PU--- WANT A 200PU SAMPLE BUT NOT CURRENTLY AVAILABLE
#config.General.requestName = 'DispSingleMu_0PU_D98_extended'
#config.Data.inputDataset = '/RelValDisplacedSingleMuFlatPt2To100/CMSSW_14_0_0_pre2-133X_mcRun4_realistic_v1_STD_2026D98_noPU_RV229-v1/GEN-SIM-DIGI-RAW'
#config.Data.outputDatasetTag = 'DispSingleMu_0PU_D98_extended'
#config.Data.totalUnits = 100
#config.Data.unitsPerJob = 20

# ---NuGun---
#config.General.requestName = 'NuGun_200PU_D98_extended'
#config.Data.inputDataset = '/RelValNuGun/CMSSW_14_0_0_pre2-PU_133X_mcRun4_realistic_v1_STD_2026D98_PU200-v3/GEN-SIM-DIGI-RAW'
#config.Data.outputDatasetTag = 'NuGun_200PU_D98_extended'
#config.Data.totalUnits = 100
#config.Data.unitsPerJob = 10
#config.Data.partialDataset = True #only process what's on disk, not tape

# ---GGH---
#config.General.requestName = 'GGH_200PU_D98_extended'
#config.Data.inputDataset = '/HiddenGluGluH_mH-125_Phi-30_ctau-100_bbbb_TuneCP5_14TeV-pythia8/Phase2Spring23DIGIRECOMiniAOD-PU200_L1TFix_131X_mcRun4_realistic_v9-v1/GEN-SIM-DIGI-RAW-MINIAOD'
#config.Data.outputDatasetTag = 'GGH_200PU_D98_extended'
#config.Data.totalUnits = 50
#config.Data.unitsPerJob = 5

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.outLFNDirBase = '/store/user/csavard/'
#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = False

config.Site.storageSite = 'T3_US_FNALLPC'

