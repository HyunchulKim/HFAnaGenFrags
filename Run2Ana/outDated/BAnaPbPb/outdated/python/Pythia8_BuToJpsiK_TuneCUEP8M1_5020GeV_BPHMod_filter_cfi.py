import FWCore.ParameterSet.Config as cms
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.Pythia8CUEP8M1Settings_cfi import *
from GeneratorInterface.EvtGenInterface.EvtGenSetting_cff import *

generator = cms.EDFilter("Pythia8GeneratorFilter",
                         pythiaPylistVerbosity = cms.untracked.int32(0),
                         pythiaHepMCVerbosity = cms.untracked.bool(False),
                         comEnergy = cms.double(5020.0),
                         maxEventsToPrint = cms.untracked.int32(0),
                         ExternalDecays = cms.PSet(
        EvtGen130 = cms.untracked.PSet(
            decay_table = cms.string('GeneratorInterface/EvtGenInterface/data/DECAY_2010.DEC'),
            particle_property_file = cms.FileInPath('GeneratorInterface/EvtGenInterface/data/evt.pdl'),
            user_decay_file = cms.vstring('GeneratorInterface/ExternalDecays/data/Bu_JpsiK.dec'),
            list_forced_decays = cms.vstring('MyB+',
                                              'MyB-'),
            operates_on_particles = cms.vint32()
            ),
        parameterSets = cms.vstring('EvtGen130')
        ),
                         PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CUEP8M1SettingsBlock,
        processParameters = cms.vstring(
#            'SoftQCD:nonDiffractive = on',
#            'SoftQCD:singleDiffractive = on',
#            'SoftQCD:doubleDiffractive = on',
            'HardQCD:gg2bbbar    = on ',
            'HardQCD:qqbar2bbbar = on ',
            'HardQCD:hardbbbar   = on',
            'PhaseSpace:pTHatMin = 2.',
            
            ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CUEP8M1Settings',
                                    'processParameters',
                                    )
        )
                         )

generator.PythiaParameters.processParameters.extend(EvtGenExtraParticles)

configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.1 $'),
    name = cms.untracked.string('$Source: Configuration/Generator/python/BuToKstarMuMu_forSTEAM_13TeV_TuneCUETP8M1_cfi.py $'),
    annotation = cms.untracked.string('Summer14: Pythia8+EvtGen130 generation of Bu --> K* Mu+Mu-, 13TeV, Tune CUETP8M1')
    )

###########
# Filters #
###########
bfilter = cms.EDFilter("PythiaFilter",
    ParticleID = cms.untracked.int32(521),
    MaxEta = cms.untracked.double(3.0),
    MinEta = cms.untracked.double(-3.0),
    MinPt = cms.untracked.double(5.0)
)

bDaufilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(0),
    ParticleID = cms.untracked.int32(521),
    DaughterIDs = cms.untracked.vint32(443, 321),
    verbose = cms.untracked.int32(0),
    MinPt = cms.untracked.vdouble(0.0, 0.0),
    MaxEta = cms.untracked.vdouble(9999, 9999),
    MinEta = cms.untracked.vdouble(-9999, -9999),
    NumberDaughters = cms.untracked.int32(2),
)

jpsifilter = cms.EDFilter("PythiaDauVFilter",
    MotherID = cms.untracked.int32(521),
    ParticleID = cms.untracked.int32(443),
    DaughterIDs = cms.untracked.vint32(13, -13),
    verbose = cms.untracked.int32(0),
    MinPt = cms.untracked.vdouble(0.5, 0.5),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    NumberDaughters = cms.untracked.int32(2),
)

mumugenfilter = cms.EDFilter("MCParticlePairFilter",
    Status = cms.untracked.vint32(1, 1),
    MinPt = cms.untracked.vdouble(0.5, 0.5),
    MinP = cms.untracked.vdouble(0., 0.),
    MaxEta = cms.untracked.vdouble(2.5, 2.5),
    MinEta = cms.untracked.vdouble(-2.5, -2.5),
    MinInvMass = cms.untracked.double(2.0),
    MaxInvMass = cms.untracked.double(4.0),
    ParticleCharge = cms.untracked.int32(-1),
    ParticleID1 = cms.untracked.vint32(13),
    ParticleID2 = cms.untracked.vint32(13)
)

ProductionFilterSequence = cms.Sequence(generator*bfilter*bDaufilter*jpsifilter*mumugenfilter)
