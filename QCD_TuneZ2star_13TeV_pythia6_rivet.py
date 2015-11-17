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

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1000))

# Input source
process.source = cms.Source("EmptySource")
process.options = cms.untracked.PSet()

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('\\$Revision$'),
    annotation = cms.untracked.string('PYTHIA8: QCD dijet production, pThat = GeV, Tune4C'),
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
    fileName = cms.untracked.string('QCD_TuneZ2star_13TeV_pythia6_rivet.root'),
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

from Configuration.Generator.PythiaUEZ2starSettings_cfi import *

process.generator = cms.EDFilter('Pythia6GeneratorFilter',
	comEnergy = cms.double(13000.0),
	crossSection = cms.untracked.double(0),
	filterEfficiency = cms.untracked.double(1),
	maxEventsToPrint = cms.untracked.int32(0),
	pythiaHepMCVerbosity = cms.untracked.bool(False),
	pythiaPylistVerbosity = cms.untracked.int32(0),

	PythiaParameters = cms.PSet(
		pythiaUESettingsBlock,
		processParameters = cms.vstring(
			'MSEL = 1        ! QCD hight pT processes',
			'CKIN(3) = 50    ! minimum pt hat for hard interactions',
			'CKIN(4) = 10000    ! maximum pt hat for hard interactions',
            'MSTP(67) = 0',
            'MSTJ(50) = 0',
		),
		parameterSets = cms.vstring(
			'pythiaUESettings',
			'processParameters',
		)
	)
)

process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
process.rivetAnalyzer.AnalysisNames = cms.vstring('cc_ana')
process.rivetAnalyzer.OutputFile = cms.string('QCD_TuneZ2star_13TeV_pythia6_rivet.yoda')

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
#process.schedule.remove(process.RAWSIMoutput_step)
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
