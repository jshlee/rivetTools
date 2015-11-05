import FWCore.ParameterSet.Config as cms

process = cms.Process('GEN')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

#import random
#f_num = random.randrange(0,100000000)
max_num = 1000
min_pt = 50
max_pt = -1

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(max_num)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('\\$Revision$'),
    annotation = cms.untracked.string('Summer2012 sample with PYTHIA8: QCD dijet production, pThat = %d .. %d GeV, Tune4C'%(min_pt, max_pt)),
    name = cms.untracked.string('\\$Source$')
)

# Output definition
process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = cms.untracked.vstring('drop *',
    'keep GenEventInfoProduct_generator_*_*',
    'keep edmHepMCProduct_generator_*_*',
    'keep recoGenJets_ak4GenJetsNoNu_*_*',
    #'keep *_genParticles_*_*',
    ),
    fileName = cms.untracked.string('QCD_Pt_%dto%d_Tune4C_8TeV_pythia8_GEN.root'%(min_pt, max_pt)),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-RAW')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

# Additional output definition

# Other statements
process.genstepfilter.triggerConditions=cms.vstring("generation_step")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
    pythiaPylistVerbosity = cms.untracked.int32(0),
    filterEfficiency = cms.untracked.double(1),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(8000.0),
    crossSection = cms.untracked.double(76210670.0),
    maxEventsToPrint = cms.untracked.int32(0),
    PythiaParameters = cms.PSet(
        processParameters = cms.vstring('Main:timesAllowErrors    = 10000', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tauMax = 10', 
            'HardQCD:all = on', 
            #'TimeShower:globalRecoil = on', # might turn off colour coherence
            'PhaseSpace:pTHatMin = %d  '%min_pt, 
            'PhaseSpace:pTHatMax = %d  '%max_pt, 
            'Tune:pp 5', 
            'Tune:ee 3'),
        parameterSets = cms.vstring('processParameters')
    )
)

process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
process.rivetAnalyzer.AnalysisNames = cms.vstring('cc_ana')
process.rivetAnalyzer.OutputFile = cms.string('QCD_Pt_%dto%d_Tune4C_8TeV_pythia8_rivet.yoda'%(min_pt, max_pt))

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

#process.RandomNumberGeneratorService.generator.initialSeed = f_num

process.generation_step+=process.rivetAnalyzer
process.schedule.remove(process.RAWSIMoutput_step)
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
