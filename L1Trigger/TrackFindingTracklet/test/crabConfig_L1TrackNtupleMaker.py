from CRABClient.UserUtilities import config#, getUsernameFromSiteDB
config = config()

config.General.workArea = 'crab_output'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'L1TrackNtupleMaker_cfg.py'

# ---DispMu 200PU---
#config.General.requestName = 'DispMu_200PU_D76_extended_notrunc'
#config.Data.inputDataset = '/RelValDisplacedMuPt2To100Dxy100/CMSSW_11_3_0_pre6-PU_113X_mcRun4_realistic_v6_2026D76PU200-v2/GEN-SIM-DIGI-RAW'
#config.Data.outputDatasetTag = 'DispMu_200PU_D76_extended_notrunc'
#config.Data.totalUnits = 1000
#config.Data.unitsPerJob = 20

# ---DispMu noPU---
#config.General.requestName = 'DispMu_noPU_D76_extended_notrunc'  
#config.Data.inputDataset = '/RelValDisplacedMuPt2To100Dxy100/CMSSW_11_3_0_pre6-113X_mcRun4_realistic_v6_2026D76noPU-v1/GEN-SIM-DIGI-RAW'
#config.Data.outputDatasetTag = 'DispMu_noPU_D76_extended_notrunc'
#config.Data.totalUnits = 100
#config.Data.unitsPerJob = 30

# ---NuGun---
#config.General.requestName = 'NuGun_200PU_D76_extended_notrunc'
#config.Data.inputDataset = '/RelValNuGun/CMSSW_12_0_0_pre1-PU_113X_mcRun4_realistic_v7_2026D76PU200-v1/GEN-SIM-DIGI-RAW'
#config.Data.outputDatasetTag = 'NuGun_200PU_D76_extended_notrunc'
#config.Data.totalUnits = 180
#config.Data.unitsPerJob = 40

# ---GGH---
config.General.requestName = 'GGH_200PU_D76_extended_notrunc'
config.Data.inputDataset = '/HiddenGluGluH_mH-250_Phi-30_ctau-100_14TeV-pythia8_TuneCP5/Phase2HLTTDRWinter20DIGI-PU200_110X_mcRun4_realistic_v3-v2/GEN-SIM-DIGI-RAW'
config.Data.outputDatasetTag = 'GGH_200PU_D76_extended_notrunc'
config.Data.totalUnits = 52
config.Data.unitsPerJob = 5

config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.outLFNDirBase = '/store/user/csavard/'
#config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = False

config.Site.storageSite = 'T3_US_FNALLPC'

