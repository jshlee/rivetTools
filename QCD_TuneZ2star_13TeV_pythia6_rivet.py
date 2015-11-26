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

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5000))

# Input source
process.source = cms.Source("EmptySource")
process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
#process.options.allowUnscheduled = cms.untracked.bool(True)

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
    'keep *_generator_*_*',
    'keep *_ak4GenJetsNoNu_*_*',
    #'keep *_genParticles_*_*',
    ),
    fileName = cms.untracked.string('QCD_TuneZ2star_13TeV_pythia6.root'),
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
			'CKIN(4) = 3000  ! maximum pt hat for hard interactions',
			#'MSTP(142) = 2   ! Turns on the PYWEVT Pt reweighting routine',
            #'MSTP(67) = 0',
            #'MSTJ(50) = 0',
		),
		#CSAParameters = cms.vstring(
		#	'CSAMODE = 7     ! towards a flat QCD spectrum',
		#	'PTPOWER = 4.5   ! reweighting of the pt spectrum',
		#),
		parameterSets = cms.vstring(
			'pythiaUESettings',
			'processParameters',
			#'CSAParameters',
		)
	)
)

process.load('GeneratorInterface.RivetInterface.rivetAnalyzer_cfi')
process.rivetAnalyzer.AnalysisNames = cms.vstring('cc_ana')
process.rivetAnalyzer.OutputFile = cms.string('QCD_TuneZ2star_13TeV_pythia6_rivet.yoda')

#from PhysicsTools.HepMCCandAlgos.genParticles_cfi import genParticles#
#from RecoJets.Configuration.GenJetParticles_cff import genParticlesForJets
#from RecoJets.JetProducers.ak4GenJets_cfi import ak4GenJets
#process.ak4GenJetsNoNu = ak4GenJets.clone( src = cms.InputTag("genParticlesForJetsNoNu") )
process.JetSelector = cms.EDFilter("CandViewSelector",
    src = cms.InputTag("ak4GenJetsNoNu"),
    cut = cms.string("pt > 30 & abs( eta ) < 5")
)       
process.JetFilter = cms.EDFilter("CandViewCountFilter",
    src = cms.InputTag("JetSelector"),
    minNumber = cms.uint32(3),
)

# Path and EndPath definitions
process.generation_step = cms.Path(process.pgen*process.rivetAnalyzer)#*process.JetSelector*process.JetFilter)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.endjob_step,process.RAWSIMoutput_step)
# filter all path with the production filter sequence
for path in process.paths:
	getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

#process.RandomNumberGeneratorService.generator.initialSeed = f_num
process.schedule.remove(process.RAWSIMoutput_step)
print process.RandomNumberGeneratorService.generator.initialSeed
process.MessageLogger.cerr.FwkReport.reportEvery = 5000
