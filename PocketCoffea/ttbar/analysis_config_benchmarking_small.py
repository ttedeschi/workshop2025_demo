from pocket_coffea.workflows.tthbb_base_processor import ttHbbBaseProcessor
from pocket_coffea.utils.configurator import Configurator
from pocket_coffea.lib.cut_functions import get_nObj_min, get_nObj_eq, get_nBtagEq, get_nBtagMin, get_HLTsel
from pocket_coffea.parameters.histograms import *
from pocket_coffea.parameters.cuts import passthrough
from pocket_coffea.lib.columns_manager import ColOut
from pocket_coffea.lib.categorization import CartesianSelection

# Local imports of functions
from preselection_cuts import *
import custom_cut_functions

import os
localdir = os.path.dirname(os.path.abspath(__file__))

# Loading default parameters
from pocket_coffea.parameters import defaults
default_parameters = defaults.get_default_parameters()
defaults.register_configuration_dir("config_dir", localdir+"/params")

# adding object preselection
parameters = defaults.merge_parameters_from_files(default_parameters,
                                                  f"{localdir}/params/object_preselection_semileptonic.yaml",
                                                  f"{localdir}/params/btagsf_calibration.yaml",
                                                  f"{localdir}/params/triggers.yaml",
                                                  # f"{localdir}/params/overrides.yaml",
                                                  update=True)


cfg = Configurator(
    parameters = parameters,
    datasets = {
        "jsons": [f"{localdir}/datasets/backgrounds_MC_ttbar.json",
                  f"{localdir}/datasets/DATA_SingleEle.json",
                    ],
        "filter" : {
            "samples": ["TTToSemiLeptonic"],
            "samples_exclude" : [],
            "year": ['2018']
        }
    },

    workflow = ttHbbBaseProcessor,
    
    skim = [get_nObj_min(4, 15., "Jet"),
             get_HLTsel()],
    preselections = [semileptonic_presel_nobtag],
    categories =  {
        "3j1b": [get_nObj_min(3, minpt=30., coll="JetGood"), get_nObj_min(1, coll="BJetGood")],
        "4j2b": [get_nObj_min(4, minpt=30., coll="JetGood"), get_nObj_min(2, coll="BJetGood")],
    },

    weights = {
        "common": {
            "inclusive": ["genWeight","lumi","XS",
                          "pileup",
                          "sf_ele_reco", "sf_ele_id",
                          "sf_mu_id","sf_mu_iso",
                          "sf_btag", "sf_jet_puId", 
                          ],
            "bycategory" : {
            }
        },
        "bysample": {
        }
    },

    variations = {
        "weights": {
            "common": {
                "inclusive": [  "pileup",                   
                              ],
                "bycategory" : {
                }
            },
        "bysample": {
        }    
        },
    },

    
   variables = {
        **ele_hists(coll="ElectronGood", pos=0),
        **muon_hists(coll="MuonGood", pos=0),
        **count_hist(name="nElectronGood", coll="ElectronGood",bins=3, start=0, stop=3),
        **count_hist(name="nMuonGood", coll="MuonGood",bins=3, start=0, stop=3),
        **count_hist(name="nJets", coll="JetGood",bins=10, start=4, stop=14),
        **count_hist(name="nBJets", coll="BJetGood",bins=12, start=2, stop=14),
        **jet_hists(coll="JetGood", pos=0),
        **jet_hists(coll="JetGood", pos=1),
        **jet_hists(coll="JetGood", pos=2),
       
       #**processing_metadata_hists(["baseline"], 300000)
    },

    # columns = {
    #     "common": {},
    #     "bysample": {
    #         "TTToSemiLeptonic" : { "inclusive":  [ColOut("LeptonGood",["pt","eta","phi"])]},
    #         "TTToSemiLeptonic__=1b" :{ "inclusive":  [ColOut("JetGood",["pt","eta","phi"])]},
    #         "TTToSemiLeptonic__=2b":{ "inclusive":  [ColOut("BJetGood",["pt","eta","phi"])]},
                
    #     },
    # }
    
)

import cloudpickle
#cloudpickle.register_pickle_by_value(preselection_cuts)
cloudpickle.register_pickle_by_value(custom_cut_functions)
   
