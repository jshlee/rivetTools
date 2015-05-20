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

import sys
print sys.argv
max_num = int(sys.argv[2])
f_num = int(sys.argv[3])
min_pt = int(sys.argv[4])
max_pt = int(sys.argv[5])

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(max_num)
)

# Input source
process.source = cms.Source("EmptySource")

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('\\$Revision: 1.1 $'),
    annotation = cms.untracked.string('Summer2012 sample with HERWIGPP: dijet production, pThat = %d .. %d GeV, TuneEE3C'%(min_pt, max_pt)),
    name = cms.untracked.string('\\$Source: /local/reps/CMSSW/CMSSW/Configuration/GenProduction/python/EightTeV/QCD_Pt_1to15_TuneEE3C_8TeV_herwigpp_cff.py,v $')
)

# Output definition
process.RAWSIMoutput = cms.OutputModule("PoolOutputModule",
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    fileName = cms.untracked.string('QCD_Pt_%dto%d_TuneEE3C_8TeV_herwigpp_GEN_%03d.root'%(min_pt, max_pt, f_num)),
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

process.generator = cms.EDFilter("ThePEGGeneratorFilter",
    ue_2_3 = cms.vstring('cd /Herwig/UnderlyingEvent', 
        'set KtCut:MinKT 4.0', 
        'set UECuts:MHatMin 8.0', 
        'set MPIHandler:InvRadius 1.5', 
        'cd /'),
    pdfMRST2001 = cms.vstring('cd /Herwig/Partons', 
        'create Herwig::MRST MRST2001 HwMRST.so', 
        'setup MRST2001 ${HERWIGPATH}/PDF/mrst/2001/lo2002.dat', 
        'set MRST2001:RemnantHandler HadronRemnants', 
        'cp MRST2001 cmsPDFSet', 
        'cd /'),
    ue_2_4 = cms.vstring('cd /Herwig/UnderlyingEvent', 
        'set KtCut:MinKT 4.3', 
        'set UECuts:MHatMin 8.6', 
        'set MPIHandler:InvRadius 1.2', 
        'cd /'),
    cm7TeV = cms.vstring('set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 7000.0', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 2.0*GeV'),
    powhegDefaults = cms.vstring('cp /Herwig/Partons/MRST-NLO /cmsPDFSet', 
        'set /Herwig/Particles/p+:PDF    /Herwig/Partons/MRST-NLO', 
        'set /Herwig/Particles/pbar-:PDF /Herwig/Partons/MRST-NLO', 
        'create Herwig::O2AlphaS O2AlphaS', 
        'set /Herwig/Generators/LHCGenerator:StandardModelParameters:QCD/RunningAlphaS O2AlphaS', 
        'cd /Herwig/Shower', 
        'set KinematicsReconstructor:ReconstructionOption General', 
        'create Herwig::PowhegEvolver PowhegEvolver HwPowhegShower.so', 
        'set ShowerHandler:Evolver PowhegEvolver', 
        'set PowhegEvolver:ShowerModel ShowerModel', 
        'set PowhegEvolver:SplittingGenerator SplittingGenerator', 
        'set PowhegEvolver:MECorrMode 0', 
        'create Herwig::DrellYanHardGenerator DrellYanHardGenerator', 
        'set DrellYanHardGenerator:ShowerAlpha AlphaQCD', 
        'insert PowhegEvolver:HardGenerator 0 DrellYanHardGenerator', 
        'create Herwig::GGtoHHardGenerator GGtoHHardGenerator', 
        'set GGtoHHardGenerator:ShowerAlpha AlphaQCD', 
        'insert PowhegEvolver:HardGenerator 0 GGtoHHardGenerator'),
    reweightConstant = cms.vstring('mkdir /Herwig/Weights', 
        'cd /Herwig/Weights', 
        'create ThePEG::ReweightConstant reweightConstant ReweightConstant.so', 
        'cd /', 
        'set /Herwig/Weights/reweightConstant:C 1', 
        'insert SimpleQCD:Reweights[0] /Herwig/Weights/reweightConstant'),
    lheDefaultPDFs = cms.vstring('cd /Herwig/EventHandlers', 
        'set LHEReader:PDFA /cmsPDFSet', 
        'set LHEReader:PDFB /cmsPDFSet', 
        'cd /'),
    lheDefaults = cms.vstring('cd /Herwig/Cuts', 
        'create ThePEG::Cuts NoCuts', 
        'cd /Herwig/EventHandlers', 
        'create ThePEG::LesHouchesInterface LHEReader', 
        'set LHEReader:Cuts /Herwig/Cuts/NoCuts', 
        'create ThePEG::LesHouchesEventHandler LHEHandler', 
        'set LHEHandler:WeightOption VarWeight', 
        'set LHEHandler:PartonExtractor /Herwig/Partons/QCDExtractor', 
        'set LHEHandler:CascadeHandler /Herwig/Shower/ShowerHandler', 
        'set LHEHandler:HadronizationHandler /Herwig/Hadronization/ClusterHadHandler', 
        'set LHEHandler:DecayHandler /Herwig/Decays/DecayHandler', 
        'insert LHEHandler:LesHouchesReaders 0 LHEReader', 
        'cd /Herwig/Generators', 
        'set LHCGenerator:EventHandler /Herwig/EventHandlers/LHEHandler', 
        'cd /Herwig/Shower', 
        'set Evolver:HardVetoScaleSource Read', 
        'set Evolver:MECorrMode No', 
        'cd /'),
    cmsDefaults = cms.vstring('+pdfMRST2001', 
        '+cm14TeV', 
        '+ue_2_3', 
        '+basicSetup', 
        '+setParticlesStableForDetector'),
    pdfMRST2008LOss = cms.vstring('cp /Herwig/Partons/MRST /Herwig/Partons/cmsPDFSet'),
    generatorModule = cms.string('/Herwig/Generators/LHCGenerator'),
    basicSetup = cms.vstring('cd /Herwig/Generators', 
        'create ThePEG::RandomEngineGlue /Herwig/RandomGlue', 
        'set LHCGenerator:RandomNumberGenerator /Herwig/RandomGlue', 
        'set LHCGenerator:NumberOfEvents 10000000', 
        'set LHCGenerator:DebugLevel 1', 
        'set LHCGenerator:PrintEvent 0', 
        'set LHCGenerator:MaxErrors 10000', 
        'cd /Herwig/Particles', 
        'set p+:PDF /Herwig/Partons/cmsPDFSet', 
        'set pbar-:PDF /Herwig/Partons/cmsPDFSet', 
        'set K0:Width 1e300*GeV', 
        'set Kbar0:Width 1e300*GeV', 
        'cd /'),
    run = cms.string('LHC'),
    repository = cms.string('HerwigDefaults.rpo'),
    cm14TeV = cms.vstring('set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 14000.0', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 2.2*GeV'),
    dataLocation = cms.string('${HERWIGPATH}'),
    pdfCTEQ5L = cms.vstring('cd /Herwig/Partons', 
        'create ThePEG::LHAPDF CTEQ5L ThePEGLHAPDF.so', 
        'set CTEQ5L:PDFName cteq5l.LHgrid', 
        'set CTEQ5L:RemnantHandler HadronRemnants', 
        'cp CTEQ5L cmsPDFSet', 
        'cd /'),
    setParticlesStableForDetector = cms.vstring('cd /Herwig/Particles', 
        'set mu-:Stable Stable', 
        'set mu+:Stable Stable', 
        'set Sigma-:Stable Stable', 
        'set Sigmabar+:Stable Stable', 
        'set Lambda0:Stable Stable', 
        'set Lambdabar0:Stable Stable', 
        'set Sigma+:Stable Stable', 
        'set Sigmabar-:Stable Stable', 
        'set Xi-:Stable Stable', 
        'set Xibar+:Stable Stable', 
        'set Xi0:Stable Stable', 
        'set Xibar0:Stable Stable', 
        'set Omega-:Stable Stable', 
        'set Omegabar+:Stable Stable', 
        'set pi+:Stable Stable', 
        'set pi-:Stable Stable', 
        'set K+:Stable Stable', 
        'set K-:Stable Stable', 
        'set K_S0:Stable Stable', 
        'set K_L0:Stable Stable', 
        'cd /'),
    reweightPthat = cms.vstring('mkdir /Herwig/Weights', 
        'cd /Herwig/Weights', 
        'create ThePEG::ReweightMinPT reweightMinPT ReweightMinPT.so', 
        'cd /', 
        'set /Herwig/Weights/reweightMinPT:Power 4.5', 
        'set /Herwig/Weights/reweightMinPT:Scale 15*GeV', 
        'insert SimpleQCD:Reweights[0] /Herwig/Weights/reweightMinPT'),
    cm10TeV = cms.vstring('set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 10000.0', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 2.1*GeV'),
    cm8TeV = cms.vstring('set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 8000.0', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 2.0*GeV'),
    pdfCTEQ6L1 = cms.vstring('cd /Herwig/Partons', 
        'create ThePEG::LHAPDF CTEQ6L1 ThePEGLHAPDF.so', 
        'set CTEQ6L1:PDFName cteq6ll.LHpdf', 
        'set CTEQ6L1:RemnantHandler HadronRemnants', 
        'cp CTEQ6L1 cmsPDFSet', 
        'cd /'),
    eventHandlers = cms.string('/Herwig/EventHandlers'),
    herwigppUE_EE_3C_1800GeV = cms.vstring('+herwigppUE_EE_3C_Base', 
        'set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 1800.0', 
        'set /Herwig/UnderlyingEvent/KtCut:MinKT 2.26', 
        'set /Herwig/UnderlyingEvent/UECuts:MHatMin 4.52'),
    herwigppUE_EE_3C_14000GeV = cms.vstring('+herwigppUE_EE_3C_Base', 
        'set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 14000.0', 
        'set /Herwig/UnderlyingEvent/KtCut:MinKT 3.53', 
        'set /Herwig/UnderlyingEvent/UECuts:MHatMin 7.06'),
    herwigppUE_EE_3C_2760GeV = cms.vstring('+herwigppUE_EE_3C_Base', 
        'set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 2760.0', 
        'set /Herwig/UnderlyingEvent/KtCut:MinKT 2.33', 
        'set /Herwig/UnderlyingEvent/UECuts:MHatMin 4.66'),
    herwigppUE_EE_3C_8000GeV = cms.vstring('+herwigppUE_EE_3C_Base', 
        'set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 8000.0', 
        'set /Herwig/UnderlyingEvent/KtCut:MinKT 2.85', 
        'set /Herwig/UnderlyingEvent/UECuts:MHatMin 5.7'),
    herwigppUE_EE_3C_7000GeV = cms.vstring('+herwigppUE_EE_3C_Base', 
        'set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 7000.0', 
        'set /Herwig/UnderlyingEvent/KtCut:MinKT 2.752', 
        'set /Herwig/UnderlyingEvent/UECuts:MHatMin 5.504', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 2.34*GeV'),
    herwigppUE_EE_3C_900GeV = cms.vstring('+herwigppUE_EE_3C_Base', 
        'set /Herwig/Generators/LHCGenerator:EventHandler:LuminosityFunction:Energy 900.0', 
        'set /Herwig/UnderlyingEvent/KtCut:MinKT 1.55', 
        'set /Herwig/UnderlyingEvent/UECuts:MHatMin 3.1', 
        'set /Herwig/Shower/Evolver:IntrinsicPtGaussian 1.81*GeV'),
    herwigppUE_EE_3C_Base = cms.vstring('+pdfCTEQ6L1', 
        'cd /Herwig', 
        'create Herwig::O2AlphaS O2AlphaS', 
        'set Model:QCD/RunningAlphaS O2AlphaS', 
        'set /Herwig/Hadronization/ColourReconnector:ColourReconnection Yes', 
        'set /Herwig/Hadronization/ColourReconnector:ReconnectionProbability 0.54', 
        'set /Herwig/Partons/RemnantDecayer:colourDisrupt 0.80', 
        'set /Herwig/UnderlyingEvent/MPIHandler:InvRadius 1.11', 
        'set /Herwig/UnderlyingEvent/MPIHandler:softInt Yes', 
        'set /Herwig/UnderlyingEvent/MPIHandler:twoComp Yes', 
        'set /Herwig/UnderlyingEvent/MPIHandler:DLmode 2', 
        'cd /'),
    configFiles = cms.vstring(),
    crossSection = cms.untracked.double(847880800.0),
    parameterSets = cms.vstring('herwigppUE_EE_3C_8000GeV', 
        'productionParameters', 
        'basicSetup', 
        'setParticlesStableForDetector'),
    productionParameters = cms.vstring('cd /Herwig/MatrixElements/', 
        'insert SimpleQCD:MatrixElements[0] MEQCD2to2', 
        'cd /', 
        'set /Herwig/Cuts/JetKtCut:MinKT %d  *GeV'%min_pt, 
        'set /Herwig/Cuts/JetKtCut:MaxKT %d*GeV'%max_pt, 
        'set /Herwig/Cuts/QCDCuts:MHatMin 0.0*GeV', 
        'set /Herwig/UnderlyingEvent/MPIHandler:IdenticalToUE 0'),
    filterEfficiency = cms.untracked.double(1)
)


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

process.source.firstRun = cms.untracked.uint32(f_num)
process.RandomNumberGeneratorService.generator.initialSeed = f_num

from Configuration.GenProduction.rivet_customize import customise

#call to customisation function customise imported from Configuration.GenProduction.rivet_customize
process = customise(process)

# End of customisation functions
process.rivetAnalyzer.AnalysisNames = cms.vstring('cc_ana')
process.rivetAnalyzer.OutputFile = cms.string('QCD_Pt_%dto%d_TuneEE3C_8TeV_herwigpp_rivet_%03d.yoda'%(min_pt, max_pt, f_num))



