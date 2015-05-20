import FWCore.ParameterSet.Config as cms

process = cms.Process("runRivetAnalysis")

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

import sys, os
target_d = sys.argv[2]
file_l = ["file:"+os.path.abspath(target_d)+"/"+x for x in os.listdir(target_d) if x.endswith(".root")]
#file_l = ["file:"+os.path.abspath(target_d)+"/QCD_Pt_50to250_TuneZ2_8TeV_pythia6_GEN_%03d.root"%x for x in xrange(1,10)]
print len(file_l)
process.source = cms.Source("PoolSource", fileNames = cms.untracked.vstring())
process.source.fileNames = file_l
#process.source = cms.Source("PoolSource"
#    fileNames = cms.untracked.vstring('file:QCD_Pt_70to2500_TuneZ2_8TeV_pythia6_GEN_118.root')
#)

process.load("GeneratorInterface.RivetInterface.rivetAnalyzer_cfi")

tmp = target_d.split("_")[:6]
out_f = ""
for x in tmp:
  out_f += x+"_"
out_f += "rivet.yoda"

process.rivetAnalyzer.AnalysisNames = cms.vstring('cc_ana')
process.rivetAnalyzer.OutputFile = cms.string(out_f)

process.p = cms.Path(process.rivetAnalyzer)
