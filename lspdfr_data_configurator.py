# pylint: disable=W0614
import configparser
import copy
import os
import re
import sys
import traceback
from enum import Enum, IntFlag, auto
from functools import partial
from os.path import basename
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *
from xml.dom import minidom
from xml.etree import ElementTree

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

VERSION = "0.4.0"

PEDS = ["mp_m_freemode_01", "mp_f_freemode_01", "s_m_m_armoured_01", "s_m_m_armoured_02", "s_m_y_cop_01", "s_f_y_cop_01", "s_m_m_fiboffice_01", "s_m_m_fiboffice_02", "s_m_y_fireman_01", "s_m_y_hwaycop_01", "s_m_m_paramedic_01", "s_m_m_prisguard_01", "s_m_y_ranger_01", "s_f_y_ranger_01", "s_m_m_security_01", "s_m_y_sheriff_01", "s_f_y_sheriff_01", "s_m_m_snowcop_01", "u_m_m_fibarchitect", "a_f_m_beach_01", "a_f_m_bevhills_01", "a_f_m_bevhills_02", "a_f_m_bodybuild_01", "a_f_m_business_02", "a_f_m_downtown_01", "a_f_m_eastsa_01", "a_f_m_eastsa_02", "a_f_m_fatbla_01", "a_f_m_fatcult_01", "a_f_m_fatwhite_01", "a_f_m_ktown_01", "a_f_m_ktown_02", "a_f_m_prolhost_01", "a_f_m_salton_01", "a_f_m_skidrow_01", "a_f_m_soucentmc_01", "a_f_m_soucent_01", "a_f_m_soucent_02", "a_f_m_tourist_01", "a_f_m_trampbeac_01", "a_f_m_tramp_01", "a_f_o_genstreet_01", "a_f_o_indian_01", "a_f_o_ktown_01", "a_f_o_salton_01", "a_f_o_soucent_01", "a_f_o_soucent_02", "a_f_y_beach_01", "a_f_y_bevhills_01", "a_f_y_bevhills_02", "a_f_y_bevhills_03", "a_f_y_bevhills_04", "a_f_y_business_01", "a_f_y_business_02", "a_f_y_business_03", "a_f_y_business_04", "a_f_y_eastsa_01", "a_f_y_eastsa_02", "a_f_y_eastsa_03", "a_f_y_epsilon_01", "a_f_y_fitness_01", "a_f_y_fitness_02", "a_f_y_genhot_01", "a_f_y_golfer_01", "a_f_y_hiker_01", "a_f_y_hippie_01", "a_f_y_hipster_01", "a_f_y_hipster_02", "a_f_y_hipster_03", "a_f_y_hipster_04", "a_f_y_indian_01", "a_f_y_juggalo_01", "a_f_y_runner_01", "a_f_y_rurmeth_01", "a_f_y_scdressy_01", "a_f_y_skater_01", "a_f_y_soucent_01", "a_f_y_soucent_02", "a_f_y_soucent_03", "a_f_y_tennis_01", "a_f_y_topless_01", "a_f_y_tourist_01", "a_f_y_tourist_02", "a_f_y_vinewood_01", "a_f_y_vinewood_02", "a_f_y_vinewood_03", "a_f_y_vinewood_04", "a_f_y_yoga_01", "a_m_m_acult_01", "a_m_m_afriamer_01", "a_m_m_beach_01", "a_m_m_beach_02", "a_m_m_bevhills_01", "a_m_m_bevhills_02", "a_m_m_business_01", "a_m_m_eastsa_01", "a_m_m_eastsa_02", "a_m_m_farmer_01", "a_m_m_fatlatin_01", "a_m_m_genfat_01", "a_m_m_genfat_02", "a_m_m_golfer_01", "a_m_m_hasjew_01", "a_m_m_hillbilly_01", "a_m_m_hillbilly_02", "a_m_m_indian_01", "a_m_m_ktown_01", "a_m_m_malibu_01", "a_m_m_mexcntry_01", "a_m_m_mexlabor_01", "a_m_m_og_boss_01", "a_m_m_paparazzi_01", "a_m_m_polynesian_01", "a_m_m_prolhost_01", "a_m_m_rurmeth_01", "a_m_m_salton_01", "a_m_m_salton_02", "a_m_m_salton_03", "a_m_m_salton_04", "a_m_m_skater_01", "a_m_m_skidrow_01", "a_m_m_socenlat_01", "a_m_m_soucent_01", "a_m_m_soucent_02", "a_m_m_soucent_03", "a_m_m_soucent_04", "a_m_m_stlat_02", "a_m_m_tennis_01", "a_m_m_tourist_01", "a_m_m_trampbeac_01", "a_m_m_tramp_01", "a_m_m_tranvest_01", "a_m_m_tranvest_02", "a_m_o_acult_01", "a_m_o_acult_02", "a_m_o_beach_01", "a_m_o_genstreet_01", "a_m_o_ktown_01", "a_m_o_salton_01", "a_m_o_soucent_01", "a_m_o_soucent_02", "a_m_o_soucent_03", "a_m_o_tramp_01", "a_m_y_acult_01", "a_m_y_acult_02", "a_m_y_beachvesp_01", "a_m_y_beachvesp_02", "a_m_y_beach_01", "a_m_y_beach_02", "a_m_y_beach_03", "a_m_y_bevhills_01", "a_m_y_bevhills_02", "a_m_y_breakdance_01", "a_m_y_busicas_01", "a_m_y_business_01", "a_m_y_business_02", "a_m_y_business_03", "a_m_y_cyclist_01", "a_m_y_dhill_01", "a_m_y_downtown_01", "a_m_y_eastsa_01", "a_m_y_eastsa_02", "a_m_y_epsilon_01", "a_m_y_epsilon_02", "a_m_y_gay_01", "a_m_y_gay_02", "a_m_y_genstreet_01", "a_m_y_genstreet_02", "a_m_y_golfer_01", "a_m_y_hasjew_01", "a_m_y_hiker_01", "a_m_y_hippy_01", "a_m_y_hipster_01", "a_m_y_hipster_02", "a_m_y_hipster_03", "a_m_y_indian_01", "a_m_y_jetski_01", "a_m_y_juggalo_01", "a_m_y_ktown_01", "a_m_y_ktown_02", "a_m_y_latino_01", "a_m_y_methhead_01", "a_m_y_mexthug_01", "a_m_y_motox_01", "a_m_y_motox_02", "a_m_y_musclbeac_01", "a_m_y_musclbeac_02", "a_m_y_polynesian_01", "a_m_y_roadcyc_01", "a_m_y_runner_01", "a_m_y_runner_02", "a_m_y_salton_01", "a_m_y_skater_01", "a_m_y_skater_02", "a_m_y_soucent_01", "a_m_y_soucent_02", "a_m_y_soucent_03", "a_m_y_soucent_04", "a_m_y_stbla_01", "a_m_y_stbla_02", "a_m_y_stlat_01", "a_m_y_stwhi_01", "a_m_y_stwhi_02", "a_m_y_sunbathe_01", "a_m_y_surfer_01", "a_m_y_vindouche_01", "a_m_y_vinewood_01", "a_m_y_vinewood_02", "a_m_y_vinewood_03", "a_m_y_vinewood_04", "a_m_y_yoga_01", "csb_abigail", "csb_anita", "csb_anton", "csb_ballasog", "csb_bride", "csb_burgerdrug", "csb_car3guy1", "csb_car3guy2", "csb_chef", "csb_chin_goon", "csb_cletus", "csb_cop", "csb_customer", "csb_denise_friend", "csb_fos_rep", "csb_groom", "csb_grove_str_dlr", "csb_g", "csb_hao", "csb_hugh", "csb_imran", "csb_janitor", "csb_maude", "csb_mweather", "csb_ortega", "csb_oscar", "csb_porndudes", "csb_prologuedriver", "csb_prolsec", "csb_ramp_gang", "csb_ramp_hic", "csb_ramp_hipster", "csb_ramp_marine", "csb_ramp_mex", "csb_reporter", "csb_roccopelosi", "csb_screen_writer", "csb_stripper_01", "csb_stripper_02", "csb_tonya", "csb_trafficwarden", "g_f_y_ballas_01", "g_f_y_families_01", "g_f_y_lost_01", "g_f_y_vagos_01", "g_m_m_armboss_01", "g_m_m_armgoon_01", "g_m_m_armlieut_01", "g_m_m_chemwork_01", "g_m_m_chiboss_01", "g_m_m_chicold_01", "g_m_m_chigoon_01", "g_m_m_chigoon_02", "g_m_m_korboss_01", "g_m_m_mexboss_01", "g_m_m_mexboss_02", "g_m_y_armgoon_02", "g_m_y_azteca_01", "g_m_y_ballaeast_01", "g_m_y_ballaorig_01", "g_m_y_ballasout_01", "g_m_y_famca_01", "g_m_y_famdnf_01", "g_m_y_famfor_01", "g_m_y_korean_01", "g_m_y_korean_02", "g_m_y_korlieut_01", "g_m_y_lost_01", "g_m_y_lost_02", "g_m_y_lost_03", "g_m_y_mexgang_01", "g_m_y_mexgoon_01", "g_m_y_mexgoon_02", "g_m_y_mexgoon_03", "g_m_y_pologoon_01", "g_m_y_pologoon_02", "g_m_y_salvaboss_01", "g_m_y_salvagoon_01", "g_m_y_salvagoon_02", "g_m_y_salvagoon_03", "g_m_y_strpunk_01", "g_m_y_strpunk_02", "hc_driver", "hc_gunman", "hc_hacker", "ig_abigail", "ig_amandatownley", "ig_andreas", "ig_ashley", "ig_ballasog", "ig_bankman", "ig_barry", "ig_bestmen", "ig_beverly", "ig_brad", "ig_bride", "ig_car3guy1", "ig_car3guy2", "ig_casey", "ig_chef", "ig_chengsr", "ig_chrisformage", "ig_claypain", "ig_clay", "ig_cletus", "ig_dale", "ig_davenorton", "ig_denise", "ig_devin", "ig_dom", "ig_dreyfuss", "ig_drfriedlander", "ig_fabien", "ig_fbisuit_01", "ig_floyd", "ig_groom", "ig_hao", "ig_hunter", "ig_janet", "ig_jay_norris", "ig_jewelass", "ig_jimmyboston", "ig_jimmydisanto", "ig_joeminuteman", "ig_johnnyklebitz", "ig_josef", "ig_josh", "ig_kerrymcintosh", "ig_lamardavis", "ig_lazlow", "ig_lestercrest", "ig_lifeinvad_01", "ig_lifeinvad_02", "ig_magenta", "ig_manuel", "ig_marnie", "ig_maryann", "ig_maude", "ig_michelle", "ig_milton", "ig_molly", "ig_mrk", "ig_mrsphillips", "ig_mrs_thornhill", "ig_natalia", "ig_nervousron", "ig_nigel", "ig_old_man1a", "ig_old_man2", "ig_omega", "ig_oneil", "ig_orleans", "ig_ortega", "ig_paper", "ig_patricia", "ig_priest", "ig_prolsec_02", "ig_ramp_gang", "ig_ramp_hic", "ig_ramp_hipster", "ig_ramp_mex", "ig_roccopelosi", "ig_russiandrunk", "ig_screen_writer", "ig_siemonyetarian", "ig_solomon", "ig_stevehains", "ig_stretch", "ig_talina", "ig_tanisha", "ig_taocheng", "ig_taostranslator", "ig_tenniscoach", "ig_terry", "ig_tomepsilon", "ig_tonya", "ig_tracydisanto", "ig_trafficwarden", "ig_tylerdix", "ig_wade", "ig_zimbor", "mp_f_deadhooker", "mp_f_misty_01", "mp_f_stripperlite", "mp_g_m_pros_01", "mp_m_claude_01", "mp_m_exarmy_01", "mp_m_famdd_01", "mp_m_fibsec_01", "mp_m_marston_01", "mp_m_niko_01", "mp_m_shopkeep_01", "player_one", "player_two", "player_zero", "s_f_m_fembarber", "s_f_m_maid_01", "s_f_m_shop_high", "s_f_m_sweatshop_01", "s_f_y_airhostess_01", "s_f_y_bartender_01", "s_f_y_baywatch_01", "s_f_y_factory_01", "s_f_y_hooker_01", "s_f_y_hooker_02", "s_f_y_hooker_03", "s_f_y_migrant_01", "s_f_y_movprem_01", "s_f_y_scrubs_01", "s_f_y_shop_low", "s_f_y_shop_mid", "s_f_y_stripperlite", "s_f_y_stripper_01", "s_f_y_stripper_02", "s_f_y_sweatshop_01", "s_m_m_ammucountry", "s_m_m_autoshop_01", "s_m_m_autoshop_02", "s_m_m_bouncer_01", "s_m_m_chemsec_01", "s_m_m_ciasec_01", "s_m_m_cntrybar_01", "s_m_m_dockwork_01", "s_m_m_doctor_01", "s_m_m_gaffer_01", "s_m_m_gardener_01", "s_m_m_gentransport", "s_m_m_hairdress_01", "s_m_m_highsec_01", "s_m_m_highsec_02", "s_m_m_janitor", "s_m_m_lathandy_01", "s_m_m_lifeinvad_01", "s_m_m_linecook", "s_m_m_lsmetro_01", "s_m_m_mariachi_01", "s_m_m_marine_01", "s_m_m_marine_02", "s_m_m_migrant_01", "s_m_m_movalien_01", "s_m_m_movprem_01", "s_m_m_movspace_01", "s_m_m_pilot_01", "s_m_m_pilot_02", "s_m_m_postal_01", "s_m_m_postal_02", "s_m_m_scientist_01", "s_m_m_strperf_01", "s_m_m_strpreach_01", "s_m_m_strvend_01", "s_m_m_trucker_01", "s_m_m_ups_01", "s_m_m_ups_02", "s_m_o_busker_01", "s_m_y_airworker", "s_m_y_ammucity_01", "s_m_y_armymech_01", "s_m_y_autopsy_01", "s_m_y_barman_01", "s_m_y_baywatch_01", "s_m_y_blackops_01", "s_m_y_blackops_02", "s_m_y_busboy_01", "s_m_y_chef_01", "s_m_y_clown_01", "s_m_y_construct_01", "s_m_y_construct_02", "s_m_y_dealer_01", "s_m_y_devinsec_01", "s_m_y_dockwork_01", "s_m_y_doorman_01", "s_m_y_dwservice_01", "s_m_y_dwservice_02", "s_m_y_factory_01", "s_m_y_garbage", "s_m_y_grip_01", "s_m_y_marine_01", "s_m_y_marine_02", "s_m_y_marine_03", "s_m_y_mime", "s_m_y_pestcont_01", "s_m_y_pilot_01", "s_m_y_prismuscl_01", "s_m_y_prisoner_01", "s_m_y_robber_01", "s_m_y_shop_mask", "s_m_y_strvend_01", "s_m_y_swat_01", "s_m_y_uscg_01", "s_m_y_valet_01", "s_m_y_waiter_01", "s_m_y_winclean_01", "s_m_y_xmech_01", "s_m_y_xmech_02", "u_f_m_corpse_01", "u_f_m_miranda", "u_f_m_promourn_01", "u_f_o_moviestar", "u_f_o_prolhost_01", "u_f_y_bikerchic", "u_f_y_comjane", "u_f_y_corpse_01", "u_f_y_corpse_02", "u_f_y_hotposh_01", "u_f_y_jewelass_01", "u_f_y_mistress", "u_f_y_poppymich", "u_f_y_princess", "u_f_y_spyactress", "u_m_m_aldinapoli", "u_m_m_bankman", "u_m_m_bikehire_01", "u_m_m_filmdirector", "u_m_m_glenstank_01", "u_m_m_griff_01", "u_m_m_jesus_01", "u_m_m_jewelsec_01", "u_m_m_jewelthief", "u_m_m_markfost", "u_m_m_partytarget", "u_m_m_prolsec_01", "u_m_m_promourn_01", "u_m_m_rivalpap", "u_m_m_spyactor", "u_m_m_willyfist", "u_m_o_finguru_01", "u_m_o_taphillbilly", "u_m_o_tramp_01", "u_m_y_abner", "u_m_y_antonb", "u_m_y_babyd", "u_m_y_baygor", "u_m_y_burgerdrug_01", "u_m_y_chip", "u_m_y_cyclist_01", "u_m_y_fibmugger_01", "u_m_y_guido_01", "u_m_y_gunvend_01", "u_m_y_hippie_01", "u_m_y_imporage", "u_m_y_justin", "u_m_y_mani", "u_m_y_militarybum", "u_m_y_paparazzi", "u_m_y_party_01", "u_m_y_pogo_01", "u_m_y_prisoner_01", "u_m_y_proldriver_01", "u_m_y_rsranger_01", "u_m_y_sbike", "u_m_y_staggrm_01", "u_m_y_tattoo_01", "u_m_y_zombie_01"]

VEHICLES = ["Ambulance", "FBI", "FBI2", "FireTruck", "PBus", "Police", "Police2", "Police3", "Police4", "PoliceOld1", "PoliceOld2", "PoliceT", "Policeb", "Polmav", "Pranger", "Predator", "Riot", "Sheriff", "Sheriff2", "Buzzard", "Buzzard2", "Dinghy", "Dinghy2", "Dinghy3", "Dinghy4", "Jetmax", "Marquis", "Seashark", "Seashark2", "Seashark3", "Speeder", "Speeder2", "Squalo", "Submersible", "Submersible2", "Suntrap", "Toro", "Toro2", "Tropic", "Tropic2", "Tug", "Benson", "Biff", "Hauler", "Hauler2", "Mule", "Mule2", "Mule3", "Packer", "Phantom", "Phantom2", "Phantom3", "Pounder", "Stockade", "Stockade3", "Blista", "Blista2", "Blista3", "Brioso", "Dilettante", "Dilettante2", "Issi2", "Panto", "Prairie", "Rhapsody", "CogCabrio", "Exemplar", "F620", "Felon", "Felon2", "Jackal", "Oracle", "Oracle2", "Sentinel", "Sentinel2", "Windsor", "Windsor2", "Zion", "Zion2", "Bmx", "Cruiser", "Fixter", "Scorcher", "TriBike", "TriBike2", "TriBike3", "Annihilator", "Cargobob", "Cargobob2", "Cargobob3", "Cargobob4", "Frogger", "Frogger2", "Maverick", "Savage", "Skylift", "Supervolito", "Supervolito2", "Swift", "Swift2", "Valkyrie", "Valkyrie2", "Volatus", "Bulldozer", "Cutter", "Dump", "Flatbed", "Guardian", "Handler", "Mixer", "Mixer2", "Rubble", "TipTruck", "TipTruck2", "APC", "Barracks", "Barracks2", "Barracks3", "Crusader", "Halftrack", "Rhino", "Trailersmall2", "Akuma", "Avarus", "Bagger", "Bati2", "Bati", "BF400", "Blazer4", "CarbonRS", "Chimera", "Cliffhanger", "Daemon2", "Daemon", "Defiler", "Double", "Enduro", "Esskey", "Faggio", "Faggio2", "Faggio3", "Fcr2", "Fcr", "Gargoyle", "Hakuchou2", "Hakuchou", "Hexer", "Innovation", "Lectro", "Manchez", "Nemesis", "Nightblade", "Opressor", "PCJ", "Ratbike", "Ruffian", "Sanchez2", "Sanchez", "Sanctus", "Shotaro", "Sovereign", "Thrust", "Vader", "Vindicator", "Vortex", "Wolfsbane", "Zombiea", "Zombieb", "Blade", "Buccaneer", "Buccaneer2", "Chino", "Chino2", "Dominator", "Dominator2", "Dukes", "Dukes2", "Faction", "Faction2", "Faction3", "Gauntlet", "Gauntlet2", "Hotknife", "Lurcher", "Moonbeam", "Moonbeam2", "Nightshade", "Phoenix", "Picador", "RatLoader", "RatLoader2", "Ruiner", "Ruiner2", "SabreGT", "SabreGT2", "Sadler2", "SlamVan", "SlamVan2", "SlamVan3", "Stalion", "Stalion2", "Tampa", "Tampa3", "Vigero", "Virgo", "Virgo2", "Virgo3", "Voodoo", "Voodoo2", "BfInjection", "Bifta", "Blazer", "Blazer2", "Blazer3", "Blazer5", "Bodhi2", "Brawler", "DLoader", "Dune", "Dune2", "Dune3", "Dune4", "Dune5", "Insurgent", "Insurgent2", "Insurgent3", "Kalahari", "Lguard", "Marshall", "Mesa", "Mesa2", "Mesa3", "Monster", "Nightshark", "RancherXL", "RancherXL2", "Rebel", "Rebel2", "Sandking", "Sandking2", "Technical", "Technical2", "Technical3", "TrophyTruck", "TrophyTruck2", "Besra", "Blimp", "Blimp2", "CargoPlane", "Cuban800", "Dodo", "Duster", "Hydra", "Jet", "Lazer", "Luxor", "Luxor2", "Mammatus", "Miljet", "Nimbus", "Shamal", "Stunt", "Titan", "Velum", "Velum2", "Vestra", "BJXL", "Baller", "Baller2", "Baller3", "Baller4", "Baller5", "Baller6", "Cavalcade", "Cavalcade2", "Contender", "Dubsta", "Dubsta2", "Dubsta3", "FQ2", "Granger", "Gresley", "Habanero", "Huntley", "Landstalker", "Patriot", "Radi", "Rocoto", "Seminole", "Serrano", "XLS", "XLS2", "Asea", "Asea2", "Asterope", "Cog55", "Cog552", "Cognoscenti", "Cognoscenti2", "Emperor", "Emperor2", "Emperor3", "Fugitive", "Glendale", "Ingot", "Intruder", "Limo2", "Premier", "Primo", "Primo2", "Regina", "Romero", "Stanier", "Stratum", "Stretch", "Surge", "Tailgater", "Warrener", "Washington", "Airbus", "Brickade", "Bus", "Coach", "Rallytruck", "RentalBus", "Taxi", "Tourbus", "Trash", "Trash2", "Alpha", "Banshee", "Banshee2", "BestiaGTS", "Buffalo", "Buffalo2", "Buffalo3", "Carbonizzare", "Comet2", "Comet3", "Coquette", "Elegy", "Elegy2", "Feltzer2", "Feltzer3", "Furoregt", "Fusilade", "Futo", "Infernus2", "Jester", "Jester2", "Khamelion", "Kuruma", "Kuruma2", "Lynx", "Massacro", "Massacro2", "Ninef", "Ninef2", "Omnis", "Penumbra", "RapidGT", "RapidGT2", "Raptor", "Ruston", "Schafter2", "Schafter3", "Schafter4", "Schafter5", "Schafter6", "Schwarzer", "Seven70", "Specter", "Specter2", "Sultan", "Surano", "Tampa2", "Tropos", "Verlierer2", "Ardent", "BType", "BType2", "BType3", "Casco", "Cheetah2", "Coquette2", "Coquette3", "JB700", "Mamba", "Manana", "Monroe", "Peyote", "Pigalle", "Stinger", "StingerGT", "Torero", "Tornado", "Tornado2", "Tornado3", "Tornado4", "Tornado5", "Tornado6", "ZType", "Adder", "Bullet", "Cheetah", "EntityXF", "FMJ", "GP1", "Infernus", "RE7B", "Nero", "Nero2", "Osiris", "Penetrator", "Pfister811", "Prototipo", "Reaper", "Sheava", "SultanRS", "Superd", "T20", "Tempesta", "Turismo2", "Turismor", "Tyrus", "Vacca", "Vagner", "Voltic", "Voltic2", "Zentorno", "Italigtb", "Italigtb2", "XA21", "ArmyTanker", "ArmyTrailer", "ArmyTrailer2", "BaleTrailer", "BoatTrailer", "CableCar", "DockTrailer", "GrainTrailer", "PropTrailer", "RakeTrailer", "TR2", "TR3", "TR4", "TRFlat", "TVTrailer", "Tanker", "Tanker2", "TrailerLogs", "TrailerSmall", "Trailers", "Trailers2", "Trailers3", "Freight", "FreightCar", "FreightCont1", "FreightCont2", "FreightGrain", "FreightTrailer", "TankerCar", "Airtug", "Caddy", "Caddy2", "Caddy3", "Docktug", "Forklift", "Mower", "Ripley", "Sadler", "Scrap", "TowTruck", "TowTruck2", "Tractor", "Tractor2", "Tractor3", "TrailerLarge", "TrailerS4", "UtilliTruck", "UtilliTruck3", "UtilliTruck2", "Bison", "Bison2", "Bison3", "BobcatXL", "Boxville", "Boxville2", "Boxville3", "Boxville4", "Boxville5", "Burrito", "Burrito2", "Burrito3", "Burrito4", "Burrito5", "Camper", "GBurrito", "GBurrito2", "Journey", "Minivan", "Minivan2", "Paradise", "Pony", "Pony2", "Rumpo", "Rumpo2", "Rumpo3", "Speedo", "Speedo2", "Surfer", "Surfer2", "Taco", "Youga", "Youga2"]

ZONES = {"AIRP": "Los Santos International Airport", "ALAMO": "Alamo Sea", "ALTA": "Alta", "ARMYB": "Fort Zancudo", "BANHAMC": "Banham Canyon Dr", "BANNING": "Banning", "BEACH": "Vespucci Beach", "BHAMCA": "Banham Canyon", "BRADP": "Braddock Pass", "BRADT": "Braddock Tunnel", "BURTON": "Burton", "CALAFB": "Calafia Bridge", "CANNY": "Raton Canyon", "CCREAK": "Cassidy Creek", "CHAMH": "Chamberlain Hills", "CHIL": "Vinewood Hills", "CHU": "Chumash", "CMSW": "Chiliad Mountain State Wilderness", "CYPRE": "Cypress Flats", "DAVIS": "Davis", "DELBE": "Del Perro Beach", "DELPE": "Del Perro", "DELSOL": "La Puerta", "DESRT": "Grand Senora Desert", "DOWNT": "Downtown", "DTVINE": "Downtown Vinewood", "EAST_V": "East Vinewood", "EBURO": "El Burro Heights", "ELGORL": "El Gordo Lighthouse", "ELYSIAN": "Elysian Island", "GALFISH": "Galilee", "GOLF": "GWC and Golfing Society", "GRAPES": "Grapeseed", "GREATC": "Great Chaparral", "HARMO": "Harmony", "HAWICK": "Hawick", "HORS": "Vinewood Racetrack", "HUMLAB": "Humane Labs and Research", "JAIL": "Bolingbroke Penitentiary", "KOREAT": "Little Seoul", "LACT": "Land Act Reservoir", "LAGO": "Lago Zancudo", "LDAM": "Land Act Dam", "LEGSQU": "Legion Square", "LMESA": "La Mesa", "LOSPUER": "La Puerta", "MIRR": "Mirror Park", "MORN": "Morningwood", "MOVIE": "Richards Majestic", "MTCHIL": "Mount Chiliad", "MTGORDO": "Mount Gordo", "MTJOSE": "Mount Josiah", "MURRI": "Murrieta Heights", "NCHU": "North Chumash", "NOOSE": "N.O.O.S.E", "OCEANA": "Pacific Ocean", "PALCOV": "Paleto Cove", "PALETO": "Paleto Bay", "PALFOR": "Paleto Forest", "PALHIGH": "Palomino Highlands", "PALMPOW": "Palmer-Taylor Power Station", "PBLUFF": "Pacific Bluffs", "PBOX": "Pillbox Hill", "PROCOB": "Procopio Beach", "RANCHO": "Rancho", "RGLEN": "Richman Glen", "RICHM": "Richman", "ROCKF": "Rockford Hills", "RTRAK": "Redwood Lights Track", "SANAND": "San Andreas", "SANCHIA": "San Chianski Mountain Range", "SANDY": "Sandy Shores", "SKID": "Mission Row", "SLAB": "Stab City", "STAD": "Maze Bank Arena", "STRAW": "Strawberry", "TATAMO": "Tataviam Mountains", "TERMINA": "Terminal", "TEXTI": "Textile City", "TONGVAH": "Tongva Hills", "TONGVAV": "Tongva Valley", "VCANA": "Vespucci Canals", "VESP": "Vespucci", "VINE": "Vinewood", "WINDF": "Ron Alternates Wind Farm", "WVINE": "West Vinewood", "ZANCUDO": "Zancudo River", "ZP_ORT": "Port of South Los Santos", "ZQ_UAR": "Davis Quartz"}

class WeaponType(Enum):
    LONG_GUN = "LongGun"
    HAND_GUN = "HandGun"
    OTHER = HAND_GUN

class Weapon:
    def __init__(self, desc, name, type = WeaponType.OTHER, components = None):
        self.DESC = desc
        self.NAME = name
        self.TYPE = type
        self.COMPONENTS = list()

        if components is not None:
            self.COMPONENTS = components

    def __hash__(self):
        return hash(self.NAME)

    def __eq__(self, other):
        return hasattr(other, "NAME") and self.NAME == other.NAME

    def __ne__(self, other):
        return not self == other

    def getComponentDescs(self):
        return list(map(lambda component: component.DESC, self.COMPONENTS))

    def getComponentIDs(self):
        return list(map(lambda component: component.NAME, self.COMPONENTS))

    def getComponentByID(self, id):
        for component in self.COMPONENTS:
            if component.NAME == id:
                return component

        return None

    def getComponentByDesc(self, desc):
        for component in self.COMPONENTS:
            if component.DESC == desc:
                return component

    class Component:
        def __init__(self, desc, name):
            self.DESC = desc
            self.NAME = name

        def __hash__(self):
            return hash(self.NAME)

        def __eq__(self, other):
            return hasattr(other, "NAME") and self.NAME == other.NAME

        def __ne__(self, other):
            return not self == other

WEAPON_IDs = [
    Weapon("Antique Cavalry Dagger", "WEAPON_DAGGER"),
    Weapon("Baseball Bat", "WEAPON_BAT"),
    Weapon("Broken Bottle", "WEAPON_BOTTLE"),
    Weapon("Crowbar", "WEAPON_CROWBAR"),
    Weapon("Flashlight", "WEAPON_FLASHLIGHT"),
    Weapon("Golf Club", "WEAPON_GOLFCLUB"),
    Weapon("Hammer", "WEAPON_HAMMER"),
    Weapon("Hatchet", "WEAPON_HATCHET"),
    Weapon("Knuckle Dusters", "WEAPON_KNUCKLE", [
        Weapon.Component("The Pimp", "COMPONENT_KNUCKLE_VARMOD_PIMP"),
        Weapon.Component("The Ballas", "COMPONENT_KNUCKLE_VARMOD_BALLAS"),
        Weapon.Component("The Hustler", "COMPONENT_KNUCKLE_VARMOD_DOLLAR"),
        Weapon.Component("The Rock", "COMPONENT_KNUCKLE_VARMOD_DIAMOND"),
        Weapon.Component("The Hater", "COMPONENT_KNUCKLE_VARMOD_HATE"),
        Weapon.Component("The Lover", "COMPONENT_KNUCKLE_VARMOD_LOVE"),
        Weapon.Component("The Player", "COMPONENT_KNUCKLE_VARMOD_PLAYER"),
        Weapon.Component("The King", "COMPONENT_KNUCKLE_VARMOD_KING"),
        Weapon.Component("The Vagos", "COMPONENT_KNUCKLE_VARMOD_VAGOS"),
    ]),
    Weapon("Knife", "WEAPON_KNIFE"),
    Weapon("Machete", "WEAPON_MACHETE"),
    Weapon("Switchblade", "WEAPON_SWITCHBLADE", [
        Weapon.Component("VIP Variant", "COMPONENT_SWITCHBLADE_VARMOD_VAR1"),            
        Weapon.Component("Bodyguard Variant", "COMPONENT_SWITCHBLADE_VARMOD_VAR2")        
    ]),
    Weapon("Nightstick", "WEAPON_NIGHTSTICK"),
    Weapon("Pipe Wrench", "WEAPON_WRENCH"),
    Weapon("Battle Axe", "WEAPON_BATTLEAXE"),
    Weapon("Pool Cue", "WEAPON_POOLCUE"),
    Weapon("Stone Hatchet", "WEAPON_STONE_HATCHET"),
    Weapon("Pistol", "WEAPON_PISTOL", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_PISTOL_CLIP_02"),
        Weapon.Component("Flashlight", "COMPONENT_AT_PI_FLSH"),
        Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP_02"),
        Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_PISTOL_VARMOD_LUXE")
    ]),
    Weapon("Pistol Mk II", "WEAPON_PISTOL_MK2", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_PISTOL_MK2_CLIP_02"),
        Weapon.Component("Tracer Rounds", "COMPONENT_PISTOL_MK2_CLIP_TRACER"),
        Weapon.Component("Incendiary Rounds", "COMPONENT_PISTOL_MK2_CLIP_INCENDIARY"),
        Weapon.Component("Hollow Point Rounds", "COMPONENT_PISTOL_MK2_CLIP_HOLLOWPOINT"),
        Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_PISTOL_MK2_CLIP_FMJ"),
        Weapon.Component("Mounted Scope", "COMPONENT_AT_PI_RAIL"),
        Weapon.Component("Flashlight", "COMPONENT_AT_PI_FLSH_02"),
        Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP_02"),
        Weapon.Component("Compensator", "COMPONENT_AT_PI_COMP"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO"),
        Weapon.Component("Brushstroke Camo", "COMPONENT_PISTOL_MK2_CAMO_02"),
        Weapon.Component("Woodland Camo", "COMPONENT_PISTOL_MK2_CAMO_03"),
        Weapon.Component("Skull", "COMPONENT_PISTOL_MK2_CAMO_04"),
        Weapon.Component("Sessanta Nove", "COMPONENT_PISTOL_MK2_CAMO_05"),
        Weapon.Component("Perseus", "COMPONENT_PISTOL_MK2_CAMO_06"),
        Weapon.Component("Leopard", "COMPONENT_PISTOL_MK2_CAMO_07"),
        Weapon.Component("Zebra", "COMPONENT_PISTOL_MK2_CAMO_08"),
        Weapon.Component("Geometric", "COMPONENT_PISTOL_MK2_CAMO_09"),
        Weapon.Component("Boom!", "COMPONENT_PISTOL_MK2_CAMO_10"),
        Weapon.Component("Patriotic", "COMPONENT_PISTOL_MK2_CAMO_IND_01"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_SLIDE"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_02_SLIDE"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_03_SLIDE"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_04_SLIDE"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_05_SLIDE"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_06_SLIDE"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_07_SLIDE"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_08_SLIDE"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_09_SLIDE"),
        Weapon.Component("Digital Camo", "COMPONENT_PISTOL_MK2_CAMO_10_SLIDE"),
        Weapon.Component("Patriotic", "COMPONENT_PISTOL_MK2_CAMO_IND_01_SLIDE")
    ]),
    Weapon("Combat Pistol", "WEAPON_COMBATPISTOL", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_COMBATPISTOL_CLIP_02"),
        Weapon.Component("Flashlight", "COMPONENT_AT_PI_FLSH"),
        Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP"),
        Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_COMBATPISTOL_VARMOD_LOWRIDER")
    ]),
    Weapon("AP Pistol", "WEAPON_APPISTOL", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_APPISTOL_CLIP_02"),
        Weapon.Component("Flashlight", "COMPONENT_AT_PI_FLSH"),
        Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP"),
        Weapon.Component("Gilded Gun Metal Finish", "COMPONENT_APPISTOL_VARMOD_LUXE")
    ]),
    Weapon("Stungun", "WEAPON_STUNGUN"),
    Weapon("Pistol .50", "WEAPON_PISTOL50", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_PISTOL50_CLIP_02"),
        Weapon.Component("Flashlight", "COMPONENT_AT_PI_FLSH"),
        Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
        Weapon.Component("Platinum Pearl Deluxe Finish", "COMPONENT_PISTOL50_VARMOD_LUXE")
    ]),
    Weapon("SNS Pistol", "WEAPON_SNSPISTOL", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_SNSPISTOL_CLIP_02"),
        Weapon.Component("Etched Wood Grip Finish", "COMPONENT_SNSPISTOL_VARMOD_LOWRIDER")
    ]),
    Weapon("SNS Pistol Mk II", "WEAPON_SNSPISTOL_MK2", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_SNSPISTOL_MK2_CLIP_02"),
        Weapon.Component("Tracer Rounds", "COMPONENT_SNSPISTOL_MK2_CLIP_TRACER"),
        Weapon.Component("Incendiary Rounds", "COMPONENT_SNSPISTOL_MK2_CLIP_INCENDIARY"),
        Weapon.Component("Hollow Point Rounds", "COMPONENT_SNSPISTOL_MK2_CLIP_HOLLOWPOINT"),
        Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_SNSPISTOL_MK2_CLIP_FMJ"),
        Weapon.Component("Flashlight", "COMPONENT_AT_PI_FLSH_03"),
        Weapon.Component("Mounted Scope", "COMPONENT_AT_PI_RAIL_02"),
        Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP_02"),
        Weapon.Component("Compensator", "COMPONENT_AT_PI_COMP_02"),
        Weapon.Component("Digital Camo", "COMPONENT_SNSPISTOL_MK2_CAMO"),
        Weapon.Component("Brushstroke Camo", "COMPONENT_SNSPISTOL_MK2_CAMO_02"),
        Weapon.Component("Woodland Camo", "COMPONENT_SNSPISTOL_MK2_CAMO_03"),
        Weapon.Component("Skull", "COMPONENT_SNSPISTOL_MK2_CAMO_04"),
        Weapon.Component("Sessanta Nove", "COMPONENT_SNSPISTOL_MK2_CAMO_05"),
        Weapon.Component("Perseus", "COMPONENT_SNSPISTOL_MK2_CAMO_06"),
        Weapon.Component("Leopard", "COMPONENT_SNSPISTOL_MK2_CAMO_07"),
        Weapon.Component("Zebra", "COMPONENT_SNSPISTOL_MK2_CAMO_08"),
        Weapon.Component("Geometric", "COMPONENT_SNSPISTOL_MK2_CAMO_09"),
        Weapon.Component("Boom!", "COMPONENT_SNSPISTOL_MK2_CAMO_10"),
        Weapon.Component("Boom!", "COMPONENT_SNSPISTOL_MK2_CAMO_IND_01"),
        Weapon.Component("Digital Camo", "COMPONENT_SNSPISTOL_MK2_CAMO_SLIDE"),
        Weapon.Component("Brushstroke Camo", "COMPONENT_SNSPISTOL_MK2_CAMO_02_SLIDE"),
        Weapon.Component("Woodland Camo", "COMPONENT_SNSPISTOL_MK2_CAMO_03_SLIDE"),
        Weapon.Component("Skull", "COMPONENT_SNSPISTOL_MK2_CAMO_04_SLIDE"),
        Weapon.Component("Sessanta Nove", "COMPONENT_SNSPISTOL_MK2_CAMO_05_SLIDE"),
        Weapon.Component("Perseus", "COMPONENT_SNSPISTOL_MK2_CAMO_06_SLIDE"),
        Weapon.Component("Leopard", "COMPONENT_SNSPISTOL_MK2_CAMO_07_SLIDE"),
        Weapon.Component("Zebra", "COMPONENT_SNSPISTOL_MK2_CAMO_08_SLIDE"),
        Weapon.Component("Geometric", "COMPONENT_SNSPISTOL_MK2_CAMO_09_SLIDE"),
        Weapon.Component("Boom!", "COMPONENT_SNSPISTOL_MK2_CAMO_10_SLIDE"),
        Weapon.Component("Patriotic", "COMPONENT_SNSPISTOL_MK2_CAMO_IND_01_SLIDE")
    ]),
    Weapon("Heavy Pistol", "WEAPON_HEAVY_PISTOL", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_HEAVYPISTOL_CLIP_02"),
        Weapon.Component("Flashlight", "COMPONENT_AT_PI_FLSH"),
        Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP"),
        Weapon.Component("Etched Wood Grip Finish", "COMPONENT_HEAVYPISTOL_VARMOD_LUX")
    ]),
    Weapon("Vintage Pistol", "WEAPON_VINTAGE_PISTOL", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_VINTAGEPISTOL_CLIP_02"),
        Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP")
    ]),
    Weapon("Flare Gun", "WEAPON_FLAREGUN"),
    Weapon("Marksman Pistol", "WEAPON_MARKSMANPISTOL", WeaponType.HAND_GUN),
    Weapon("Heavy Revolver", "WEAPON_REVOLVER", WeaponType.HAND_GUN, [
        Weapon.Component("VIP Variant", "COMPONENT_REVOLVER_VARMOD_BOSS"),
        Weapon.Component("Bodyguard Variant", "COMPONENT_REVOLVER_VARMOD_GOON")       
    ]),
    Weapon("Heavy Revolver Mk II", "WEAPON_REVOLVER_MK2", WeaponType.HAND_GUN, [
        Weapon.Component("Tracer Rounds", "COMPONENT_REVOLVER_MK2_CLIP_TRACER"),
        Weapon.Component("Incendiary Rounds", "COMPONENT_REVOLVER_MK2_CLIP_INCENDIARY"),
        Weapon.Component("Hollow Point Rounds", "COMPONENT_REVOLVER_MK2_CLIP_HOLLOWPOINT"),
        Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_REVOLVER_MK2_CLIP_FMJ"),
        Weapon.Component("Holographic Sight", "COMPONENT_AT_SIGHTS"),
        Weapon.Component("Small Scope", "COMPONENT_AT_SCOPE_MACRO_MK2"),
        Weapon.Component("Flashlight", "COMPONENT_AT_PI_FLSH"),
        Weapon.Component("Compensator", "COMPONENT_AT_PI_COMP_03"),
        Weapon.Component("Digital Camo", "COMPONENT_REVOLVER_MK2_CAMO"),
        Weapon.Component("Brushstroke Camo", "COMPONENT_REVOLVER_MK2_CAMO_02"),
        Weapon.Component("Woodland Camo", "COMPONENT_REVOLVER_MK2_CAMO_03"),
        Weapon.Component("Skull", "COMPONENT_REVOLVER_MK2_CAMO_04"),
        Weapon.Component("Sessanta Nove", "COMPONENT_REVOLVER_MK2_CAMO_05"),
        Weapon.Component("Perseus", "COMPONENT_REVOLVER_MK2_CAMO_06"),
        Weapon.Component("Leopard", "COMPONENT_REVOLVER_MK2_CAMO_07"),
        Weapon.Component("Zebra", "COMPONENT_REVOLVER_MK2_CAMO_08"),
        Weapon.Component("Geometric", "COMPONENT_REVOLVER_MK2_CAMO_09"),
        Weapon.Component("Boom!", "COMPONENT_REVOLVER_MK2_CAMO_10"),
        Weapon.Component("Patriotic", "COMPONENT_REVOLVER_MK2_CAMO_IND_01")
    ]),
    Weapon("Double Action Revolver", "WEAPON_DOUBLEACTION", WeaponType.HAND_GUN),
    Weapon("Up-n-Atomizer", "WEAPON_RAYPISTOL", WeaponType.HAND_GUN, [
        Weapon.Component("Festive tint", "COMPONENT_RAYPISTOL_VARMOD_XMAS18")
    ]),
    Weapon("Micro SMG", "WEAPON_MICROSMG", WeaponType.HAND_GUN, [
		Weapon.Component("Extended Clip", "COMPONENT_MICROSMG_CLIP_02"),
		Weapon.Component("Flashlight", "COMPONENT_AT_PI_FLSH"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_MACRO"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
		Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_MICROSMG_VARMOD_LUXE")
    ]),
    Weapon("SMG", "WEAPON_SMG", WeaponType.HAND_GUN, [
		Weapon.Component("Extended Clip", "COMPONENT_SMG_CLIP_02"),
		Weapon.Component("Drum Magazine", "COMPONENT_SMG_CLIP_03"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_MACRO_02"),
		Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP"),
		Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_SMG_VARMOD_LUXE")
    ]),
    Weapon("SMG Mk II", "WEAPON_SMG_MK2", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_SMG_MK2_CLIP_02"),
		Weapon.Component("Tracer Rounds", "COMPONENT_SMG_MK2_CLIP_TRACER"),
		Weapon.Component("Incendiary Rounds", "COMPONENT_SMG_MK2_CLIP_INCENDIARY"),
		Weapon.Component("Hollow Point Rounds", "COMPONENT_SMG_MK2_CLIP_HOLLOWPOINT"),
		Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_SMG_MK2_CLIP_FMJ"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Holographic Sight", "COMPONENT_AT_SIGHTS_SMG"),
		Weapon.Component("Small Scope", "COMPONENT_AT_SCOPE_MACRO_02_SMG_MK2"),
		Weapon.Component("Medium Scope", "COMPONENT_AT_SCOPE_SMALL_SMG_MK2"),
		Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP"),
		Weapon.Component("Flat Muzzle Brake", "COMPONENT_AT_MUZZLE_01"),
		Weapon.Component("Tactical Muzzle Brake", "COMPONENT_AT_MUZZLE_02"),
		Weapon.Component("Fat-End Muzzle Brake", "COMPONENT_AT_MUZZLE_03"),
		Weapon.Component("Precision Muzzle Brake", "COMPONENT_AT_MUZZLE_04"),
		Weapon.Component("Heavy Duty Muzzle Brake", "COMPONENT_AT_MUZZLE_05"),
		Weapon.Component("Slanted Muzzle Brake", "COMPONENT_AT_MUZZLE_06"),
		Weapon.Component("Split-End Muzzle Brake", "COMPONENT_AT_MUZZLE_07"),
		Weapon.Component("Default Barrel", "COMPONENT_AT_SB_BARREL_01"),
		Weapon.Component("Heavy Barrel", "COMPONENT_AT_SB_BARREL_02"),
		Weapon.Component("Digital Camo", "COMPONENT_SMG_MK2_CAMO"),
		Weapon.Component("Brushstroke Camo", "COMPONENT_SMG_MK2_CAMO_02"),
		Weapon.Component("Woodland Camo", "COMPONENT_SMG_MK2_CAMO_03"),
		Weapon.Component("Skull", "COMPONENT_SMG_MK2_CAMO_04"),
		Weapon.Component("Sessanta Nove", "COMPONENT_SMG_MK2_CAMO_05"),
		Weapon.Component("Perseus", "COMPONENT_SMG_MK2_CAMO_06"),
		Weapon.Component("Leopard", "COMPONENT_SMG_MK2_CAMO_07"),
		Weapon.Component("Zebra", "COMPONENT_SMG_MK2_CAMO_08"),
		Weapon.Component("Geometric", "COMPONENT_SMG_MK2_CAMO_09"),
		Weapon.Component("Boom!", "COMPONENT_SMG_MK2_CAMO_10"),
		Weapon.Component("Patriotic", "COMPONENT_SMG_MK2_CAMO_IND_01")
    ]),
    Weapon("Assault SMG", "WEAPON_ASSAULTSMG", WeaponType.HAND_GUN, [
		Weapon.Component("Extended Clip", "COMPONENT_ASSAULTSMG_CLIP_02"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_MACRO"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
		Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_ASSAULTSMG_VARMOD_LOWRIDER")
    ]),
    Weapon("Combat PDW", "WEAPON_COMBATPDW", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_COMBATPDW_CLIP_02"),
		Weapon.Component("Drum Magazine", "COMPONENT_COMBATPDW_CLIP_03"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_SMALL")
    ]),
    Weapon("Machine Pistol", "WEAPON_MACHINEPISTOL", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_MACHINEPISTOL_CLIP_02"),
		Weapon.Component("Drum Magazine", "COMPONENT_MACHINEPISTOL_CLIP_03"),
		Weapon.Component("Suppressor", "COMPONENT_AT_PI_SUPP")
    ]),
    Weapon("Mini SMG", "WEAPON_MINISMG", WeaponType.HAND_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_MINISMG_CLIP_02")
    ]),
    Weapon("Unholy Hellbringer", "WEAPON_RAYCARBINE", WeaponType.HAND_GUN),
    Weapon("Pump Shotgun", "WEAPON_PUMPSHOTGUN", WeaponType.LONG_GUN, [
        Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Suppressor", "COMPONENT_AT_SR_SUPP"),
		Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_PUMPSHOTGUN_VARMOD_LOWRIDER")
    ]),
    Weapon("Pump Shotgun Mk II", "WEAPON_PUMPSHOTGUN_MK2", WeaponType.LONG_GUN, [
        Weapon.Component("Dragon's Breath Shells", "COMPONENT_PUMPSHOTGUN_MK2_CLIP_INCENDIARY"),
		Weapon.Component("Steel Buckshot Shells", "COMPONENT_PUMPSHOTGUN_MK2_CLIP_ARMORPIERCING"),
		Weapon.Component("Flechette Shells", "COMPONENT_PUMPSHOTGUN_MK2_CLIP_HOLLOWPOINT"),
		Weapon.Component("Explosive Slugs", "COMPONENT_PUMPSHOTGUN_MK2_CLIP_EXPLOSIVE"),
		Weapon.Component("Holographic Sight", "COMPONENT_AT_SIGHTS"),
		Weapon.Component("Small Scope", "COMPONENT_AT_SCOPE_MACRO_MK2"),
		Weapon.Component("Medium Scope", "COMPONENT_AT_SCOPE_SMALL_MK2"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Suppressor", "COMPONENT_AT_SR_SUPP_03"),
		Weapon.Component("Squared Muzzle Brake", "COMPONENT_AT_MUZZLE_08"),
		Weapon.Component("Digital Camo", "COMPONENT_PUMPSHOTGUN_MK2_CAMO"),
		Weapon.Component("Brushstroke Camo", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_02"),
		Weapon.Component("Woodland Camo", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_03"),
		Weapon.Component("Skull", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_04"),
		Weapon.Component("Sessanta Nove", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_05"),
		Weapon.Component("Perseus", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_06"),
		Weapon.Component("Leopard", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_07"),
		Weapon.Component("Zebra", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_08"),
		Weapon.Component("Geometric", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_09"),
		Weapon.Component("Boom!", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_10"),
		Weapon.Component("Patriotic", "COMPONENT_PUMPSHOTGUN_MK2_CAMO_IND_01")
    ]),
    Weapon("Sawed-Off Shotgun", "WEAPON_SAWNOFFSHOTGUN", WeaponType.LONG_GUN, [
        Weapon.Component("Gilded Gun Metal Finish", "COMPONENT_SAWNOFFSHOTGUN_VARMOD_LUXE")
    ]),
    Weapon("Assault Shotgun", "WEAPON_ASSAULTSHOTGUN", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_ASSAULTSHOTGUN_CLIP_02"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP")
    ]),
    Weapon("Bullpup Shotgun", "WEAPON_BULLPUPSHOTGUN", WeaponType.LONG_GUN, [
        Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP")
    ]),
    Weapon("Musket", "WEAPON_MUSKET", WeaponType.LONG_GUN),
    Weapon("Heavy Shotgun", "WEAPON_HEAVYSHOTGUN", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_HEAVYSHOTGUN_CLIP_02"),
		Weapon.Component("Drum Magazine", "COMPONENT_HEAVYSHOTGUN_CLIP_03"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP")
    ]),
    Weapon("Double Barrel Shotgun", "WEAPON_DBSHOTGUN", WeaponType.LONG_GUN),
    Weapon("Sweeper Shotgun", "WEAPON_AUTOSHOTGUN", WeaponType.LONG_GUN),
    Weapon("Assault Rifle", "WEAPON_ASSAULTRIFLE", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_ASSAULTRIFLE_CLIP_02"),
		Weapon.Component("Drum Magazine", "COMPONENT_ASSAULTRIFLE_CLIP_03"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_MACRO"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP"),
		Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_ASSAULTRIFLE_VARMOD_LUXE")
    ]),
    Weapon("Assault Rifle Mk II", "WEAPON_ASSAULTRIFLE_MK2", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_ASSAULTRIFLE_MK2_CLIP_02"),
		Weapon.Component("Tracer Rounds", "COMPONENT_ASSAULTRIFLE_MK2_CLIP_TRACER"),
		Weapon.Component("Incendiary Rounds", "COMPONENT_ASSAULTRIFLE_MK2_CLIP_INCENDIARY"),
		Weapon.Component("Armor Piercing Rounds", "COMPONENT_ASSAULTRIFLE_MK2_CLIP_ARMORPIERCING"),
		Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_ASSAULTRIFLE_MK2_CLIP_FMJ"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP_02"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Holographic Sight", "COMPONENT_AT_SIGHTS"),
		Weapon.Component("Small Scope", "COMPONENT_AT_SCOPE_MACRO_MK2"),
		Weapon.Component("Large Scope", "COMPONENT_AT_SCOPE_MEDIUM_MK2"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
		Weapon.Component("Flat Muzzle Brake", "COMPONENT_AT_MUZZLE_01"),
		Weapon.Component("Tactical Muzzle Brake", "COMPONENT_AT_MUZZLE_02"),
		Weapon.Component("Fat-End Muzzle Brake", "COMPONENT_AT_MUZZLE_03"),
		Weapon.Component("Precision Muzzle Brake", "COMPONENT_AT_MUZZLE_04"),
		Weapon.Component("Heavy Duty Muzzle Brake", "COMPONENT_AT_MUZZLE_05"),
		Weapon.Component("Slanted Muzzle Brake", "COMPONENT_AT_MUZZLE_06"),
		Weapon.Component("Split-End Muzzle Brake", "COMPONENT_AT_MUZZLE_07"),
		Weapon.Component("Default Barrel", "COMPONENT_AT_AR_BARREL_01"),
		Weapon.Component("Heavy Barrel", "COMPONENT_AT_AR_BARREL_02"),
		Weapon.Component("Digital Camo", "COMPONENT_ASSAULTRIFLE_MK2_CAMO"),
		Weapon.Component("Brushstroke Camo", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_02"),
		Weapon.Component("Woodland Camo", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_03"),
		Weapon.Component("Skull", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_04"),
		Weapon.Component("Sessanta Nove", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_05"),
		Weapon.Component("Perseus", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_06"),
		Weapon.Component("Leopard", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_07"),
		Weapon.Component("Zebra", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_08"),
		Weapon.Component("Geometric", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_09"),
		Weapon.Component("Boom!", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_10"),
		Weapon.Component("Patriotic", "COMPONENT_ASSAULTRIFLE_MK2_CAMO_IND_01")
    ]),
    Weapon("Carbine Rifle", "WEAPON_CARBINERIFLE", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_CARBINERIFLE_CLIP_02"),
		Weapon.Component("Box Magazine", "COMPONENT_CARBINERIFLE_CLIP_03"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_MEDIUM"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP"),
		Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_CARBINERIFLE_VARMOD_LUXE")
    ]),
    Weapon("Carbine Rifle Mk II", "WEAPON_CARBINERIFLE_MK2", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_CARBINERIFLE_MK2_CLIP_02"),
		Weapon.Component("Tracer Rounds", "COMPONENT_CARBINERIFLE_MK2_CLIP_TRACER"),
		Weapon.Component("Incendiary Rounds", "COMPONENT_CARBINERIFLE_MK2_CLIP_INCENDIARY"),
		Weapon.Component("Armor Piercing Rounds", "COMPONENT_CARBINERIFLE_MK2_CLIP_ARMORPIERCING"),
		Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_CARBINERIFLE_MK2_CLIP_FMJ"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP_02"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Holographic Sight", "COMPONENT_AT_SIGHTS"),
		Weapon.Component("Small Scope", "COMPONENT_AT_SCOPE_MACRO_MK2"),
		Weapon.Component("Large Scope", "COMPONENT_AT_SCOPE_MEDIUM_MK2"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP"),
		Weapon.Component("Flat Muzzle Brake", "COMPONENT_AT_MUZZLE_01"),
		Weapon.Component("Tactical Muzzle Brake", "COMPONENT_AT_MUZZLE_02"),
		Weapon.Component("Fat-End Muzzle Brake", "COMPONENT_AT_MUZZLE_03"),
		Weapon.Component("Precision Muzzle Brake", "COMPONENT_AT_MUZZLE_04"),
		Weapon.Component("Heavy Duty Muzzle Brake", "COMPONENT_AT_MUZZLE_05"),
		Weapon.Component("Slanted Muzzle Brake", "COMPONENT_AT_MUZZLE_06"),
		Weapon.Component("Split-End Muzzle Brake", "COMPONENT_AT_MUZZLE_07"),
		Weapon.Component("Default Barrel", "COMPONENT_AT_CR_BARREL_01"),
		Weapon.Component("Heavy Barrel", "COMPONENT_AT_CR_BARREL_02"),
		Weapon.Component("Digital Camo", "COMPONENT_CARBINERIFLE_MK2_CAMO"),
		Weapon.Component("Brushstroke Camo", "COMPONENT_CARBINERIFLE_MK2_CAMO_02"),
		Weapon.Component("Woodland Camo", "COMPONENT_CARBINERIFLE_MK2_CAMO_03"),
		Weapon.Component("Skull", "COMPONENT_CARBINERIFLE_MK2_CAMO_04"),
		Weapon.Component("Sessanta Nove", "COMPONENT_CARBINERIFLE_MK2_CAMO_05"),
		Weapon.Component("Perseus", "COMPONENT_CARBINERIFLE_MK2_CAMO_06"),
		Weapon.Component("Leopard", "COMPONENT_CARBINERIFLE_MK2_CAMO_07"),
		Weapon.Component("Zebra", "COMPONENT_CARBINERIFLE_MK2_CAMO_08"),
		Weapon.Component("Geometric", "COMPONENT_CARBINERIFLE_MK2_CAMO_09"),
		Weapon.Component("Boom!", "COMPONENT_CARBINERIFLE_MK2_CAMO_10"),
		Weapon.Component("Patriotic", "COMPONENT_CARBINERIFLE_MK2_CAMO_IND_01")
    ]),
    Weapon("Advanced Rifle", "WEAPON_ADVANCEDRIFLE", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_ADVANCEDRIFLE_CLIP_02"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_SMALL"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP"),
		Weapon.Component("Gilded Gun Metal Finish", "COMPONENT_ADVANCEDRIFLE_VARMOD_LUXE")
    ]),
    Weapon("Special Carbine", "WEAPON_SPECIALCARBINE", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_SPECIALCARBINE_CLIP_02"),
		Weapon.Component("Drum Magazine", "COMPONENT_SPECIALCARBINE_CLIP_03"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_MEDIUM"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP"),
		Weapon.Component("Etched Gun Metal Finish", "COMPONENT_SPECIALCARBINE_VARMOD_LOWRIDER")
    ]),
    Weapon("Special Carbine Mk II", "WEAPON_SPECIALCARBINE_MK2", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_SPECIALCARBINE_MK2_CLIP_02"),
		Weapon.Component("Tracer Rounds", "COMPONENT_SPECIALCARBINE_MK2_CLIP_TRACER"),
		Weapon.Component("Incendiary Rounds", "COMPONENT_SPECIALCARBINE_MK2_CLIP_INCENDIARY"),
		Weapon.Component("Armor Piercing Rounds", "COMPONENT_SPECIALCARBINE_MK2_CLIP_ARMORPIERCING"),
		Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_SPECIALCARBINE_MK2_CLIP_FMJ"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Holographic Sight", "COMPONENT_AT_SIGHTS"),
		Weapon.Component("Small Scope", "COMPONENT_AT_SCOPE_MACRO_MK2"),
		Weapon.Component("Large Scope", "COMPONENT_AT_SCOPE_MEDIUM_MK2"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
		Weapon.Component("Flat Muzzle Brake", "COMPONENT_AT_MUZZLE_01"),
		Weapon.Component("Tactical Muzzle Brake", "COMPONENT_AT_MUZZLE_02"),
		Weapon.Component("Fat-End Muzzle Brake", "COMPONENT_AT_MUZZLE_03"),
		Weapon.Component("Precision Muzzle Brake", "COMPONENT_AT_MUZZLE_04"),
		Weapon.Component("Heavy Duty Muzzle Brake", "COMPONENT_AT_MUZZLE_05"),
		Weapon.Component("Slanted Muzzle Brake", "COMPONENT_AT_MUZZLE_06"),
		Weapon.Component("Split-End Muzzle Brake", "COMPONENT_AT_MUZZLE_07"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP_02"),
		Weapon.Component("Default Barrel", "COMPONENT_AT_SC_BARREL_01"),
		Weapon.Component("Heavy Barrel", "COMPONENT_AT_SC_BARREL_02"),
		Weapon.Component("Digital Camo", "COMPONENT_SPECIALCARBINE_MK2_CAMO"),
		Weapon.Component("Brushstroke Camo", "COMPONENT_SPECIALCARBINE_MK2_CAMO_02"),
		Weapon.Component("Woodland Camo", "COMPONENT_SPECIALCARBINE_MK2_CAMO_03"),
		Weapon.Component("Skull", "COMPONENT_SPECIALCARBINE_MK2_CAMO_04"),
		Weapon.Component("Sessanta Nove", "COMPONENT_SPECIALCARBINE_MK2_CAMO_05"),
		Weapon.Component("Perseus", "COMPONENT_SPECIALCARBINE_MK2_CAMO_06"),
		Weapon.Component("Leopard", "COMPONENT_SPECIALCARBINE_MK2_CAMO_07"),
		Weapon.Component("Zebra", "COMPONENT_SPECIALCARBINE_MK2_CAMO_08"),
		Weapon.Component("Geometric", "COMPONENT_SPECIALCARBINE_MK2_CAMO_09"),
		Weapon.Component("Boom!", "COMPONENT_SPECIALCARBINE_MK2_CAMO_10"),
		Weapon.Component("Patriotic", "COMPONENT_SPECIALCARBINE_MK2_CAMO_IND_01")
    ]),
    Weapon("Bullpup Rifle", "WEAPON_BULLPUPRIFLE", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_BULLPUPRIFLE_CLIP_02"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_SMALL"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP"),
		Weapon.Component("Gilded Gun Metal Finish", "COMPONENT_BULLPUPRIFLE_VARMOD_LOW")
    ]),
    Weapon("Bullpup Rifle Mk II", "WEAPON_BULLPUPRIFLE_MK2", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_BULLPUPRIFLE_MK2_CLIP_02"),
		Weapon.Component("Tracer Rounds", "COMPONENT_BULLPUPRIFLE_MK2_CLIP_TRACER"),
		Weapon.Component("Incendiary Rounds", "COMPONENT_BULLPUPRIFLE_MK2_CLIP_INCENDIARY"),
		Weapon.Component("Armor Piercing Rounds", "COMPONENT_BULLPUPRIFLE_MK2_CLIP_ARMORPIERCING"),
		Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_BULLPUPRIFLE_MK2_CLIP_FMJ"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Holographic Sight", "COMPONENT_AT_SIGHTS"),
		Weapon.Component("Small Scope", "COMPONENT_AT_SCOPE_MACRO_02_MK2"),
		Weapon.Component("Medium Scope", "COMPONENT_AT_SCOPE_SMALL_MK2"),
		Weapon.Component("Default Barrel", "COMPONENT_AT_BP_BARREL_01"),
		Weapon.Component("Heavy Barrel", "COMPONENT_AT_BP_BARREL_02"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP"),
		Weapon.Component("Flat Muzzle Brake", "COMPONENT_AT_MUZZLE_01"),
		Weapon.Component("Tactical Muzzle Brake", "COMPONENT_AT_MUZZLE_02"),
		Weapon.Component("Fat-End Muzzle Brake", "COMPONENT_AT_MUZZLE_03"),
		Weapon.Component("Precision Muzzle Brake", "COMPONENT_AT_MUZZLE_04"),
		Weapon.Component("Heavy Duty Muzzle Brake", "COMPONENT_AT_MUZZLE_05"),
		Weapon.Component("Slanted Muzzle Brake", "COMPONENT_AT_MUZZLE_06"),
		Weapon.Component("Split-End Muzzle Brake", "COMPONENT_AT_MUZZLE_07"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP_02"),
		Weapon.Component("Digital Camo", "COMPONENT_BULLPUPRIFLE_MK2_CAMO"),
		Weapon.Component("Brushstroke Camo", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_02"),
		Weapon.Component("Woodland Camo", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_03"),
		Weapon.Component("Skull", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_04"),
		Weapon.Component("Sessanta Nove", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_05"),
		Weapon.Component("Perseus", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_06"),
		Weapon.Component("Leopard", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_07"),
		Weapon.Component("Zebra", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_08"),
		Weapon.Component("Geometric", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_09"),
		Weapon.Component("Boom!", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_10"),
		Weapon.Component("Patriotic", "COMPONENT_BULLPUPRIFLE_MK2_CAMO_IND_01")
    ]),
    Weapon("Compact Rifle", "WEAPON_COMPACTRIFLE", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_COMPACTRIFLE_CLIP_02"),
		Weapon.Component("Drum Magazine", "COMPONENT_COMPACTRIFLE_CLIP_03")
    ]),
    Weapon("MG", "WEAPON_MG", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_MG_CLIP_02"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_SMALL_02"),
		Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_MG_VARMOD_LOWRIDER")
    ]),
    Weapon("Combat MG", "WEAPON_COMBATMG", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_COMBATMG_CLIP_02"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_MEDIUM"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP"),
		Weapon.Component("Etched Gun Metal Finish", "COMPONENT_COMBATMG_VARMOD_LOWRIDER")
    ]),
    Weapon("Combat MG Mk II", "WEAPON_COMBATMG_MK2", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_COMBATMG_MK2_CLIP_02"),
		Weapon.Component("Tracer Rounds", "COMPONENT_COMBATMG_MK2_CLIP_TRACER"),
		Weapon.Component("Incendiary Rounds", "COMPONENT_COMBATMG_MK2_CLIP_INCENDIARY"),
		Weapon.Component("Armor Piercing Rounds", "COMPONENT_COMBATMG_MK2_CLIP_ARMORPIERCING"),
		Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_COMBATMG_MK2_CLIP_FMJ"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP_02"),
		Weapon.Component("Holographic Sight", "COMPONENT_AT_SIGHTS"),
		Weapon.Component("Medium Scope", "COMPONENT_AT_SCOPE_SMALL_MK2"),
		Weapon.Component("Large Scope", "COMPONENT_AT_SCOPE_MEDIUM_MK2"),
		Weapon.Component("Flat Muzzle Brake", "COMPONENT_AT_MUZZLE_01"),
		Weapon.Component("Tactical Muzzle Brake", "COMPONENT_AT_MUZZLE_02"),
		Weapon.Component("Fat-End Muzzle Brake", "COMPONENT_AT_MUZZLE_03"),
		Weapon.Component("Precision Muzzle Brake", "COMPONENT_AT_MUZZLE_04"),
		Weapon.Component("Heavy Duty Muzzle Brake", "COMPONENT_AT_MUZZLE_05"),
		Weapon.Component("Slanted Muzzle Brake", "COMPONENT_AT_MUZZLE_06"),
		Weapon.Component("Split-End Muzzle Brake", "COMPONENT_AT_MUZZLE_07"),
		Weapon.Component("Default Barrel", "COMPONENT_AT_MG_BARREL_01"),
		Weapon.Component("Heavy Barrel", "COMPONENT_AT_MG_BARREL_02"),
		Weapon.Component("Digital Camo", "COMPONENT_COMBATMG_MK2_CAMO"),
		Weapon.Component("Brushstroke Camo", "COMPONENT_COMBATMG_MK2_CAMO_02"),
		Weapon.Component("Woodland Camo", "COMPONENT_COMBATMG_MK2_CAMO_03"),
		Weapon.Component("Skull", "COMPONENT_COMBATMG_MK2_CAMO_04"),
		Weapon.Component("Sessanta Nove", "COMPONENT_COMBATMG_MK2_CAMO_05"),
		Weapon.Component("Perseus", "COMPONENT_COMBATMG_MK2_CAMO_06"),
		Weapon.Component("Leopard", "COMPONENT_COMBATMG_MK2_CAMO_07"),
		Weapon.Component("Zebra", "COMPONENT_COMBATMG_MK2_CAMO_08"),
		Weapon.Component("Geometric", "COMPONENT_COMBATMG_MK2_CAMO_09"),
		Weapon.Component("Boom!", "COMPONENT_COMBATMG_MK2_CAMO_10"),
		Weapon.Component("Patriotic", "COMPONENT_COMBATMG_MK2_CAMO_IND_01")
    ]),
    Weapon("Gusenberg Sweeper", "WEAPON_GUSENBERG", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_GUSENBERG_CLIP_02")
    ]),
    Weapon("Sniper Rifle", "WEAPON_SNIPERRIFLE", WeaponType.LONG_GUN, [
        Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP_02"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_LARGE"),
		Weapon.Component("Advanced Scope", "COMPONENT_AT_SCOPE_MAX"),
		Weapon.Component("Etched Wood Grip Finish", "COMPONENT_SNIPERRIFLE_VARMOD_LUXE")
    ]),
    Weapon("Heavy Sniper", "WEAPON_HEAVYSNIPER", WeaponType.LONG_GUN, [
        Weapon.Component("Scope", "COMPONENT_AT_SCOPE_LARGE"),
		Weapon.Component("Advanced Scope", "COMPONENT_AT_SCOPE_MAX")
    ]),
    Weapon("Heavy Sniper Mk II", "WEAPON_HEAVYSNIPER_MK2", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_HEAVYSNIPER_MK2_CLIP_02"),
		Weapon.Component("Incendiary Rounds", "COMPONENT_HEAVYSNIPER_MK2_CLIP_INCENDIARY"),
		Weapon.Component("Armor Piercing Rounds", "COMPONENT_HEAVYSNIPER_MK2_CLIP_ARMORPIERCING"),
		Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_HEAVYSNIPER_MK2_CLIP_FMJ"),
		Weapon.Component("Explosive Rounds", "COMPONENT_HEAVYSNIPER_MK2_CLIP_EXPLOSIVE"),
		Weapon.Component("Zoom Scope", "COMPONENT_AT_SCOPE_LARGE_MK2"),
		Weapon.Component("Advanced Scope", "COMPONENT_AT_SCOPE_MAX"),
		Weapon.Component("Night Vision Scope", "COMPONENT_AT_SCOPE_NV"),
		Weapon.Component("Thermal Scope", "COMPONENT_AT_SCOPE_THERMAL"),
		Weapon.Component("Suppressor", "COMPONENT_AT_SR_SUPP_03"),
		Weapon.Component("Squared Muzzle Brake", "COMPONENT_AT_MUZZLE_08"),
		Weapon.Component("Bell-End Muzzle Brake", "COMPONENT_AT_MUZZLE_09"),
		Weapon.Component("Default Barrel", "COMPONENT_AT_SR_BARREL_01"),
		Weapon.Component("Heavy Barrel", "COMPONENT_AT_SR_BARREL_02"),
		Weapon.Component("Digital Camo", "COMPONENT_HEAVYSNIPER_MK2_CAMO"),
		Weapon.Component("Brushstroke Camo", "COMPONENT_HEAVYSNIPER_MK2_CAMO_02"),
		Weapon.Component("Woodland Camo", "COMPONENT_HEAVYSNIPER_MK2_CAMO_03"),
		Weapon.Component("Skull", "COMPONENT_HEAVYSNIPER_MK2_CAMO_04"),
		Weapon.Component("Sessanta Nove", "COMPONENT_HEAVYSNIPER_MK2_CAMO_05"),
		Weapon.Component("Perseus", "COMPONENT_HEAVYSNIPER_MK2_CAMO_06"),
		Weapon.Component("Leopard", "COMPONENT_HEAVYSNIPER_MK2_CAMO_07"),
		Weapon.Component("Zebra", "COMPONENT_HEAVYSNIPER_MK2_CAMO_08"),
		Weapon.Component("Geometric", "COMPONENT_HEAVYSNIPER_MK2_CAMO_09"),
		Weapon.Component("Boom!", "COMPONENT_HEAVYSNIPER_MK2_CAMO_10"),
		Weapon.Component("Patriotic", "COMPONENT_HEAVYSNIPER_MK2_CAMO_IND_01")
    ]),
    Weapon("Marksman Rifle", "WEAPON_MARKSMANRIFLE", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_MARKSMANRIFLE_CLIP_02"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_LARGE_FIXED_ZOOM"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP"),
		Weapon.Component("Yusuf Amir Luxury Finish", "COMPONENT_MARKSMANRIFLE_VARMOD_LUXE")
    ]),
    Weapon("Marksman Rifle Mk II", "WEAPON_MARKSMANRIFLE_MK2", WeaponType.LONG_GUN, [
        Weapon.Component("Extended Clip", "COMPONENT_MARKSMANRIFLE_MK2_CLIP_02"),
		Weapon.Component("Tracer Rounds", "COMPONENT_MARKSMANRIFLE_MK2_CLIP_TRACER"),
		Weapon.Component("Incendiary Rounds", "COMPONENT_MARKSMANRIFLE_MK2_CLIP_INCENDIARY"),
		Weapon.Component("Armor Piercing Rounds", "COMPONENT_MARKSMANRIFLE_MK2_CLIP_ARMORPIERCING"),
		Weapon.Component("Full Metal Jacket Rounds", "COMPONENT_MARKSMANRIFLE_MK2_CLIP_FMJ"),
		Weapon.Component("Holographic Sight", "COMPONENT_AT_SIGHTS"),
		Weapon.Component("Large Scope", "COMPONENT_AT_SCOPE_MEDIUM_MK2"),
		Weapon.Component("Zoom Scope", "COMPONENT_AT_SCOPE_LARGE_FIXED_ZOOM_MK2"),
		Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Suppressor", "COMPONENT_AT_AR_SUPP"),
		Weapon.Component("Flat Muzzle Brake", "COMPONENT_AT_MUZZLE_01"),
		Weapon.Component("Tactical Muzzle Brake", "COMPONENT_AT_MUZZLE_02"),
		Weapon.Component("Fat-End Muzzle Brake", "COMPONENT_AT_MUZZLE_03"),
		Weapon.Component("Precision Muzzle Brake", "COMPONENT_AT_MUZZLE_04"),
		Weapon.Component("Heavy Duty Muzzle Brake", "COMPONENT_AT_MUZZLE_05"),
		Weapon.Component("Slanted Muzzle Brake", "COMPONENT_AT_MUZZLE_06"),
		Weapon.Component("Split-End Muzzle Brake", "COMPONENT_AT_MUZZLE_07"),
		Weapon.Component("Default Barrel", "COMPONENT_AT_MRFL_BARREL_01"),
		Weapon.Component("Heavy Barrel", "COMPONENT_AT_MRFL_BARREL_02"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP_02"),
		Weapon.Component("Digital Camo", "COMPONENT_MARKSMANRIFLE_MK2_CAMO"),
		Weapon.Component("Brushstroke Camo", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_02"),
		Weapon.Component("Woodland Camo", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_03"),
		Weapon.Component("Skull", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_04"),
		Weapon.Component("Sessanta Nove", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_05"),
		Weapon.Component("Perseus", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_06"),
		Weapon.Component("Leopard", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_07"),
		Weapon.Component("Zebra", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_08"),
		Weapon.Component("Geometric", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_09"),
		Weapon.Component("Boom!", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_10"),
		Weapon.Component("Boom!", "COMPONENT_MARKSMANRIFLE_MK2_CAMO_IND_01")
    ]),
    Weapon("RPG", "WEAPON_RPG", WeaponType.LONG_GUN),
    Weapon("Grenade Launcher", "WEAPON_GRENADELAUNCHER", WeaponType.LONG_GUN, [
        Weapon.Component("Flashlight", "COMPONENT_AT_AR_FLSH"),
		Weapon.Component("Grip", "COMPONENT_AT_AR_AFGRIP"),
		Weapon.Component("Scope", "COMPONENT_AT_SCOPE_SMALL"),
    ]),
    Weapon("Grenade Launcher Smoke", "WEAPON_GRENADELAUNCHER_SMOKE", WeaponType.LONG_GUN),
    Weapon("Minigun", "WEAPON_MINIGUN", WeaponType.LONG_GUN),
    Weapon("Firework Launcher", "WEAPON_FIREWORK", WeaponType.LONG_GUN),
    Weapon("Railgun", "WEAPON_RAILGUN", WeaponType.LONG_GUN),
    Weapon("Homing Launcher", "WEAPON_HOMINGLAUNCHER", WeaponType.LONG_GUN),
    Weapon("Compact Grenade Launcher", "WEAPON_COMPACTLAUNCHER", WeaponType.LONG_GUN),
    Weapon("Widowmaker", "WEAPON_RAYMINIGUN", WeaponType.LONG_GUN),
    Weapon("Grenade", "WEAPON_GRENADE"),
    Weapon("BZ Gas", "WEAPON_BZGAS"),
    Weapon("Molotov Cocktail", "WEAPON_MOLOTOV"),
    Weapon("Sticky Bomb", "WEAPON_STICKYBOMB"),
    Weapon("Proximity Mines", "WEAPON_PROXMINE"),
    Weapon("Snowballs", "WEAPON_SNOWBALL"),
    Weapon("Pipe Bombs", "WEAPON_PIPEBOMB"),
    Weapon("Baseball", "WEAPON_BALL"),
    Weapon("Tear Gas", "WEAPON_SMOKEGRENADE"),
    Weapon("Flare", "WEAPON_FLARE"),
    Weapon("Jerry Can", "WEAPON_PETROLCAN"),
    Weapon("Parachute", "GADGET_PARACHUTE"),
    Weapon("Fire Extinguisher", "WEAPON_FIREEXTINGUISHER")
]

def getWeaponDescs():
    return list(map(lambda weapon: weapon.DESC, WEAPON_IDs))

def getWeaponIDs():
    return list(map(lambda weapon: weapon.NAME, WEAPON_IDs))

def getWeaponByID(id):
    for weapon in WEAPON_IDs:
        if weapon.NAME == id:
            return weapon

    return None

def getWeaponByDesc(desc):
    for weapon in WEAPON_IDs:
        if weapon.DESC == desc:
            return weapon

    return None

class IDType(Enum):
    LSPDFR = "LSPDFR"
    LSPDFR_NAME = "LSPDFR_NAME"
    EUP = "EUP"
    UB = "UB"

class Component:
    def __init__(self, desc, lspdfrID, lspdfrName, eupID = None, ubName = None):
        self.DESC = desc
        self.ID = {IDType.LSPDFR: lspdfrID, IDType.LSPDFR_NAME: lspdfrName, IDType.EUP: eupID, IDType.UB: ubName}

    def __hash__(self):
        return hash(self.ID[IDType.LSPDFR])

    def __eq__(self, other):
        return hasattr(other, "ID") and self.ID[IDType.LSPDFR] == other.ID[IDType.LSPDFR]

    def __ne__(self, other):
        return not self == other

COMPONENT_IDS = [
    Component("Head", "0", "comp_head"),
    Component("Beard/mask", "1", "comp_berd", "Mask", "comp_beard"),
    Component("Hair", "2", "comp_hair"),
    Component("Upper body", "3", "comp_uppr", "UpperSkin", "comp_shirt"),
    Component("Lower body", "4", "comp_lowr", "Pants", "comp_pants"),
    Component("Hands/arms", "5", "comp_hand", "Parachute", "comp_hands"),
    Component("Shoes/feet", "6", "comp_feet", "Shoes", "comp_shoes"),
    Component("Accessory", "7", "comp_teef", "Accessories", "comp_eyes"),
    Component("Misc.", "8", "comp_accs", "UnderCoat", "comp_accessories"),
    Component("Gear/equipment", "9", "comp_task", "Armor", "comp_tasks"),
    Component("Overlay", "10", "comp_decl", "Decal", "comp_decals"),
    Component("Misc. accessory", "11", "comp_jbib", "Top", "comp_shirtoverlay")
]

PROP_IDS = [
    Component("Headwear", "0", "prop_head", "Hat", "prop_hats"),
    Component("Eyewear", "1", "prop_eyes", "Glasses", "prop_glasses"),
    Component("Earrings/misc. head", "2", "prop_ears", "Ear", "prop_ears"),
    Component("Left wrist/forearm", "6", "prop_lwrist", "Watch", "prop_watches"),
    Component("Right wrist/forearm", "7", "prop_rwrist")
]

def getComponentByID(id):
    for component in COMPONENT_IDS:
        for idType in IDType:
            if component.ID[idType] == id:
                return component

    return None

def getPropByID(id):
    for prop in PROP_IDS:
        for idType in IDType:
            if prop.ID[idType] == id:
                return prop

    return None

inventories = list()
outfits = list()
agencies = list()
stations = list()
regions = list()
backups = list()

def getInventoryByScriptName(scriptName):
    for inventory in inventories:
        if inventory.getScriptName() == scriptName:
            return inventory
    return None

def getInventoryScriptNames():
    return list(map(lambda inventory: inventory.getScriptName(), inventories))

def getOutfitByScriptName(scriptName):
    for outfit in outfits:
        if outfit.getScriptName() == scriptName:
            return outfit
    return None

def getOutfitScriptNames():
    outfitScriptNames = list()
    for outfit in outfits:
        outfitScriptNames.append(outfit.getScriptName())
        outfitScriptNames = outfitScriptNames + list(map(lambda variation: outfit.getScriptName() + "." + variation, outfit.getVariationScriptNames()))
    return outfitScriptNames

def getOutfitUBSettings(outfitName, isMale):
    settings = dict()
    outfit = getOutfitByScriptName(outfitName.split(".")[0])

    variation = None
    if len(outfitName.split(".")) > 1:
        variation = outfit.getVariationByScriptName(outfitName.split(".")[1])
    else:
        for variationCandidate in outfit.variations:
             if not isMale ^ (variationCandidate.gender == "male"):
                 variation = variationCandidate
                 break

    if variation:
        for component in variation.components:
            id = component.id.ID[IDType.UB]

            if id is None:
                continue

            drawable = str(int(list(map(lambda drawable: drawable.split("-")[0], component.drawable.split(",")))[0]) + 1)
            texture = int(list(map(lambda texture: texture.split("-")[0], component.texture.split(",")))[0]) + 1

            settings[id] = drawable
            if texture > 1:
                settings[id.replace("comp_", "tex_")] = str(texture)

        for prop in variation.props:
            id = component.id.ID[IDType.UB]

            if id is None:
                continue

            drawable = str(int(list(map(lambda drawable: drawable.split("-")[0], prop.drawable.split(",")))[0]) + 1)
            texture = int(list(map(lambda texture: texture.split("-")[0], prop.texture.split(",")))[0]) + 1

            settings[id] = drawable
            if texture > 1:
                settings[id.replace("prop_", "tex_")] = str(texture)

    return settings

def getAgencyByScriptName(scriptName):
    for agency in agencies:
        if agency.getScriptName() == scriptName:
            return agency
    return None

def getAgencyScriptNames():
    return list(map(lambda agency: agency.getScriptName(), agencies))

def getStationByScriptName(scriptName):
    for station in stations:
        if station.scriptName == scriptName:
            return station
    return None

def getRegionByName(name):
    for region in regions:
        if region.getName() == name:
            return region
    return None

def getAvailableZones():
    availableZones = list(ZONES.keys())
    for region in regions:
        availableZones = list(filter(lambda zone: zone not in region.zones, availableZones))
    return availableZones

def getBackupsByType(type):
    return list(filter(lambda backup: backup.type == type.name, backups))

class Dialog(Toplevel):
    def __init__(self, master, title = None, **kw):
        super().__init__(master, **kw)

        self.transient(master)

        if title:
            self.title(title)

        self._build()

        self._return_grab = self.grab_current()
        self.grab_set()

        self.update_idletasks()
        startX = max(0, min(master.winfo_rootx() + 50, self.winfo_screenwidth() - self.winfo_width() - 50))
        startY = max(0, min(master.winfo_rooty() + 50, self.winfo_screenheight() - self.winfo_height() - 50))
        self.geometry("+{}+{}".format(startX, startY))

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.wait_window(self)

    def _build(self):
        pass

    def close(self):
        if self._return_grab:
            self._return_grab.grab_set()
        else:
            self.master.focus_set()

        self.destroy()

    @staticmethod
    def askcustom(title = None, message = None, default = None, buttons = ["Okay"]):
        class CustomMessagebox(Dialog):
            def __init__(self, title, message, default, buttons):
                self._message = message
                self.result = default
                self._buttons = buttons

                w = Frame(None)
                super().__init__(w.focus_get(), title)

            def _build(self):
                message = Label(self, text = self._message)
                message.pack(side = TOP, fill = X)

                buttonBox = Frame(self)
                buttonBox.pack(side = TOP)

                for i, buttonMessage in enumerate(self._buttons):
                    command = partial(self._return, i)
                    button = Button(buttonBox, text = buttonMessage, command = command)
                    button.pack(side = LEFT)

            def _return(self, result):
                self.result = result
                self.close()

        return CustomMessagebox(title, message, default, buttons).result


class ScrollFrame(Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        canvas.create_window(0, 0, window=interior, anchor=NW)

        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)   
        canvas.bind('<Enter>', _bind_to_mousewheel)

        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>") 
        canvas.bind('<Leave>', _unbind_from_mousewheel)

        def _on_mousewheel(event):
            if interior.winfo_reqheight() > canvas.winfo_height():
                canvas.yview_scroll(int(-1 * (event.delta / 120)), UNITS)  

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 {} {}".format(*size))
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

class ScrollListbox(Listbox):
    def __init__(self, master, *args, **kw):
        self._container = Frame(master)

        super().__init__(self._container, *args, **kw)
        super().pack(side = LEFT, fill = BOTH, expand = True)
        
        scrollbar = Scrollbar(self._container)
        scrollbar.pack(side = RIGHT, fill = Y)
        scrollbar.config(command = self.yview)
        self.config(yscrollcommand = scrollbar.set)

    def pack(self, cnf = {}, **kw):
        self._container.pack(cnf, **kw)

    def grid(self, cnf = {}, **kw):
        self._container.grid(cnf, **kw)

    def place(self, cnf = {}, **kw):
        self._container.place(cnf, **kw)

class BandedScrollListbox(ScrollListbox):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)

    def insert(self, index, *elements):
        super().insert(index, *elements)
        self._updateBanding()

    def delete(self, first, last = None):
        super().delete(first, last)
        self._updateBanding()

    def _updateBanding(self):
        for i in range(0, self.size()):
            bg = "#f3f3f3" if i % 2 else "white"
            self.itemconfigure(i, bg = bg)

class ScrollTreeview(Treeview):
    def __init__(self, master, *args, **kw):
        self._container = Frame(master)

        super().__init__(self._container, *args, **kw)
        super().pack(side = LEFT, fill = BOTH, expand = True)
        
        scrollbar = Scrollbar(self._container)
        scrollbar.pack(side = RIGHT, fill = Y)
        scrollbar.config(command = self.yview)
        self.config(yscrollcommand = scrollbar.set)

    def pack(self, cnf = {}, **kw):
        self._container.pack(cnf, **kw)

    def grid(self, cnf = {}, **kw):
        self._container.grid(cnf, **kw)

    def place(self, cnf = {}, **kw):
        self._container.place(cnf, **kw)

class AutoCombobox(Combobox):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)

        self._textVariable = None
        if "textvariable" in kw:
            self._textVariable = kw["textvariable"]
            self._observer = kw["textvariable"].trace("w", self._showSuggestions)

        self._masterValues = None
        if "values" in kw:
            self._masterValues = kw["values"]
        
        cb = str(self)
        popdownWindow = self.tk.call("ttk::combobox::PopdownWindow", self)
        popdown = popdownWindow + ".f"

        self.tk.call("bind", popdown, "<<Cut>>", "ttk::entry::Cut " + cb)
        self.tk.call("bind", popdown, "<<Copy>>", "ttk::entry::Copy " + cb)
        self.tk.call("bind", popdown, "<<Paste>>", "ttk::entry::Paste " + cb)
        self.tk.call("bind", popdown, "<<Clear>>", "ttk::entry::Clear " + cb)

        self.tk.call("bind", popdown, "<<PrevChar>>", "ttk::entry::Move " + cb + " prevchar")
        self.tk.call("bind", popdown, "<<NextChar>>", "ttk::entry::Move " + cb + " nextchar")
        self.tk.call("bind", popdown, "<<PrevWord>>", "ttk::entry::Move " + cb + " prevword")
        self.tk.call("bind", popdown, "<<NextWord>>", "ttk::entry::Move " + cb + " nextword")
        self.tk.call("bind", popdown, "<<LineStart>>", "ttk::entry::Move " + cb + " home")
        self.tk.call("bind", popdown, "<<LineEnd>>", "ttk::entry::Move " + cb + " end")

        self.tk.call("bind", popdown, "<<SelectPrevChar>>", "ttk::entry::Extend " + cb + " prevchar")
        self.tk.call("bind", popdown, "<<SelectNextChar>>", "ttk::entry::Extend " + cb + " nextchar")
        self.tk.call("bind", popdown, "<<SelectPrevWord>>", "ttk::entry::Extend " + cb + " prevword")
        self.tk.call("bind", popdown, "<<SelectNextWord>>", "ttk::entry::Extend " + cb + " nextword")
        self.tk.call("bind", popdown, "<<SelectLineStart>>", "ttk::entry::Extend " + cb + " home")
        self.tk.call("bind", popdown, "<<SelectLineEnd>>", "ttk::entry::Extend " + cb + " end")

        self.tk.call("bind", popdown, "<<SelectAll>>", cb + " selection range 0 end")
        self.tk.call("bind", popdown, "<<SelectNone>>", cb + " selection clear")

        self.tk.call("bind", popdown, "<<TraverseIn>>", cb + " selection range 0 end; " + cb + " icursor end")

        self.tk.call("bind", popdown, "<KeyPress>", "ttk::entry::Insert " + cb + " %A")
        self.tk.call("bind", popdown, "<Key-Delete>", "ttk::entry::Delete " + cb)
        self.tk.call("bind", popdown, "<Key-BackSpace>", "ttk::entry::Backspace " + cb)

        self.tk.call("bind", popdown, "<Alt-KeyPress>",	"# nothing")
        self.tk.call("bind", popdown, "<Meta-KeyPress>", "# nothing")
        self.tk.call("bind", popdown, "<Control-KeyPress>",	"# nothing")
        self.tk.call("bind", popdown, "<Key-Escape>", "# nothing")
        self.tk.call("bind", popdown, "<Key-Return>", "# nothing")
        self.tk.call("bind", popdown, "<Key-KP_Enter>", "# nothing")
        self.tk.call("bind", popdown, "<Key-Tab>", "# nothing")    

    def config(self, **kw):
        super().config(**kw)

        if "textvariable" in kw:
            if self._textVariable is not None:
                self._textVariable.trace_vdelete("w", self._observer)
            self._observer = kw["textvariable"].trace("w", self._showSuggestions)
            self._textVariable = kw["textvariable"]

        if "values" in kw:
            self._masterValues = kw["values"]

    def _showSuggestions(self, *args):
        token = self.get()

        if self._masterValues:
            if len(token):
                filteredList = list(filter(lambda value: token.lower() in value.lower(), self._masterValues))
                if len(filteredList):
                    self["values"] = filteredList
                    self.tk.call("ttk::combobox::Post", self)
            if not len(token) or not len(filteredList):
                self["values"] = self._masterValues
                self.tk.call("ttk::combobox::Unpost", self)

class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        self.title("LSPDFR Data Configurator")
        try:
            self.iconbitmap(resource_path("icon.ico"))
        except:
            pass

        toolbar = Frame(self)
        toolbar.pack(side = TOP, fill = X)
        
        importLSPDFRButton = Button(toolbar, text = "Import from LSPDFR", command = self._importLSPDFR)
        importLSPDFRButton.pack(side = LEFT)

        importEUPButton = Button(toolbar, text = "Import from EUPMenu", command = self._importEUP)
        importEUPButton.pack(side = LEFT)

        exportLSPDFRButton = Button(toolbar, text = "Export to LSPDFR", command = self._exportLSPDFR)
        exportLSPDFRButton.pack(side = LEFT)

        exportUBButton = Button(toolbar, text = "Export to UltimateBackup", command = self._exportUB)
        exportUBButton.pack(side = LEFT)

        mainNotebook = Notebook(self, width = 640, height = 480)
        mainNotebook.pack(fill = BOTH, expand = True)

        self._inventoriesTab = InventoriesTab(mainNotebook)
        self._outfitsTab = OutfitsTab(mainNotebook)
        self._agenciesTab = AgenciesTab(mainNotebook)
        self._stationsTab = StationsTab(mainNotebook)
        self._regionsTab = RegionsTab(mainNotebook)
        self._backupsTab = BackupsTab(mainNotebook)

        mainNotebook.add(self._inventoriesTab, text = "Inventories")
        mainNotebook.add(self._outfitsTab, text = "Outfits")
        mainNotebook.add(self._agenciesTab, text = "Agencies")
        mainNotebook.add(self._stationsTab, text = "Stations")
        mainNotebook.add(self._regionsTab, text = "Regions")
        mainNotebook.add(self._backupsTab, text = "Backups")
            
        self.mainloop()

    def _importLSPDFR(self):
        lspdfrConfigFiles = filedialog.askopenfilenames(title = "Select LSPDFR files to import", filetypes = [[".xml files", "*.xml"], ["All files", "*"]])
        if not len(lspdfrConfigFiles):
            return

        for configFile in lspdfrConfigFiles:
            try:
                configRoot = ElementTree.parse(configFile).getroot()

                if configRoot.tag == "Inventories":
                    for inventoryTree in configRoot.findall("Inventory"):
                        name = inventoryTree.find("Name").text
                        scriptName = inventoryTree.find("ScriptName").text

                        stunWeapon = None
                        if len(inventoryTree.findall("StunWeapon")):
                            stunWeapon = getWeaponByID(inventoryTree.findall("StunWeapon")[0].text)

                        armor = 0
                        if len(inventoryTree.findall("Armor")):
                            armor = int(inventoryTree.findall("Armor")[0].text)

                        inventory = Inventory(name, scriptName, stunWeapon, armor)

                        for weaponTree in inventoryTree.findall("Weapon"):
                            chance = 100
                            if weaponTree.get("chance") is not None:
                                chance = int(weaponTree.get("chance"))

                            components = list()
                            if not len(list(weaponTree)):
                                weaponName = getWeaponByID(weaponTree.text)
                            else:
                                weaponName = getWeaponByID(weaponTree.find("Model").text)
                                for component in weaponTree.findall("Component"):
                                    components.append(weaponName.getComponentByID(component.text))
                            
                            inventory.weapons.append(Inventory.Weapon(inventory, weaponName, chance, components))

                        inventories.append(inventory)

                    self._inventoriesTab.updateInventories()

                elif configRoot.tag == "Outfits":
                    for outfitTree in configRoot.findall("Outfit"):
                        name = outfitTree.find("Name").text
                        scriptName = outfitTree.find("ScriptName").text

                        outfit = Outfit(name, scriptName)
                        
                        for variation in outfitTree.find("Variations"):
                            variationName = variation.find("Name").text
                            variationScriptName = variation.find("ScriptName").text if variation.find("ScriptName") is not None else ""
                            base = variation.find("Base").text if variation.find("Base") is not None else ""
                            gender = variation.find("Gender").text

                            components = list()
                            propsToParse = list()
                            if len(variation.findall("Components")):
                                propsToParse = variation.find("Components").findall("Prop")

                                for component in variation.find("Components").findall("Component"):
                                    id = getComponentByID(component.get("id"))
                                    drawable = component.get("drawable")
                                    texture = component.get("texture")

                                    components.append(Outfit.Variation.Component(id, drawable, texture))

                            if len(variation.findall("Props")):
                                propsToParse = propsToParse + variation.find("Props").findall("Prop")
                                
                            props = list()
                            for prop in propsToParse:
                                id = getPropByID(prop.get("id"))
                                drawable = prop.get("drawable")
                                texture = prop.get("texture")

                                props.append(Outfit.Variation.Component(id, drawable, texture))

                            outfit.variations.append(Outfit.Variation(outfit, variationName, variationScriptName, base, gender, components, props))
                        
                        outfits.append(outfit)

                    self._outfitsTab.updateOutfits()

                elif configRoot.tag == "Agencies":
                    for agencyTree in configRoot.findall("Agency"):
                        name = agencyTree.find("Name").text
                        shortName = agencyTree.find("ShortName").text
                        scriptName = agencyTree.find("ScriptName").text

                        if len(agencyTree.findall("Inventory")):
                            inventory = agencyTree.findall("Inventory")[0].text
                        else:
                            inventory = ""

                        if len(agencyTree.findall("Parent")):
                            parent = agencyTree.find("Parent").text
                        else:
                            parent = ""

                        if len(agencyTree.findall("TextureDictionary")):
                            textureDict = agencyTree.find("TextureDictionary").text
                        else:
                            textureDict = ""

                        if len(agencyTree.findall("TextureName")):
                            textureName = agencyTree.find("TextureName").text
                        else:
                            textureName = ""

                        if len(agencyTree.findall("ExcludeFromBackupMenu")):
                            exclude = agencyTree.find("ExcludeFromBackupMenu").text.lower() == "true"
                        else:
                            exclude = False

                        agency = Agency(name, shortName, scriptName, parent, inventory, textureDict, textureName, exclude)

                        for loadoutTree in agencyTree.findall("Loadout"):
                            loadoutName = loadoutTree.find("Name").text
                            
                            chance = 100
                            if loadoutTree.get("chance") is not None:
                                chance = int(loadoutTree.get("chance"))

                            vehicles = list()
                            if len(loadoutTree.findall("Vehicles")):
                                for vehicle in loadoutTree.find("Vehicles").findall("Vehicle"):
                                    vehicleName = vehicle.text

                                    vehicleChance = 100
                                    if vehicle.get("chance") is not None:
                                        vehicleChance = int(vehicle.get("chance"))

                                    livery = 0
                                    if vehicle.get("livery") is not None:
                                        livery = int(vehicle.get("livery"))

                                    weapon = ""
                                    if vehicle.get("weapon") is not None:
                                        weapon = vehicle.get("weapon")

                                    extras = [-1] * 15
                                    for i in range(15):
                                        if vehicle.get("extra_{}".format(i + 1)) is not None:
                                            extras[i] = 1 if vehicle.get("extra_{}".format(i + 1)).lower() == "true" else 0

                                    vehicles.append(Agency.Loadout.Vehicle(vehicleName, vehicleChance, livery, weapon, extras))

                            peds = list()
                            if len(loadoutTree.findall("Peds")):
                                for ped in loadoutTree.find("Peds").findall("Ped"):
                                    pedName = ped.text

                                    pedChance = 100
                                    if ped.get("chance") is not None:
                                        pedChance = int(ped.get("chance"))

                                    outfit = ""
                                    if ped.get("outfit") is not None:
                                        outfit = ped.get("outfit")

                                    pedInventory = ""
                                    if ped.get("inventory") is not None:
                                        pedInventory = ped.get("inventory")

                                    components = list()
                                    for component in COMPONENT_IDS:
                                        if ped.get(component.ID[IDType.LSPDFR_NAME]) is not None:
                                            texture = ped.get(component.ID[IDType.LSPDFR_NAME].replace("comp_", "comp_tex_"))
                                            if texture is None:
                                                texture = "0"

                                            components.append(Outfit.Variation.Component(component, ped.get(component.ID[IDType.LSPDFR_NAME]), texture))

                                    props = list()
                                    for prop in PROP_IDS:
                                        if ped.get(prop.ID[IDType.LSPDFR_NAME]) is not None:
                                            texture = ped.get(prop.ID[IDType.LSPDFR_NAME].replace("prop_", "prop_tex_"))
                                            if texture is None:
                                                texture = "0"

                                            props.append(Outfit.Variation.Component(prop, ped.get(prop.ID[IDType.LSPDFR_NAME]), texture))

                                    randomizeProps = True
                                    if ped.get("randomizeProps") is not None:
                                        randomizeProps = ped.get("randomizeProps").lower() == "true"

                                    peds.append(Agency.Loadout.Ped(pedName, pedChance, outfit, pedInventory, components, props, randomizeProps))

                            numPeds = {"min": 1, "max": 1}
                            if len(loadoutTree.findall("NumPeds")):
                                numPeds["min"] = int(loadoutTree.find("NumPeds").get("min"))
                                numPeds["max"] = int(loadoutTree.find("NumPeds").get("max"))

                            flags = 0
                            if len(loadoutTree.findall("Flags")):
                                for flag in loadoutTree.find("Flags").findall("Flag"):
                                    flags |= Agency.Loadout.Flags.toFlag(flag.text)

                            agency.loadouts.append(Agency.Loadout(agency, loadoutName, chance, vehicles, peds, numPeds, flags))
                        
                        agencies.append(agency)
                    
                    self._agenciesTab.updateAgencies()
                
                elif configRoot.tag == "PoliceStations":
                    for stationTree in configRoot.findall("Station"):
                        name = stationTree.find("Name").text
                        scriptName = stationTree.find("ScriptName").text
                        agency = stationTree.find("Agency").text
                        position = list(map(lambda coord: float(coord.replace("f", "")), stationTree.find("Position").text.split(",")))
                        heading = float(stationTree.find("Heading").text.replace("f", ""))
                        
                        garagePosition = [None] * 4
                        if len(stationTree.findall("GaragePosition")):
                            garagePosition = stationTree.find("GaragePosition").text.split(",")
                            garagePosition = garagePosition[0:-1] + garagePosition[-1].split(";")
                            garagePosition = list(map(lambda coord: float(coord.replace("f", "")), garagePosition))

                        garageSpawnPosition = [None] * 4
                        if len(stationTree.findall("GarageSpawnPosition")):
                            garageSpawnPosition = stationTree.find("GarageSpawnPosition").text.split(",")
                            garageSpawnPosition = garageSpawnPosition[0:-1] + garageSpawnPosition[-1].split(";")
                            garageSpawnPosition = list(map(lambda coord: float(coord.replace("f", "")), garageSpawnPosition))

                        dropOffPosition = [None] * 3
                        if len(stationTree.findall("DropOffPosition")):
                            dropOffPosition = list(map(lambda coord: float(coord.replace("f", "")), stationTree.find("DropOffPosition").text.split(",")))

                        ambientSpawns = list()
                        if len(stationTree.findall("AmbientSpawns")):
                            ambientSpawnsTree = stationTree.find("AmbientSpawns")
                            for spawnPointTree in ambientSpawnsTree.findall("SpawnPoint"):
                                chance = 100
                                if spawnPointTree.get("chance") is not None:
                                    chance = spawnPointTree.get("chance")

                                position = spawnPointTree.get("position")
                                position = list(map(lambda coord: float(coord), position.split(",")))
                                heading = float(spawnPointTree.get("heading"))

                                if len(spawnPointTree):
                                    type = spawnLeaf.tag
                                    spawnLeaf = spawnPointTree[0]
                                    if spawnLeaf.tag == "Ped":
                                        ped = spawnLeaf

                                        pedName = ped.text

                                        pedChance = 100
                                        if ped.get("chance") is not None:
                                            pedChance = int(ped.get("chance"))

                                        outfit = ""
                                        if ped.get("outfit") is not None:
                                            outfit = ped.get("outfit")

                                        pedInventory = ""
                                        if ped.get("inventory") is not None:
                                            pedInventory = ped.get("inventory")

                                        components = list()
                                        for component in COMPONENT_IDS:
                                            if ped.get(component.ID[IDType.LSPDFR_NAME]) is not None:
                                                texture = ped.get(component.ID[IDType.LSPDFR_NAME].replace("comp", "comp_tex"))
                                                if texture is None:
                                                    texture = "0"

                                                components.append(Outfit.Variation.Component(component, ped.get(component.ID[IDType.LSPDFR_NAME]), texture))

                                        props = list()
                                        for prop in PROP_IDS:
                                            if ped.get(prop.ID[IDType.LSPDFR_NAME]) is not None:
                                                texture = ped.get(prop.ID[IDType.LSPDFR_NAME].replace("prop", "prop_tex"))
                                                if texture is None:
                                                    texture = "0"

                                                props.append(Outfit.Variation.Component(prop, ped.get(prop.ID[IDType.LSPDFR_NAME]), texture))

                                        randomizeProps = True
                                        if ped.get("randomizeProps") is not None:
                                            randomizeProps = ped.get("randomizeProps").lower() == "true"

                                        spawn = Agency.Loadout.Ped(pedName, pedChance, outfit, pedInventory, components, props, randomizeProps)
                                    else:
                                        vehicle = spawnLeaf

                                        vehicleName = vehicle.text

                                        vehicleChance = 100
                                        if vehicle.get("chance") is not None:
                                            vehicleChance = int(vehicle.get("chance"))

                                        livery = 0
                                        if vehicle.get("livery") is not None:
                                            livery = int(vehicle.get("livery"))

                                        weapon = ""
                                        if vehicle.get("weapon") is not None:
                                            weapon = vehicle.get("weapon")

                                        extras = [-1] * 15
                                        for i in range(15):
                                            if vehicle.get("extra_{}".format(i + 1)) is not None:
                                                extras[i] = 1 if vehicle.get("extra_{}".format(i + 1)).lower() == "true" else 0

                                        spawn = Agency.Loadout.Vehicle(vehicleName, vehicleChance, livery, weapon, extras)
                                else:
                                    spawn = None
                                    type = spawnPointTree.get("type")

                            ambientSpawns.append(Station.AmbientSpawnPoint(chance, position, heading, type, spawn))
                                
                        stations.append(Station(name, scriptName, agency, position, heading, garagePosition, garageSpawnPosition, dropOffPosition, ambientSpawns))

                    self._stationsTab.updateStations()

                elif configRoot.tag == "Regions":
                    for regionTree in configRoot.findall("Region"):
                        name = regionTree.find("Name").text

                        zones = list()
                        for zone in regionTree.find("Zones").findall("Zone"):
                            zones.append(zone.text)

                        regions.append(Region(name, zones))
                    
                    self._regionsTab.updateRegions()

                elif configRoot.tag == "BackupUnits":
                    for backupType in Backup.Types:
                        type = backupType.name
                        if configRoot.find(backupType.value):
                            for regionTree in configRoot.find(backupType.value):
                                backup = Backup(type, regionTree.tag)
                                for agencyName in regionTree.findall("Agency"):
                                    backup.agencies.append(agencyName.text)
                                
                                backups.append(backup)

                    self._backupsTab.updateBackups()

                else:
                    messagebox.showwarning("Import unsuccessful", "Could not find anything to import in {}".format(basename(configFile)))
                
            except Exception:
                messagebox.showerror("Import unsuccessful", "Failed to import {}, most likely due to a misconfigured file. Until this message is made more helpful, use this traceback:\n\n{}".format(basename(configFile), traceback.format_exc()))

    def _importEUP(self):
        eupOutfitFile = filedialog.askopenfilename(title = "Select an EUPMenu outfit file", filetypes = [[".ini files", "*.ini"], ["All files", "*"]])
        if not eupOutfitFile:
            return
        
        config = configparser.ConfigParser(comment_prefixes = ["//"])
        config.read(eupOutfitFile)

        for outfitName in config.sections():
            scriptName = re.sub(r"\W+", "", outfitName.lower().replace(" ", "_"))
            gender = config[outfitName]["Gender"].lower()

            components = list()
            for id in COMPONENT_IDS:
                name = id.ID[IDType.EUP]

                if name is None:
                    continue
                
                drawable = config[outfitName][name].split(":")[0]
                texture = config[outfitName][name].split(":")[1]
                drawable = int(drawable) - 1
                texture = str(int(texture) - 1)

                if drawable < 1:
                    continue

                components.append(Outfit.Variation.Component(id, str(drawable), texture))
                
            props = list()
            for id in PROP_IDS:
                name = id.ID[IDType.EUP]

                if name is None:
                    continue

                drawable = config[outfitName][name].split(":")[0]
                texture = config[outfitName][name].split(":")[1]

                drawable = int(drawable) - 1
                texture = str(int(texture) - 1)

                if drawable < 0:
                    continue

                props.append(Outfit.Variation.Component(id, str(drawable), texture))

            outfit = Outfit(outfitName, scriptName)
            outfit.variations.append(Outfit.Variation(outfit, outfitName, scriptName, "", gender, components, props))
            outfits.append(outfit)

        self._outfitsTab.updateOutfits()

    def _exportLSPDFR(self):
        exportDir = filedialog.askdirectory(title = "Choose where to export your settings")
        if not exportDir:
            return

        suffix = SuffixMenu(self).suffix
        if not suffix:
            return

        inventoryRoot = ElementTree.Element("Inventories")
        for inventory in inventories:
            inventoryTree = ElementTree.SubElement(inventoryRoot, "Inventory")

            ElementTree.SubElement(inventoryTree, "Name").text = inventory.name
            ElementTree.SubElement(inventoryTree, "ScriptName").text = inventory.getScriptName()

            for weapon in inventory.weapons:
                weaponTree = ElementTree.SubElement(inventoryTree, "Weapon")

                if weapon.chance < 100:
                    weaponTree.set("chance", str(weapon.chance))

                if len(weapon.components):
                    ElementTree.SubElement(weaponTree, "Model").text = weapon.name.NAME

                    for component in weapon.components:
                        ElementTree.SubElement(weaponTree, "Component").text = component.NAME
                else:
                    weaponTree.text = weapon.name.NAME

            if inventory.stunWeapon:
                ElementTree.SubElement(inventoryTree, "StunWeapon").text = inventory.stunWeapon.NAME

            if inventory.armor > 0:
                ElementTree.SubElement(inventoryTree, "Armor").text = str(inventory.armor)

        outfitRoot = ElementTree.Element("Outfits")
        for outfit in outfits:
            outfitTree = ElementTree.SubElement(outfitRoot, "Outfit")

            ElementTree.SubElement(outfitTree, "Name").text = outfit.name
            ElementTree.SubElement(outfitTree, "ScriptName").text = outfit.getScriptName()

            variationsTree = ElementTree.SubElement(outfitTree, "Variations")
            for variation in outfit.variations:
                variationTree = ElementTree.SubElement(variationsTree, "Variation")

                if variation.base:
                    ElementTree.SubElement(variationTree, "Base").text = variation.base

                ElementTree.SubElement(variationTree, "Name").text = variation.name

                if variation.getScriptName():
                    ElementTree.SubElement(variationTree, "ScriptName").text = variation.getScriptName()

                ElementTree.SubElement(variationTree, "Gender").text = variation.gender

                if len(variation.components):
                    componentsTree = ElementTree.SubElement(variationTree, "Components")

                    for component in variation.components:
                        componentLeaf = ElementTree.SubElement(componentsTree, "Component")
                        componentLeaf.set("id", component.id.ID[IDType.LSPDFR])
                        componentLeaf.set("drawable", component.drawable)
                        componentLeaf.set("texture", component.texture)

                if len(variation.props):
                    propsTree = ElementTree.SubElement(variationTree, "Props")

                    for prop in variation.props:
                        propLeaf = ElementTree.SubElement(propsTree, "Prop")
                        propLeaf.set("id", prop.id.ID[IDType.LSPDFR])
                        propLeaf.set("drawable", prop.drawable)
                        propLeaf.set("texture", prop.texture)

        agencyRoot = ElementTree.Element("Agencies")
        dutySelectionRoot = ElementTree.Element("Duty")
        dutySelectionPedsTree = ElementTree.SubElement(dutySelectionRoot, "Peds")
        dutySelectionVehiclesTree = ElementTree.SubElement(dutySelectionRoot, "Vehicles")
        for agency in agencies:
            agencyTree = ElementTree.SubElement(agencyRoot, "Agency")

            ElementTree.SubElement(agencyTree, "Name").text = agency.name
            ElementTree.SubElement(agencyTree, "ShortName").text = agency.shortName
            ElementTree.SubElement(agencyTree, "ScriptName").text = agency.getScriptName()

            ElementTree.SubElement(dutySelectionPedsTree, "Agency").text = agency.getScriptName()
            ElementTree.SubElement(dutySelectionVehiclesTree, "Agency").text = agency.getScriptName()

            if agency.textureDict:
                ElementTree.SubElement(agencyTree, "TextureDictionary").text = agency.textureDict

            if agency.textureName:
                ElementTree.SubElement(agencyTree, "TextureName").text = agency.textureName

            if agency.inventory:
                ElementTree.SubElement(agencyTree, "Inventory").text = agency.inventory

            if agency.parent:
                ElementTree.SubElement(agencyTree, "Parent").text = agency.parent

            for loadout in agency.loadouts:
                loadoutTree = ElementTree.SubElement(agencyTree, "Loadout")
                if loadout.chance < 100:
                    loadoutTree.set("chance", str(loadout.chance))

                ElementTree.SubElement(loadoutTree, "Name").text = loadout.name

                if len(loadout.vehicles):
                    vehiclesTree = ElementTree.SubElement(loadoutTree, "Vehicles")

                    for vehicle in loadout.vehicles:
                        vehicleLeaf = ElementTree.SubElement(vehiclesTree, "Vehicle")
                        vehicleLeaf.text = vehicle.name
                        
                        if vehicle.chance < 100:
                            vehicleLeaf.set("chance", str(vehicle.chance))
                        
                        if vehicle.livery > 0:
                            vehicleLeaf.set("livery", str(vehicle.livery))

                        if vehicle.weapon:
                            vehicleLeaf.set("weapon", vehicle.weapon)

                        for i, extra in enumerate(vehicle.extras):
                            if extra > -1:
                                vehicleLeaf.set("extra_{}".format(i + 1), "true" if extra else "false")
                        
                if len(loadout.peds):
                    pedsTree = ElementTree.SubElement(loadoutTree, "Peds")

                    for ped in loadout.peds:
                        pedLeaf = ElementTree.SubElement(pedsTree, "Ped")
                        pedLeaf.text = ped.name

                        if ped.chance < 100:
                            pedLeaf.set("chance", str(ped.chance))

                        if ped.outfit:
                            pedLeaf.set("outfit", ped.outfit)

                        if ped.inventory:
                            pedLeaf.set("inventory", ped.inventory)

                        for component in ped.components:
                            id = component.id.ID[IDType.LSPDFR_NAME]

                            pedLeaf.set(id, component.drawable)
                            if component.texture != "0":
                                pedLeaf.set(id.replace("comp", "comp_tex"), component.texture)

                        for prop in ped.props:
                            id = prop.id.ID[IDType.LSPDFR_NAME]

                            pedLeaf.set(id, prop.drawable)
                            if prop.texture != "0":
                                pedLeaf.set(id.replace("prop", "prop_tex"), prop.texture)

                        if not ped.randomizeProps:
                            pedLeaf.set("randomizeProps", "false")

                if loadout.numPeds["max"] > 1:
                    numPedsLeaf = ElementTree.SubElement(loadoutTree, "NumPeds")
                    numPedsLeaf.set("min", str(loadout.numPeds["min"]))
                    numPedsLeaf.set("max", str(loadout.numPeds["max"]))

                if loadout.hasFlags():
                    flagsTree = ElementTree.SubElement(loadoutTree, "Flags")

                    for flag in Agency.Loadout.Flags:
                        if loadout.checkFlag(flag):
                            ElementTree.SubElement(flagsTree, "Flag").text = str(flag)
                
            if agency.exclude:
                ElementTree.SubElement(agencyTree, "ExcludeFromBackupMenu").text = str(agency.exclude)

        stationRoot = ElementTree.Element("PoliceStations")
        for station in stations:
            stationTree = ElementTree.SubElement(stationRoot, "Station")
            
            ElementTree.SubElement(stationTree, "Name").text = station.name
            ElementTree.SubElement(stationTree, "Agency").text = station.agency
            ElementTree.SubElement(stationTree, "ScriptName").text = station.scriptName
            ElementTree.SubElement(stationTree, "Position").text = "{}f, {}f, {}f".format(*station.position)
            ElementTree.SubElement(stationTree, "Heading").text = "{}f".format(station.heading)
            
            if station.garagePosition[0] is not None:
                ElementTree.SubElement(stationTree, "GaragePosition").text = "{}f, {}f, {}f; {}f".format(*station.garagePosition)

            if station.garageSpawnPosition[0] is not None:
                ElementTree.SubElement(stationTree, "GaragePosition").text = "{}f, {}f, {}f; {}f".format(*station.garageSpawnPosition)

            if station.dropOffPosition[0] is not None:
                ElementTree.SubElement(stationTree, "DropOffPosition").text = "{}f, {}f, {}f".format(*station.dropOffPosition)

            if len(station.ambientSpawns):
                ambientSpawnsTree = ElementTree.SubElement(stationTree, "AmbientSpawns")
                for spawnPoint in station.ambientSpawns:
                    spawnPointTree = ElementTree.SubElement(ambientSpawnsTree, "SpawnPoint")
                    if spawnPoint.chance < 100:
                        spawnPointTree.set("chance", str(spawnPoint.chance))
                    spawnPointTree.set("position", ", ".join(list(map(lambda coord: str(coord), spawnPoint.position))))
                    spawnPointTree.set("heading", str(spawnPoint.heading))

                    if spawnPoint.spawn is None:
                        spawnPointTree.set("type", spawnPoint.type)
                    elif spawnPoint.type == "Ped":
                        ped = spawnPoint.spawn

                        pedLeaf = ElementTree.SubElement(spawnPointTree, "Ped")
                        pedLeaf.text = ped.name

                        if ped.chance < 100:
                            pedLeaf.set("chance", str(ped.chance))

                        if ped.outfit:
                            pedLeaf.set("outfit", ped.outfit)

                        if ped.inventory:
                            pedLeaf.set("inventory", ped.inventory)

                        for component in ped.components:
                            id = component.id.ID[IDType.LSPDFR_NAME]

                            pedLeaf.set(id, component.drawable)
                            if component.texture != "0":
                                pedLeaf.set(id.replace("comp_", "comp_tex_"), component.texture)

                        for prop in ped.props:
                            id = prop.id.ID[IDType.LSPDFR_NAME]

                            pedLeaf.set(id, prop.drawable)
                            if prop.texture != "0":
                                pedLeaf.set(id.replace("prop_", "prop_tex_"), prop.texture)

                        if not ped.randomizeProps:
                            pedLeaf.set("randomizeProps", "false")
                    else:
                        vehicle = spawnPoint.spawn

                        vehicleLeaf = ElementTree.SubElement(vehiclesTree, "Vehicle")
                        vehicleLeaf.text = vehicle.name
                        
                        if vehicle.chance < 100:
                            vehicleLeaf.set("chance", str(vehicle.chance))
                        
                        if vehicle.livery > 0:
                            vehicleLeaf.set("livery", str(vehicle.livery))

                        if vehicle.weapon:
                            vehicleLeaf.set("weapon", vehicle.weapon)

                        for i, extra in enumerate(vehicle.extras):
                            if extra > -1:
                                vehicleLeaf.set("extra_{}".format(i + 1), "true" if extra else "false")

        regionRoot = ElementTree.Element("Regions")
        for region in regions:
            if region.getName() == "HIGHWAY":
                continue

            regionTree = ElementTree.SubElement(regionRoot, "Region")

            ElementTree.SubElement(regionTree, "Name").text = region.getName()

            zonesTree = ElementTree.SubElement(regionTree, "Zones")
            for zone in region.zones:
                ElementTree.SubElement(zonesTree, "Zone").text = zone

        backupRoot = ElementTree.Element("BackupUnits")
        for backupType in Backup.Types:
            if len(getBackupsByType(backupType)):
                backupTree = ElementTree.SubElement(backupRoot, backupType.value)
                for backup in getBackupsByType(backupType):
                    regionTree = ElementTree.SubElement(backupTree, backup.region)
                    for agency in backup.agencies:
                        ElementTree.SubElement(regionTree, "Agency").text = agency

        generatedComment = "<!-- Generated by LSPDFR Data Configurator version {} -->\n".format(VERSION)

        with open(exportDir + "/inventory_{}.xml".format(suffix), "w") as f:
            f.write(minidom.parseString(ElementTree.tostring(inventoryRoot, "utf-8")).toprettyxml())
            f.write(generatedComment)

        with open(exportDir + "/outfits_{}.xml".format(suffix), "w") as f:
            f.write(minidom.parseString(ElementTree.tostring(outfitRoot, "utf-8")).toprettyxml())
            f.write(generatedComment)

        with open(exportDir + "/agency_{}.xml".format(suffix), "w") as f:
            f.write(minidom.parseString(ElementTree.tostring(agencyRoot, "utf-8")).toprettyxml())
            f.write(generatedComment)

        with open(exportDir + "/stations_{}.xml".format(suffix), "w") as f:
            f.write(minidom.parseString(ElementTree.tostring(stationRoot, "utf-8")).toprettyxml())
            f.write(generatedComment)

        with open(exportDir + "/regions_{}.xml".format(suffix), "w") as f:
            f.write(minidom.parseString(ElementTree.tostring(regionRoot, "utf-8")).toprettyxml())
            f.write(generatedComment)

        with open(exportDir + "/backup_{}.xml".format(suffix), "w") as f:
            f.write(minidom.parseString(ElementTree.tostring(backupRoot, "utf-8")).toprettyxml())
            f.write(generatedComment)

        with open(exportDir + "/duty_selection_{}.xml".format(suffix), "w") as f:
            f.write(minidom.parseString(ElementTree.tostring(dutySelectionRoot, "utf-8")).toprettyxml())
            f.write(generatedComment)

    def _exportUB(self):
        exportDir = filedialog.askdirectory(title = "Choose where to export your settings")
        if not exportDir:
            return

        ultimateBackupRoot = ElementTree.Element("UltimateBackup")
        policeTransportTree = ElementTree.SubElement(ultimateBackupRoot, "PoliceTransport")
        for backupType in Backup.Types:
            if len(getBackupsByType(backupType)):
                ultimateBackupTree = ElementTree.SubElement(ultimateBackupRoot, backupType.value)
                for backup in getBackupsByType(backupType):
                    if backup.region == "HIGHWAY":
                        continue

                    region = getRegionByName(backup.region)
                    customRegionTree = ElementTree.SubElement(ultimateBackupTree, "CustomRegion")
                    customRegionTree.set("label", region.getName())

                    zonesTree = ElementTree.SubElement(customRegionTree, "Zones")
                    for zone in region.zones:
                        ElementTree.SubElement(zonesTree, "Zone").text = zone

                    for agency in backup.agencies:
                        agency = getAgencyByScriptName(agency)
                        for loadout in agency.loadouts:
                            if not loadout.checkFlag(Agency.Loadout.Flags.RESPONDS_AS_BACKUP) and not loadout.checkFlag(Agency.Loadout.Flags.RESPONDS_AS_TRANSPORT):
                                continue

                            vehicleSetTree = ElementTree.Element("VehicleSet")

                            if loadout.checkFlag(Agency.Loadout.Flags.RESPONDS_AS_BACKUP):
                                customRegionTree.append(vehicleSetTree)

                            if loadout.checkFlag(Agency.Loadout.Flags.RESPONDS_AS_TRANSPORT):
                                transportCustomRegionTree = policeTransportTree.find("CustomRegion[@label='{}']".format(region.getName()))
                                if transportCustomRegionTree is None:
                                    transportCustomRegionTree = ElementTree.SubElement(policeTransportTree, "CustomRegion")
                                    transportCustomRegionTree.set("label", region.getName())

                                    transportZonesTree = ElementTree.SubElement(transportCustomRegionTree, "Zones")
                                    for zone in region.zones:
                                        ElementTree.SubElement(transportZonesTree, "Zone").text = zone

                                transportCustomRegionTree.append(vehicleSetTree)

                            pax = str(loadout.numPeds["max"] - 1)
                            pax_chance = str(int(loadout.numPeds["min"] / loadout.numPeds["max"] * 100))

                            vehiclesTree = ElementTree.SubElement(vehicleSetTree, "Vehicles")
                            for vehicle in loadout.vehicles:
                                if vehicle.chance == 0:
                                    continue

                                vehicleLeaf = ElementTree.SubElement(vehiclesTree, "Vehicle")
                                vehicleLeaf.text = vehicle.name
                                
                                if vehicle.chance < 100 or len(loadout.vehicles) > 1:
                                    vehicleLeaf.set("chance", str(vehicle.chance))

                                if vehicle.livery > 0:
                                    vehicleLeaf.set("livery", str(vehicle.livery))

                                for i, extra in enumerate(vehicle.extras):
                                    if extra > -1:
                                        vehicleLeaf.set("extra_{}".format(i + 1), "true" if extra else "false")

                                if int(pax) > 0:
                                    vehicleLeaf.set("pax", pax)
                                    vehicleLeaf.set("pax_chance", pax_chance)

                            pedsTree = ElementTree.SubElement(vehicleSetTree, "Peds")
                            for ped in loadout.peds:
                                if ped.chance == 0:
                                    continue

                                pedLeaf = ElementTree.SubElement(pedsTree, "Ped")
                                pedLeaf.text = ped.name

                                if ped.chance < 100 or len(loadout.peds) > 1:
                                    pedLeaf.set("chance", str(ped.chance))

                                if not ped.randomizeProps:
                                    pedLeaf.set("random_props", "false")

                                if ped.outfit:
                                    for attr, value in getOutfitUBSettings(ped.outfit, ped.name.lower() == "mp_m_freemode_01").items():
                                        pedLeaf.set(attr, value)

                                for component in ped.components:
                                    id = component.id.ID[IDType.UB]
                                    drawable = str(int(list(map(lambda drawable: drawable.split("-")[0], component.drawable.split(",")))[0]) + 1)
                                    texture = int(list(map(lambda texture: texture.split("-")[0], component.texture.split(",")))[0]) + 1

                                    pedLeaf.set(id, drawable)
                                    if component.texture != "0":
                                        pedLeaf.set(id.replace("comp_", "tex_"), texture)

                                for prop in ped.props:
                                    id = prop.id.ID[IDType.UB]
                                    drawable = str(int(list(map(lambda drawable: drawable.split("-")[0], prop.drawable.split(",")))[0]) + 1)
                                    texture = int(list(map(lambda texture: texture.split("-")[0], prop.texture.split(",")))[0]) + 1

                                    pedLeaf.set(id, drawable)
                                    if prop.texture != "0":
                                        pedLeaf.set(id.replace("prop_", "tex_"), texture)

                            if agency.inventory:
                                inventory = getInventoryByScriptName(agency.inventory)
                                if inventory.stunWeapon:
                                    ElementTree.SubElement(ElementTree.SubElement(vehicleSetTree, "NonLethals"), "NonLethal").text = inventory.stunWeapon.NAME

                                if len(inventory.weapons):
                                    handGunsTree = ElementTree.SubElement(vehicleSetTree, "HandGuns")
                                    longGunsTree = ElementTree.SubElement(vehicleSetTree, "LongGuns")
                                    for weapon in inventory.weapons:
                                        if weapon.name.TYPE == WeaponType.HAND_GUN:
                                            weaponLeaf = ElementTree.SubElement(handGunsTree, "HandGun")
                                        else:
                                            weaponLeaf = ElementTree.SubElement(longGunsTree, "LongGun")
                                        weaponLeaf.text = weapon.name.NAME

                                        for i, component in enumerate(weapon.components):
                                            weaponLeaf.set("comp_{}".format(i + 1), component.NAME)

        generatedComment = "<!-- Generated by LSPDFR Data Configurator version {} -->\n".format(VERSION)

        with open(exportDir + "/CustomRegions.xml", "w") as f:
            f.write(minidom.parseString(ElementTree.tostring(ultimateBackupRoot, "utf-8")).toprettyxml())
            f.write(generatedComment)

class SuffixMenu(Dialog):
    def __init__(self, master):
        self.suffix = None

        super().__init__(master, "Choose a suffix")

    def _build(self):
        Button(self, text = "OK", command = self._save).pack(side = BOTTOM, anchor = E)

        Label(self, text = "Suffix: <file>_").pack(side = LEFT)
        self._suffixEntry = Entry(self)
        self._suffixEntry.pack(side = LEFT)
        Label(self, text = ".xml").pack(side = LEFT)

    def _save(self):
        self.suffix = self._suffixEntry.get()
        self.close()


class InventoriesTab(Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)

        listFrame = LabelFrame(self, text = "Inventories")
        listFrame.pack(side = LEFT, fill = BOTH, expand = True)
        buttonFrame = Frame(self)
        buttonFrame.pack(side = LEFT, fill = Y)

        self._listbox = listbox = BandedScrollListbox(listFrame, selectmode = EXTENDED)
        listbox.pack(side = LEFT, fill = BOTH, expand = True)
        
        addButton = Button(buttonFrame, text = "Add", command = self._addInventory)
        addButton.pack(fill = X)
        editButton = Button(buttonFrame, text = "Edit", command = self._editInventory)
        editButton.pack(fill = X)
        copyButton = Button(buttonFrame, text = "Duplicate", command = self._copyInventory)
        copyButton.pack(fill = X)
        deleteButton = Button(buttonFrame, text = "Delete", command = self._deleteInventory)
        deleteButton.pack(fill = X)

        listbox.bind("<Double-Button-1>", self._editInventory)
        listbox.bind("<Delete>", self._deleteInventory)

    def updateInventories(self):
        self._listbox.delete(0, END)
        for inventory in inventories:
            self._listbox.insert(END, "{} ({})".format(inventory.name, inventory.getScriptName()))

    def _addInventory(self):
        if EditinventoryBox(self).update:
            self.updateInventories()
            self._listbox.see(END)

    def _editInventory(self, event = None):
        if len(self._listbox.curselection()):
            i = self._listbox.curselection()[0]
            if EditinventoryBox(self, i).update:
                self.updateInventories()
                self._listbox.see(min(i, self._listbox.size() - 1))

    def _deleteInventory(self, event = None):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                inventories[i].delete()
            self.updateInventories()
            self._listbox.see(min(i, self._listbox.size() - 1))

    def _copyInventory(self):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                inventory = copy.deepcopy(inventories[i])
                ii = 1
                scriptName = inventory.getScriptName() + "_copy{}".format(ii)
                while getInventoryByScriptName(scriptName):
                    ii += 1
                    scriptName = inventory.getScriptName() + "_copy{}".format(ii)
                inventory.setScriptName(scriptName, False)
                inventories.insert(i + 1, inventory)
            self.updateInventories()
            self._listbox.see(min(i, self._listbox.size() - 1))

class EditinventoryBox(Dialog):
    def __init__(self, master, inventoryIndex = None):
        self._inventoryIndex = inventoryIndex
        if inventoryIndex is not None:
            self._inventory = copy.deepcopy(inventories[inventoryIndex])
        else:
            self._inventory = Inventory()
            self._inventoryIndex = len(inventories)

        self.update = False

        super().__init__(master, "Edit inventory")

    def _build(self):
        optionFrame = Frame(self)
        optionFrame.pack(side = TOP, fill = X)
        saveButton = Button(self, text = "Save", command = self._saveInventory)
        saveButton.pack(side = BOTTOM, fill = X)
        addButton = Button(self, text = "Add weapon", command = self._addWeapon)
        addButton.pack(side = BOTTOM, fill = X)
        weaponContainer = LabelFrame(self, text = "Weapons")
        weaponContainer.pack(side = LEFT, fill = BOTH, expand = True)

        nameLabel = Label(optionFrame, text = "Name:")
        nameLabel.grid(row = 0, column = 0, sticky = W)
        self._nameEntry = nameEntry = Entry(optionFrame)
        nameEntry.grid(row = 1, column = 0, sticky = W)

        scriptNameLabel = Label(optionFrame, text = "Script name:")
        scriptNameLabel.grid(row = 0, column = 1, sticky = W)
        self._scriptNameEntry = scriptNameEntry = Entry(optionFrame)
        scriptNameEntry.grid(row = 1, column = 1, sticky = W)

        stunWeaponLabel = Label(optionFrame, text = "Stun weapon:")
        stunWeaponLabel.grid(row = 0, column = 2, sticky = W)
        self._stunWeaponName = StringVar(optionFrame)
        stunWeaponBox = AutoCombobox(optionFrame, textvariable = self._stunWeaponName, values = getWeaponDescs())
        stunWeaponBox.grid(row = 1, column = 2, sticky = W)

        armorLabel = Label(optionFrame, text = "Armor:")
        armorLabel.grid(row = 0, column = 3, sticky = W)
        self._armorBox = Spinbox(optionFrame, from_ = 0, to = 100)
        self._armorBox.grid(row = 1, column = 3, sticky = W)

        weaponScrollFrame = ScrollFrame(weaponContainer)
        weaponScrollFrame.pack(side = LEFT, fill = BOTH, expand = True)
        self._weaponFrame = weaponScrollFrame.interior 

        self._nameEntry.insert(0, self._inventory.name)
        self._scriptNameEntry.insert(0, self._inventory.getScriptName())
        if self._inventory.stunWeapon:
            self._stunWeaponName.set(self._inventory.stunWeapon.DESC)
        self._armorBox.insert(0, self._inventory.armor)

        if len(self._inventory.weapons):
            self._updateWeapons()

    def _saveWeapon(self, index, weaponName, weaponChance, *args):
        weapon = self._inventory.weapons[index]

        weaponName = getWeaponByDesc(weaponName.get())
        if weapon.name != weaponName:
            weapon.name = weaponName
            weapon.components.clear()
            self._updateWeapons()

        try:
            weapon.chance = max(0, min(100, int(weaponChance.get())))
        except ValueError:
            pass

    def _saveInventory(self):
        name = self._nameEntry.get()
        scriptName = self._scriptNameEntry.get()
        stunWeapon = getWeaponByDesc(self._stunWeaponName.get())

        armor = self._armorBox.get()

        if not name or not scriptName or not armor:
            messagebox.showerror(title = "Save unsuccessful", message = "Name, script name, and armor are required")
            return

        if not re.match(r"^[A-Za-z0-9_-]*$", scriptName):
            messagebox.showerror("Save unsuccessful", "Script name must contain only letters, numbers, underscores, and dashes")
            return

        if not armor.isdigit():
            messagebox.showerror(title = "Save unsuccessful", message = "Armor must be an integer between 0 and 100")
            return

        existingInventory = getInventoryByScriptName(scriptName)
        if self._inventory.getScriptName() != scriptName and existingInventory:
            if messagebox.askyesno(title = "Overwrite?", message = "An inventory with the script name {} already exists, overwrite?".format(scriptName)):
                if self._inventoryIndex < len(inventories):
                    inventories[self._inventoryIndex].delete()
                self._inventoryIndex = inventories.index(getInventoryByScriptName(scriptName))
            else:
                return

        self._inventory.name = name
        self._inventory.setScriptName(scriptName)
        self._inventory.stunWeapon = stunWeapon
        self._inventory.armor = max(0, min(100, int(armor)))

        if self._inventoryIndex < len(inventories):
            inventories[self._inventoryIndex].delete(False)
        inventories.insert(self._inventoryIndex, self._inventory)

        self.update = True
        self.close()

    def _updateWeapons(self):
        for widget in self._weaponFrame.children.values():
            widget.grid_forget()

        if len(self._inventory.weapons):
            weaponColLabel = Label(self._weaponFrame, text = "Weapon")
            weaponColLabel.grid(row = 0, column = 0)
            chanceColLabel = Label(self._weaponFrame, text = "Chance")
            chanceColLabel.grid(row = 0, column = 1)

        for i, weapon in enumerate(self._inventory.weapons):
            weaponName = StringVar(self._weaponFrame, weapon.name.DESC)
            weaponBox = AutoCombobox(self._weaponFrame, textvariable = weaponName, values = getWeaponDescs())
            weaponBox.grid(row = i + 1, column = 0, sticky = W)
           
            weaponChance = StringVar(self._weaponFrame, str(weapon.chance))
            chanceEntry = Entry(self._weaponFrame, textvariable = weaponChance)
            chanceEntry.grid(row = i + 1, column = 1)

            trace = partial(self._saveWeapon, i, weaponName, weaponChance)
            weaponName.trace("w", trace)
            weaponChance.trace("w", trace)

            command = partial(self._editComponents, i)
            componentsButton = Button(self._weaponFrame, text = "Components", command = command)
            componentsButton.grid(row = i + 1, column = 2)
            if not len(weapon.name.COMPONENTS):
                componentsButton.config(state = DISABLED)

            command = partial(self._deleteWeapon, i)
            deleteButton = Button(self._weaponFrame, text = "Delete", command = command)
            deleteButton.grid(row = i + 1, column = 4)

    def _addWeapon(self):
        self._inventory.weapons.append(Inventory.Weapon(self._inventory))
        self._updateWeapons()

    def _deleteWeapon(self, index):
        del self._inventory.weapons[index]
        self._updateWeapons()

    def _editComponents(self, index):
        EditComponentsMenu(self, self._inventory.weapons[index])

class EditComponentsMenu(Dialog):
    def __init__(self, master, weapon):
        self._weapon = weapon

        super().__init__(master, "Edit components")

    def _build(self):
        addFrame = Frame(self)
        addFrame.pack()

        self._newComponent = StringVar(addFrame, self._weapon.name.getComponentDescs()[0])
        newComponentMenu = OptionMenu(addFrame, self._newComponent, self._weapon.name.getComponentDescs()[0], *self._weapon.name.getComponentDescs())
        newComponentMenu.pack(side = LEFT)

        addButton = Button(addFrame, text = "Add", command = self._addComponent)
        addButton.pack(side = LEFT)

        listFrame = LabelFrame(self, text = "Components")
        listFrame.pack(fill = BOTH, expand = True)

        self._listbox = BandedScrollListbox(listFrame, selectmode = EXTENDED)
        self._listbox.pack(side = LEFT, fill = BOTH, expand = True)

        deleteButton = Button(self, text = "Delete", command = self._deleteComponent)
        deleteButton.pack(fill = X)

        saveButton = Button(self, text = "Save", command = self._saveWeapon)
        saveButton.pack(fill = X)

        for component in self._weapon.components:
            self._listbox.insert(END, component.DESC)

        self._listbox.bind("<Delete>", self._deleteComponent)

    def _addComponent(self):
        i = self._weapon.name.getComponentDescs().index(self._newComponent.get())
        self._listbox.insert(END, self._weapon.name.COMPONENTS[i].DESC)

    def _deleteComponent(self, event = None):
        for i in sorted(self._listbox.curselection(), reverse = True):
            self._listbox.delete(i)
    
    def _saveWeapon(self):
        components = list()

        for component in self._listbox.get(0, END):
            component = self._weapon.name.getComponentByDesc(component)

            if component is None:
                messagebox.showerror(title = "Save unsuccessful", message = "{} is not a valid component for this weapon".format(component.DESC))
                return

            if component in components:
                messagebox.showerror(title = "Save unsuccessful", message = "There can not be more than one {}".format(component.DESC))
                return

            components.append(component)

        self._weapon.components = components
        self.close()

class OutfitsTab(Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)

        listFrame = LabelFrame(self, text = "Outfits")
        listFrame.pack(side = LEFT, fill = BOTH, expand = True)
        buttonFrame = Frame(self)
        buttonFrame.pack(side = LEFT, fill = Y)

        self._listbox = listbox = BandedScrollListbox(listFrame, selectmode = EXTENDED)
        listbox.pack(side = LEFT, fill = BOTH, expand = True)

        addButton = Button(buttonFrame, text = "Add", command = self._addOutfit)
        editButton = Button(buttonFrame, text = "Edit", command = self._editOutfit)
        copyButton = Button(buttonFrame, text = "Duplicate", command = self._copyOutfit)
        combineButton = Button(buttonFrame, text = "Combine as variations", command = self._combineOutfits)
        deleteButton = Button(buttonFrame, text = "Delete", command = self._deleteOutfit)
        addButton.pack(fill = X)
        editButton.pack(fill = X)
        copyButton.pack(fill = X)
        combineButton.pack(fill = X)
        deleteButton.pack(fill = X)

        listbox.bind("<Double-Button-1>", self._editOutfit)
        listbox.bind("<Delete>", self._deleteOutfit)

    def updateOutfits(self):
        self._listbox.delete(0, END)
        for outfit in outfits:
            self._listbox.insert(END, "{} ({})".format(outfit.name, outfit.getScriptName()))

    def _addOutfit(self):
        if EditOutfitMenu(self).update:
            self.updateOutfits()
            self._listbox.see(END)

    def _editOutfit(self, event = None):
        if len(self._listbox.curselection()):
            index = self._listbox.curselection()[0]
            if EditOutfitMenu(self, index).update:
                self.updateOutfits()
                self._listbox.see(min(index, self._listbox.size() - 1))

    def _copyOutfit(self):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                outfit = copy.deepcopy(outfits[i])
                ii = 1
                scriptName = outfit.getScriptName() + "_copy{}".format(ii)
                while getOutfitByScriptName(scriptName):
                    ii += 1
                    scriptName = outfit.getScriptName() + "_copy{}".format(ii)
                outfit.setScriptName(scriptName, False)
                outfits.insert(i + 1, outfit)
            
            self.updateOutfits()
            self._listbox.see(min(i, self._listbox.size() - 1))

    def _combineOutfits(self):
        if len(self._listbox.curselection()) > 1:
            for i in sorted(self._listbox.curselection()[1:], reverse = True):
                outfits[self._listbox.curselection()[0]].combineVariations(outfits[i])
                outfits[i].delete()
            self.updateOutfits()
            self._listbox.see(min(i, self._listbox.size() - 1))

    def _deleteOutfit(self, event = None):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                outfits[i].delete()
            self.updateOutfits()
            self._listbox.see(min(i, self._listbox.size() - 1))

class EditOutfitMenu(Dialog):
    def __init__(self, master, outfitIndex = None):
        self._outfitIndex = outfitIndex
        if outfitIndex is not None:
            self._outfit = copy.deepcopy(outfits[outfitIndex])
        else:
            self._outfit = Outfit()
            self._outfitIndex = len(outfits)

        self.update = False

        super().__init__(master, "Edit outfit")

    def _build(self):
        optionFrame = Frame(self)
        optionFrame.pack(side = TOP, fill = X)
        saveButton = Button(self, text = "Save", command = self._saveOutfit)
        saveButton.pack(side = BOTTOM, fill = X)

        listFrame = LabelFrame(self, text = "Variations")
        listFrame.pack(side = LEFT, fill = BOTH, expand = True)
        buttonFrame = Frame(self)
        buttonFrame.pack(side = LEFT, fill = Y)

        nameLabel = Label(optionFrame, text = "Name: ")
        nameLabel.pack(side = LEFT)
        self._nameEntry = Entry(optionFrame)
        self._nameEntry.pack(side = LEFT)
        scriptNameLabel = Label(optionFrame, text = "Script name: ")
        scriptNameLabel.pack(side = LEFT)
        self._scriptNameEntry = Entry(optionFrame)
        self._scriptNameEntry.pack(side = LEFT)
       
        self._listbox = listbox = BandedScrollListbox(listFrame, selectmode = EXTENDED)
        listbox.pack(side = LEFT, fill = BOTH, expand = True)

        self._nameEntry.insert(0, self._outfit.name)
        self._scriptNameEntry.insert(0, self._outfit.getScriptName())
        self._updateVariations()

        addButton = Button(buttonFrame, text = "Add", command = self._addVariation)
        editButton = Button(buttonFrame, text = "Edit", command = self._editVariation)
        copyButton = Button(buttonFrame, text = "Duplicate", command = self._copyVariation)
        deleteButton = Button(buttonFrame, text = "Delete", command = self._deleteVariation)
        
        addButton.pack(fill = X)
        editButton.pack(fill = X)
        copyButton.pack(fill = X)
        deleteButton.pack(fill = X)

        listbox.bind("<Double-Button-1>", self._editVariation)
        listbox.bind("<Delete>", self._deleteVariation)

    def _updateVariations(self):
        self._listbox.delete(0, END)
        for variation in self._outfit.variations:
            if variation.getScriptName():
                self._listbox.insert(END, "{} ({})".format(variation.name, variation.getScriptName()))
            else:
                self._listbox.insert(END, variation.name)

    def _addVariation(self):
        if EditVariationMenu(self).update:
            self._updateVariations()

    def _editVariation(self, event = None):
        if len(self._listbox.curselection()):
            if EditVariationMenu(self, self._listbox.curselection()[0]).update:
                self._updateVariations()

    def _copyVariation(self):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                variation = copy.deepcopy(self._outfit.variations[i])
                variation.outfit = self._outfit
                ii = 1
                scriptName = variation.getScriptName() + "_copy{}".format(ii)
                while variation.outfit.getVariationByScriptName(scriptName):
                    ii += 1
                    scriptName = variation.getScriptName() + "_copy{}".format(ii)
                variation.setScriptName(scriptName, False)
                variation.outfit.variations.insert(i + 1, variation)
            self._updateVariations()

    def _deleteVariation(self, event = None):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                self._outfit.variations[i].delete()
            self._updateVariations()

    def _saveOutfit(self):
        name = self._nameEntry.get()
        scriptName = self._scriptNameEntry.get()

        if not (name and scriptName):
            messagebox.showerror(title = "Save unsuccessful", message = "Name and script name are required")
            return

        if not re.match(r"^[A-Za-z0-9_-]*$", scriptName):
            messagebox.showerror("Save unsuccessful", "Script name must contain only letters, numbers, underscores, and dashes")
            return

        existingOutfit = getOutfitByScriptName(scriptName)
        if self._outfit.getScriptName() != scriptName and existingOutfit:
            result = Dialog.askcustom(title = "Overwrite?", message = "An outfit with the script name {} already exists, overwrite?".format(scriptName), buttons = ["Yes", "No", "Combine as variations"])
            if result == 2:
                self._outfit.combineVariations(existingOutfit)
            if result == 0 or result == 2:
                if self._outfitIndex < len(outfits):
                    outfits[self._outfitIndex].delete()
                self._outfitIndex = outfits.index(getOutfitByScriptName(scriptName))
            else:
                return

        self._outfit.name = name
        self._outfit.setScriptName(scriptName)

        if self._outfitIndex < len(outfits):
            outfits[self._outfitIndex].delete(False)
        outfits.insert(self._outfitIndex, self._outfit)

        self.update = True
        self.close()

class EditVariationMenu(Dialog):
    def __init__(self, master, variationIndex = None):
        self._variationIndex = variationIndex
        if variationIndex is not None:
            self._variation = copy.deepcopy(master._outfit.variations[variationIndex])
            self._variation.outfit = master._outfit
        else:
            self._variation = Outfit.Variation(master._outfit)
            self._variationIndex = len(master._outfit.variations)

        self.update = False

        super().__init__(master, "Edit variation")

    def _build(self):
        nameLabel = Label(self, text = "Name:")
        self._nameEntry = Entry(self)
        nameLabel.grid(row = 0, column = 0, sticky = W)
        self._nameEntry.grid(row = 1, column = 0, sticky = W)

        scriptNameLabel = Label(self, text = "Script name:")
        self._scriptNameEntry = Entry(self)
        scriptNameLabel.grid(row = 0, column = 1, sticky = W)
        self._scriptNameEntry.grid(row = 1, column = 1, sticky = W)

        self._baseName = StringVar(self)
        baseLabel = Label(self, text = "Base:")
        baseBox = AutoCombobox(self, textvariable = self._baseName, values = self._variation.outfit.getVariationScriptNames())
        baseLabel.grid(row = 0, column = 2, sticky = W)
        baseBox.grid(row = 1, column = 2, sticky = W)

        self._gender = StringVar(self)
        self._gender.set("male")
        genderLabel = Label(self, text = "Gender:")
        genderMenu = OptionMenu(self, self._gender, "male", "male", "female")
        genderLabel.grid(row = 0, column = 3, sticky = W)
        genderMenu.grid(row = 1, column = 3, sticky = W)

        componentFrame = LabelFrame(self, text = "Components")
        componentFrame.grid(row = 2, column = 0, columnspan = 4, sticky = N + E + S + W)
        componentHeaderID = Label(componentFrame, text = "Component")
        componentHeaderDrawable = Label(componentFrame, text = "Drawable")
        componentHeaderTexture = Label(componentFrame, text = "Texture")
        componentHeaderID.grid(row = 0, column = 0)
        componentHeaderDrawable.grid(row = 0, column = 1)
        componentHeaderTexture.grid(row = 0, column = 2)

        propFrame = LabelFrame(self, text = "Props")
        propFrame.grid(row = 3, column = 0, columnspan = 4, sticky = N + E + S + W)
        propHeaderID = Label(propFrame, text = "Prop")
        propHeaderDrawable = Label(propFrame, text = "Drawable")
        propHeaderTexture = Label(propFrame, text = "Texture")
        propHeaderID.grid(row = 0, column = 0)
        propHeaderDrawable.grid(row = 0, column = 1)
        propHeaderTexture.grid(row = 0, column = 2)

        self._componentFields = {}
        for i, id in enumerate(COMPONENT_IDS):
            componentLabel = Label(componentFrame, text = id.DESC)
            drawableEntry = Entry(componentFrame)
            textureEntry = Entry(componentFrame)
            componentLabel.grid(row = i + 1, column = 0, sticky = W)
            drawableEntry.grid(row = i + 1, column = 1, sticky = W)
            textureEntry.grid(row = i + 1, column = 2, sticky = W)

            self._componentFields[id] = {"drawable": drawableEntry, "texture": textureEntry}

        self._propFields = {}
        for i, id in enumerate(PROP_IDS):
            propLabel = Label(propFrame, text = id.DESC)
            drawableEntry = Entry(propFrame)
            textureEntry = Entry(propFrame)
            propLabel.grid(row = i + 1, column = 0, sticky = W)
            drawableEntry.grid(row = i + 1, column = 1, sticky = W)
            textureEntry.grid(row = i + 1, column = 2, sticky = W)

            self._propFields[id] = {"drawable": drawableEntry, "texture": textureEntry}

        self._nameEntry.insert(0, self._variation.name)
        self._scriptNameEntry.insert(0, self._variation.getScriptName())
        if self._variation.base:
            self._baseName.set(self._variation.base)
        self._gender.set(self._variation.gender)

        for component in self._variation.components:
            self._componentFields[component.id]["drawable"].insert(0, component.drawable)
            self._componentFields[component.id]["texture"].insert(0, component.texture)

        for prop in self._variation.props:
            self._propFields[prop.id]["drawable"].insert(0, prop.drawable)
            self._propFields[prop.id]["texture"].insert(0, prop.texture)
   
        saveButton = Button(self, text = "Save", command = self._saveVariation)
        saveButton.grid(row = 4, column = 0, columnspan = 4, sticky = E + W)

    def _saveVariation(self):
        name = self._nameEntry.get()
        scriptName = self._scriptNameEntry.get()
        base = self._baseName.get()
        gender = self._gender.get()

        if not (name and gender):
            messagebox.showerror(title = "Save unsuccessful", message = "Name and gender are required")
            return

        if not re.match(r"^[A-Za-z0-9_-]*$", scriptName):
            messagebox.showerror("Save unsuccessful", "Script name must contain only letters, numbers, underscores, and dashes")
            return

        if base:
            if base == scriptName:
                messagebox.showerror(title = "Save unsuccessful", message = "An outfit's base can not be itself")
                return
            if not base in self._variation.outfit.getVariationScriptNames() or base == self._variation.getScriptName():
                messagebox.showerror(title = "Save unsuccessful", message = "Base {} is not a valid variation".format(base))
                return

        components = list()
        for id, component in self._componentFields.items():
            drawable = component["drawable"].get()
            texture = component["texture"].get()

            if not drawable:
                continue

            if not texture:
                messagebox.showerror(title = "Save unsuccessful", message = "If a component has a set drawable, a texture is required")
                return

            components.append(Outfit.Variation.Component(id, drawable, texture))

        props = list()
        for id, prop in self._propFields.items():
            drawable = prop["drawable"].get()
            texture = prop["texture"].get()

            if not drawable:
                continue

            if not texture:
                messagebox.showerror(title = "Save unsuccessful", message = "If a prop has a set drawable, a texture is required")
                return

            props.append(Outfit.Variation.Component(id, drawable, texture))

        existingVariation = self._variation.outfit.getVariationByScriptName(scriptName)
        if self._variation.getScriptName() != scriptName and existingVariation:
            if messagebox.askyesno(title = "Overwrite?", message = "A variation with the script name {} already exists in this outfit, overwrite?".format(scriptName)):
                if self._variationIndex < len(self._variation.outfit.variations):
                    self._variation.outfit.variations[self._variationIndex].delete()
                self._variationIndex = self._variation.outfit.variations.index(self._variation.outfit.getVariationByScriptName(scriptName))
            else:
                return

        self._variation.name = name
        self._variation.setScriptName(scriptName)
        self._variation.base = base
        self._variation.gender = gender
        self._variation.components = components
        self._variation.props = props

        if self._variationIndex < len(self._variation.outfit.variations):
            self._variation.outfit.variations[self._variationIndex].delete(False)
        self._variation.outfit.variations.insert(self._variationIndex, self._variation)

        self.update = True
        self.close()

class AgenciesTab(Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)

        listFrame = LabelFrame(self, text = "Agencies")
        listFrame.pack(side = LEFT, fill = BOTH, expand = True)
        buttonFrame = Frame(self)
        buttonFrame.pack(side = LEFT, fill = Y)

        self._listbox = listbox = BandedScrollListbox(listFrame, selectmode = EXTENDED)
        listbox.pack(side = LEFT, fill = BOTH, expand = True)

        addButton = Button(buttonFrame, text = "Add", command = self._addAgency)
        addButton.pack(fill = X)

        editButton = Button(buttonFrame, text = "Edit", command = self._editAgency)
        editButton.pack(fill = X)

        copyButton = Button(buttonFrame, text = "Duplicate", command = self._copyAgency)
        copyButton.pack(fill = X)

        deleteButton = Button(buttonFrame, text = "Delete", command = self._deleteAgency)
        deleteButton.pack(fill = X)

        listbox.bind("<Double-Button-1>", self._editAgency)
        listbox.bind("<Delete>", self._deleteAgency)

    def updateAgencies(self):
        self._listbox.delete(0, END)
        for agency in agencies:
            self._listbox.insert(END, "{} ({})".format(agency.name, agency.getScriptName()))

    def _addAgency(self):
        if EditAgencyMenu(self).update:
            self.updateAgencies()
            self._listbox.see(END)

    def _editAgency(self, event = None):
        if len(self._listbox.curselection()):
            i = self._listbox.curselection()[0]
            if EditAgencyMenu(self, i).update:
                self.updateAgencies()
                self._listbox.see(min(i, self._listbox.size() - 1))

    def _copyAgency(self):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                agency = copy.deepcopy(agencies[i])
                ii = 1
                scriptName = agency.getScriptName() + "_copy{}".format(ii)
                while getAgencyByScriptName(scriptName):
                    ii += 1
                    scriptName = agency.getScriptName() + "_copy{}".format(ii)
                agency.setScriptName(scriptName, False)
                agencies.insert(i + 1, agency)
            self.updateAgencies()
            self._listbox.see(min(i, self._listbox.size() - 1))

    def _deleteAgency(self, event = None):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                agencies[i].delete()
            self.updateAgencies()
            self._listbox.see(min(i, self._listbox.size() - 1))

class EditAgencyMenu(Dialog):
    def __init__(self, master, agencyIndex = None):
        self._agencyIndex = agencyIndex
        if agencyIndex is not None:
            self._agency = copy.deepcopy(agencies[agencyIndex])
        else:
            self._agency = Agency()
            self._agencyIndex = len(agencies)
            
        self.update = False

        super().__init__(master, "Edit agency")

    def _build(self):
        optionFrame = Frame(self)
        optionFrame.pack(fill = X)
        saveButton = Button(self, text = "Save", command = self._saveAgency)
        saveButton.pack(side = BOTTOM, fill = X)
        listFrame = LabelFrame(self, text = "Loadouts")
        listFrame.pack(side = LEFT, fill = BOTH, expand = True)
        buttonFrame = Frame(self)
        buttonFrame.pack(side = LEFT, fill = Y)

        nameLabel = Label(optionFrame, text = "Name:")
        nameLabel.grid(row = 0, column = 0, sticky = W)
        self._nameEntry = Entry(optionFrame)
        self._nameEntry.grid(row = 1, column = 0, sticky = W)

        shortNameLabel = Label(optionFrame, text = "Short name:")
        shortNameLabel.grid(row = 0, column = 1, sticky = W)
        self._shortNameEntry = Entry(optionFrame)
        self._shortNameEntry.grid(row = 1, column = 1, sticky = W)

        scriptNameLabel = Label(optionFrame, text = "Script name:")
        scriptNameLabel.grid(row = 0, column = 2, sticky = W)
        self._scriptNameEntry = Entry(optionFrame)
        self._scriptNameEntry.grid(row = 1, column = 2, sticky = W)

        parentLabel = Label(optionFrame, text = "Parent:")
        parentLabel.grid(row = 2, column = 0, sticky = W)
        self._parentName = StringVar(optionFrame)
        parentBox = AutoCombobox(optionFrame, width = 17, textvariable = self._parentName, values = getAgencyScriptNames())
        parentBox.grid(row = 3, column = 0, sticky = W)

        inventoryLabel = Label(optionFrame, text = "Inventory:")
        inventoryLabel.grid(row = 2, column = 1, sticky = W)
        self._inventoryName = StringVar(optionFrame)
        inventoryBox = AutoCombobox(optionFrame, width = 17, textvariable = self._inventoryName, values = getInventoryScriptNames())
        inventoryBox.grid(row = 3, column = 1, sticky = W)

        textureDictLabel = Label(optionFrame, text = "Texture dictionary:")
        textureDictLabel.grid(row = 4, column = 0, sticky = W)
        self._textureDictEntry = Entry(optionFrame)
        self._textureDictEntry.grid(row = 5, column = 0, sticky = W)

        textureNameLabel = Label(optionFrame, text = "Texture name:")
        textureNameLabel.grid(row = 4, column = 1, sticky = W)
        self._textureNameEntry = Entry(optionFrame)
        self._textureNameEntry.grid(row = 5, column = 1, sticky = W)

        self._excludeSetting = BooleanVar(optionFrame)
        excludeCheck = Checkbutton(optionFrame, text = "Exclude from backup menu", variable = self._excludeSetting)
        excludeCheck.grid(row = 6, column = 0, columnspan = 3, sticky = W)

        self._listbox = listbox = BandedScrollListbox(listFrame, selectmode = EXTENDED)
        listbox.pack(side = LEFT, fill = BOTH, expand = True)

        addButton = Button(buttonFrame, text = "Add", command = self._addLoadout)
        addButton.pack(fill = X)
        editButton = Button(buttonFrame, text = "Edit", command = self._editLoadout)
        editButton.pack(fill = X)
        copyButton = Button(buttonFrame, text = "Duplicate", command = self._copyLoadout)
        copyButton.pack(fill = X)
        deleteButton = Button(buttonFrame, text = "Delete", command = self._deleteLoadout)
        deleteButton.pack(fill = X)

        self._nameEntry.insert(0, self._agency.name)
        self._shortNameEntry.insert(0, self._agency.shortName)
        self._scriptNameEntry.insert(0, self._agency.getScriptName())
        if self._agency.parent:
            self._parentName.set(self._agency.parent)
        if self._agency.inventory:
            self._inventoryName.set(self._agency.inventory)
        self._textureDictEntry.insert(0, self._agency.textureDict)
        self._textureNameEntry.insert(0, self._agency.textureName)
        self._excludeSetting.set(self._agency.exclude)
        self._updateLoadouts()

        listbox.bind("<Double-Button-1>", self._editLoadout)
        listbox.bind("<Delete>", self._deleteLoadout)
    
    def _updateLoadouts(self):
        self._listbox.delete(0, END)
        for loadout in self._agency.loadouts:
            self._listbox.insert(END, loadout.name)

    def _addLoadout(self):
        if EditLoadoutMenu(self).update:
            self._updateLoadouts()

    def _editLoadout(self, event = None):
        if len(self._listbox.curselection()):
            if EditLoadoutMenu(self, self._listbox.curselection()[0]).update:
                self._updateLoadouts()

    def _copyLoadout(self):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                loadout = copy.deepcopy(self._agency.loadouts[i])
                loadout.name = "Copy of " + loadout.name
                self._agency.loadouts.insert(i + 1, loadout)
            self._updateLoadouts()

    def _deleteLoadout(self, event = None):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                del self._agency.loadouts[i]
            self._updateLoadouts()

    def _saveAgency(self):
        name = self._nameEntry.get()
        shortName = self._shortNameEntry.get()
        scriptName = self._scriptNameEntry.get()
        parent = self._parentName.get()
        inventory = self._inventoryName.get()
        textureDict = self._textureDictEntry.get()
        textureName = self._textureNameEntry.get()
        exclude = self._excludeSetting.get()

        if not name or not shortName or not scriptName:
            messagebox.showerror(title = "Save unsuccessful", message = "Name, short name, and script name are required")
            return

        if not re.match(r"^[A-Za-z0-9_-]*$", scriptName):
            messagebox.showerror("Save unsuccessful", "Script name must contain only letters, numbers, underscores, and dashes")
            return

        if textureDict and not re.match(r"^[A-Za-z0-9_-]*$", textureDict):
            messagebox.showerror("Save unsuccessful", "Texture dictionary must contain only letters, numbers, underscores, and dashes")
            return

        if textureName and not re.match(r"^[A-Za-z0-9_-]*$", textureName):
            messagebox.showerror("Save unsuccessful", "Texture name must contain only letters, numbers, underscores, and dashes")
            return

        if parent:
            if parent == scriptName:
                messagebox.showerror(title = "Save unsuccessful", message = "An agency's parent can not be itself")
                return
            if not parent in getAgencyScriptNames() or parent == self._agency.getScriptName():
                messagebox.showerror(title = "Save unsuccessful", message = "Parent {} is not a valid agency".format(parent))
                return

        if inventory and not inventory in getInventoryScriptNames():
            messagebox.showerror(title = "Save unsuccessful", message = "Inventory {} is not a valid inventory".format(inventory))
            return

        existingAgency = getAgencyByScriptName(scriptName)
        if self._agency.getScriptName() != scriptName and existingAgency:
            if messagebox.askyesno(title = "Overwrite?", message = "An agency with the script name {} already exists, overwrite?".format(scriptName)):
                if self._agencyIndex < len(agencies):
                    agencies[self._agencyIndex].delete()
                self._agencyIndex = agencies.index(getAgencyByScriptName(scriptName))
            else:
                return

        self._agency.name = name
        self._agency.shortName = shortName
        self._agency.setScriptName(scriptName)
        self._agency.parent = parent
        self._agency.inventory = inventory
        self._agency.textureDict = textureDict
        self._agency.textureName = textureName
        self._agency.exclude = exclude

        if self._agencyIndex < len(agencies):
            agencies[self._agencyIndex].delete(False)
        agencies.insert(self._agencyIndex, self._agency)

        self.update = True
        self.close()

class EditLoadoutMenu(Dialog):
    def __init__(self, master, loadoutIndex = None):
        self._loadoutIndex = loadoutIndex
        if loadoutIndex is not None:
            self._loadout = copy.deepcopy(master._agency.loadouts[loadoutIndex])
            self._loadout.agency = master._agency
        else:
            self._loadout = Agency.Loadout(master._agency)
            self._loadoutIndex = len(master._agency.loadouts)
            
        self.update = False

        super().__init__(master, "Edit loadout")

    def _build(self):
        optionFrame = Frame(self)
        optionFrame.pack(fill = X)

        nameLabel = Label(optionFrame, text = "Name:")
        nameLabel.grid(row = 0, column = 0, sticky = S)
        self._nameEntry = Entry(optionFrame)
        self._nameEntry.grid(row = 1, column = 0, sticky = N)

        chanceLabel = Label(optionFrame, text = "Chance:")
        chanceLabel.grid(row = 0, column = 1, sticky = S)
        self._chanceEntry = Entry(optionFrame)
        self._chanceEntry.grid(row = 1, column = 1, sticky = N)

        flagFrame = Frame(optionFrame)
        flagFrame.grid(row = 0, column = 2, rowspan = 2)

        self._transportSetting = BooleanVar(flagFrame)
        transportCheck = Checkbutton(flagFrame, text = "Responds as transport", variable = self._transportSetting)
        transportCheck.pack(anchor = W)

        self._backupSetting = BooleanVar(flagFrame)
        backupCheck = Checkbutton(flagFrame, text = "Responds as backup", variable = self._backupSetting)
        backupCheck.pack(anchor = W)

        self._ambientSetting = BooleanVar(flagFrame)
        ambientCheck = Checkbutton(flagFrame, text = "Spawns ambiently", variable = self._ambientSetting)
        ambientCheck.pack(anchor = W)

        self._swatSetting = BooleanVar(flagFrame)
        swatCheck = Checkbutton(flagFrame, text = "SWAT", variable = self._swatSetting)
        swatCheck.pack(anchor = W)

        vehiclesLabel = LabelFrame(self, text = "Vehicles")
        vehiclesLabel.pack(fill = BOTH, expand = True)

        vehiclesScrollFrame = ScrollFrame(vehiclesLabel)
        vehiclesScrollFrame.pack(fill = BOTH, expand = True)
        self._vehiclesFrame = vehiclesScrollFrame.interior

        addVehicleButton = Button(vehiclesLabel, text = "Add vehicle", command = self._addVehicle)
        addVehicleButton.pack(fill = X)

        pedsLabel = LabelFrame(self, text = "Peds")
        pedsLabel.pack(fill = BOTH, expand = True)

        numPedsFrame = Frame(pedsLabel)
        numPedsFrame.pack(anchor = W)

        minPedsLabel = Label(numPedsFrame, text = "Min. peds: ")
        minPedsLabel.pack(side = LEFT)
        self._minPedsBox = Spinbox(numPedsFrame, from_ = 1, to = 100)
        self._minPedsBox.pack(side = LEFT)

        maxPedsLabel = Label(numPedsFrame, text = "Max. peds: ")
        maxPedsLabel.pack(side = LEFT)
        self._maxPedsBox = Spinbox(numPedsFrame, from_ = 1, to = 100)
        self._maxPedsBox.pack(side = LEFT)

        pedsScrollFrame = ScrollFrame(pedsLabel)
        pedsScrollFrame.pack(fill = BOTH, expand = True)
        self._pedsFrame = pedsScrollFrame.interior

        addPedButton = Button(pedsLabel, text = "Add ped", command = self._addPed)
        addPedButton.pack(fill = X)

        saveButton = Button(self, text = "Save", command = self._saveLoadout)
        saveButton.pack(fill = X)

        self._nameEntry.insert(0, self._loadout.name)
        self._chanceEntry.insert(0, self._loadout.chance)
        self._transportSetting.set(self._loadout.checkFlag(Agency.Loadout.Flags.RESPONDS_AS_TRANSPORT))
        self._backupSetting.set(self._loadout.checkFlag(Agency.Loadout.Flags.RESPONDS_AS_BACKUP))
        self._ambientSetting.set(self._loadout.checkFlag(Agency.Loadout.Flags.SPAWNS_AMBIENTLY))
        self._swatSetting.set(self._loadout.checkFlag(Agency.Loadout.Flags.SWAT))
        self._maxPedsBox.insert(0, self._loadout.numPeds["max"])
        self._minPedsBox.insert(0, self._loadout.numPeds["min"])

        self._updateVehicles()
        self._updatePeds()

    def _updateVehicles(self):
        master = self._vehiclesFrame

        for widget in master.children.values():
            widget.grid_forget()

        if len(self._loadout.vehicles):
            nameColLabel = Label(master, text = "Model")
            nameColLabel.grid(row = 0, column = 0)

            chanceColLabel = Label(master, text = "Chance")
            chanceColLabel.grid(row = 0, column = 1)

            liveryColLabel = Label(master, text = "Livery")
            liveryColLabel.grid(row = 0, column = 2)

            weaponColLabel = Label(master, text = "Weapon")
            weaponColLabel.grid(row = 0, column = 3)

        for i, vehicle in enumerate(self._loadout.vehicles):
            row = i + 1

            modelName = StringVar(master, vehicle.name)
            modelBox = AutoCombobox(master, textvariable = modelName, values = VEHICLES)
            modelBox.grid(row = row, column = 0)

            chanceValue = StringVar(master, vehicle.chance)
            chanceEntry = Entry(master, textvariable = chanceValue)
            chanceEntry.grid(row = row, column = 1)

            liveryValue = StringVar(master, vehicle.livery)
            liveryEntry = Entry(master, textvariable = liveryValue)
            liveryEntry.grid(row = row, column = 2)

            weaponValue = StringVar(master, vehicle.weapon)
            weaponEntry = Entry(master, textvariable = weaponValue)
            weaponEntry.grid(row = row, column = 3)

            trace = partial(self._saveVehicle, i, modelName, chanceValue, liveryValue, weaponValue)
            modelName.trace("w", trace)
            chanceValue.trace("w", trace)
            liveryValue.trace("w", trace)
            weaponValue.trace("w", trace)

            command = partial(self._editExtras, i)
            editExtrasButton = Button(master, text = "Edit extras", command = command)
            editExtrasButton.grid(row = row, column = 4)

            command = partial(self._deleteVehicle, i)
            deleteButton = Button(master, text = "Delete", command = command)
            deleteButton.grid(row = row, column = 5)

    def _addVehicle(self):
        self._loadout.vehicles.append(Agency.Loadout.Vehicle())
        self._updateVehicles()

    def _deleteVehicle(self, index):
        del self._loadout.vehicles[index]
        self._updateVehicles()

    def _saveVehicle(self, index, modelName, chanceValue, liveryValue, weaponValue, *args):
        vehicle = self._loadout.vehicles[index]

        vehicle.name = modelName.get()
        try:
            vehicle.chance = max(0, min(100, int(chanceValue.get())))
        except ValueError:
            pass
        if not liveryValue.get():
            vehicle.livery = 0
        else:
            try:
                vehicle.livery = max(1, int(liveryValue.get()))
            except ValueError:
                pass
        vehicle.weapon = weaponValue.get()

    def _editExtras(self, index):
        EditExtrasMenu(self, self._loadout.vehicles[index])

    def _updatePeds(self):
        master = self._pedsFrame

        for widget in master.children.values():
            widget.grid_forget()

        if len(self._loadout.peds):
            nameColLabel = Label(master, text = "Model")
            nameColLabel.grid(row = 0, column = 0)
            
            chanceColLabel = Label(master, text = "Chance") 
            chanceColLabel.grid(row = 0, column = 1)

            outfitColLabel = Label(master, text = "Outfit")
            outfitColLabel.grid(row = 0, column = 2)

            inventoryColLabel = Label(master, text = "Inventory")
            inventoryColLabel.grid(row = 0, column = 3)

        for i, ped in enumerate(self._loadout.peds):
            row = i + 1

            modelName = StringVar(master, ped.name)
            modelEntry = AutoCombobox(master, textvariable = modelName, values = PEDS)
            modelEntry.grid(row = row, column = 0)

            chanceValue = StringVar(master, ped.chance)
            chanceEntry = Entry(master, textvariable = chanceValue)
            chanceEntry.grid(row = row, column = 1)

            outfitName = StringVar(master, ped.outfit)
            outfitBox = AutoCombobox(master, textvariable = outfitName, values = getOutfitScriptNames())
            outfitBox.grid(row = row, column = 2)

            inventoryName = StringVar(master, ped.inventory)
            inventoryBox = AutoCombobox(master, textvariable = inventoryName, values = getInventoryScriptNames())
            inventoryBox.grid(row = row, column = 3)

            randomizeSetting = BooleanVar(master, ped.randomizeProps)
            randomizeCheck = Checkbutton(master, text = "Randomize props", variable = randomizeSetting)
            randomizeCheck.grid(row = row, column = 4)

            trace = partial(self._savePed, i, modelName, chanceValue, outfitName, inventoryName, randomizeSetting)
            modelName.trace("w", trace)
            chanceValue.trace("w", trace)
            outfitName.trace("w", trace)
            inventoryName.trace("w", trace)
            randomizeSetting.trace("w", trace)

            command = partial(self._editPedComponents, i)
            Button(master, text = "Components", command = command).grid(row = row, column = 5)

            command = partial(self._deletePed, i)
            deleteButton = Button(master, text = "Delete", command = command)
            deleteButton.grid(row = row, column = 6)

    def _editPedComponents(self, index):
        EditPedComponentsMenu(self, self._loadout.peds[index])

    def _addPed(self):
        self._loadout.peds.append(Agency.Loadout.Ped())
        self._updatePeds()

    def _deletePed(self, index):
        del self._loadout.peds[index]
        self._updatePeds()

    def _savePed(self, index, modelName, chanceValue, outfitName, inventoryName, randomizeSetting, *args):
        ped = self._loadout.peds[index]

        ped.name = modelName.get()
        try:
            ped.chance = max(0, min(100, int(chanceValue.get())))
        except ValueError:
            pass
        ped.outfit = outfitName.get()
        ped.inventory = inventoryName.get()
        ped.randomizeProps = randomizeSetting.get()

    def _saveLoadout(self):
        if not self._nameEntry.get():
            messagebox.showerror("Save unsuccessful", "A name is required")
            return

        for vehicle in self._loadout.vehicles:
            if not vehicle.name:
                messagebox.showerror("Save unsuccessful", "All vehicles must have a model name set")
                return

        for ped in self._loadout.peds:
            if not ped.name:
                messagebox.showerror("Save unsuccessful", "All peds must have a model name set")
                return

            if ped.outfit and not ped.outfit in getOutfitScriptNames():
                messagebox.showerror("Save unsuccessful", "Outfit {} on ped {} is not a valid outfit".format(ped.outfit, ped.name))
                return

        self._loadout.name = self._nameEntry.get()

        try:
            self._loadout.chance = max(0, min(100, int(self._chanceEntry.get())))
        except ValueError:
            pass

        self._loadout.setFlag(Agency.Loadout.Flags.RESPONDS_AS_TRANSPORT, self._transportSetting.get())
        self._loadout.setFlag(Agency.Loadout.Flags.RESPONDS_AS_BACKUP, self._backupSetting.get())
        self._loadout.setFlag(Agency.Loadout.Flags.SPAWNS_AMBIENTLY, self._ambientSetting.get())
        self._loadout.setFlag(Agency.Loadout.Flags.SWAT, self._swatSetting.get())

        try:
            self._loadout.numPeds["min"] = max(1, int(self._minPedsBox.get()))
            self._loadout.numPeds["max"] = max(self._loadout.numPeds["min"], int(self._maxPedsBox.get()))
        except ValueError:
            pass

        if self._loadoutIndex < len(self._loadout.agency.loadouts):
            del self._loadout.agency.loadouts[self._loadoutIndex]

        self._loadout.agency.loadouts.insert(self._loadoutIndex, self._loadout)

        self.update = True
        self.close()

class EditPedComponentsMenu(Dialog):
    def __init__(self, master, ped):
        self._ped = ped

        super().__init__(master, "Edit components")

    def _build(self):
        componentFrame = LabelFrame(self, text = "Components")
        componentFrame.pack(fill = BOTH, expand = True)
        componentHeaderID = Label(componentFrame, text = "Component")
        componentHeaderDrawable = Label(componentFrame, text = "Drawable")
        componentHeaderTexture = Label(componentFrame, text = "Texture")
        componentHeaderID.grid(row = 0, column = 0)
        componentHeaderDrawable.grid(row = 0, column = 1)
        componentHeaderTexture.grid(row = 0, column = 2)

        propFrame = LabelFrame(self, text = "Props")
        propFrame.pack(fill = BOTH, expand = True)
        propHeaderID = Label(propFrame, text = "Prop")
        propHeaderDrawable = Label(propFrame, text = "Drawable")
        propHeaderTexture = Label(propFrame, text = "Texture")
        propHeaderID.grid(row = 0, column = 0)
        propHeaderDrawable.grid(row = 0, column = 1)
        propHeaderTexture.grid(row = 0, column = 2)

        self._componentFields = {}
        for i, id in enumerate(COMPONENT_IDS):
            componentLabel = Label(componentFrame, text = id.DESC)
            drawableEntry = Entry(componentFrame)
            textureEntry = Entry(componentFrame)
            componentLabel.grid(row = i + 1, column = 0, sticky = W)
            drawableEntry.grid(row = i + 1, column = 1, sticky = W)
            textureEntry.grid(row = i + 1, column = 2, sticky = W)

            self._componentFields[id] = {"drawable": drawableEntry, "texture": textureEntry}

        self._propFields = {}
        for i, id in enumerate(PROP_IDS):
            propLabel = Label(propFrame, text = id.DESC)
            drawableEntry = Entry(propFrame)
            textureEntry = Entry(propFrame)
            propLabel.grid(row = i + 1, column = 0, sticky = W)
            drawableEntry.grid(row = i + 1, column = 1, sticky = W)
            textureEntry.grid(row = i + 1, column = 2, sticky = W)

            self._propFields[id] = {"drawable": drawableEntry, "texture": textureEntry}
        
        for component in self._ped.components:
            self._componentFields[component.id]["drawable"].insert(0, component.drawable)
            self._componentFields[component.id]["texture"].insert(0, component.texture)

        for prop in self._ped.props:
            self._propFields[prop.id]["drawable"].insert(0, prop.drawable)
            self._propFields[prop.id]["texture"].insert(0, prop.texture)

        Button(self, text = "Save", command = self._saveComponents).pack(fill = X)

    def _saveComponents(self):
        components = list()
        for id, component in self._componentFields.items():
            drawable = component["drawable"].get()
            texture = component["texture"].get()

            if not drawable:
                continue

            if not texture:
                messagebox.showerror(title = "Save unsuccessful", message = "If a component has a set drawable, a texture is required")
                return

            components.append(Outfit.Variation.Component(id, drawable, texture))

        props = list()
        for id, prop in self._propFields.items():
            drawable = prop["drawable"].get()
            texture = prop["texture"].get()

            if not drawable:
                continue

            if not texture:
                messagebox.showerror(title = "Save unsuccessful", message = "If a prop has a set drawable, a texture is required")
                return

            props.append(Outfit.Variation.Component(id, drawable, texture))

        self._ped.components = components
        self._ped.props = props
        self.close()

class EditExtrasMenu(Dialog):
    def __init__(self, master, vehicle):
        self._vehicle = vehicle

        super().__init__(master, "Edit extras")

    def _build(self):
        self._extras = list()
        for i, extra in enumerate(self._vehicle.extras):
            extraLabel = Label(self, text = "Extra {}:".format(i + 1))
            extraLabel.grid(row = i, column = 0)

            extraValue = IntVar(self, extra)
            Radiobutton(self, text = "On", variable = extraValue, value = 1).grid(row = i, column = 1)
            Radiobutton(self, text = "Off", variable = extraValue, value = 0).grid(row = i, column = 2)
            Radiobutton(self, text = "Unset", variable = extraValue, value = -1).grid(row = i, column = 3)
            self._extras.append(extraValue)
        
        saveButton = Button(self, text = "Save", command = self._saveExtras)
        saveButton.grid(row = len(self._extras) + 1, column = 0, columnspan = 4, sticky = E + W) 

    def _saveExtras(self):
        self._vehicle.extras = list(map(lambda extraValue: extraValue.get(), self._extras))
        self.close()

class StationsTab(Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)

        listFrame = LabelFrame(self, text = "Stations")
        listFrame.pack(side = LEFT, fill = BOTH, expand = True)
        buttonFrame = Frame(self)
        buttonFrame.pack(side = LEFT, fill = Y)

        self._listbox = listbox = BandedScrollListbox(listFrame, selectmode = EXTENDED)
        listbox.pack(side = LEFT, fill = BOTH, expand = True)

        addButton = Button(buttonFrame, text = "Add", command = self._addStation)
        addButton.pack(fill = X)

        editButton = Button(buttonFrame, text = "Edit", command = self._editStation)
        editButton.pack(fill = X)

        deleteButton = Button(buttonFrame, text = "Delete", command = self._deleteStation)
        deleteButton.pack(fill = X)

        listbox.bind("<Double-Button-1>", self._editStation)
        listbox.bind("<Delete>", self._deleteStation)

    def updateStations(self):
        self._listbox.delete(0, END)
        for station in stations:
            self._listbox.insert(END, "{} ({})".format(station.name, station.scriptName))

    def _addStation(self):
        if EditStationMenu(self).update:
            self.updateStations()
            self._listbox.see(END)

    def _editStation(self, event = None):
        if len(self._listbox.curselection()):
            i = self._listbox.curselection()[0]
            if EditStationMenu(self, i).update:
                self.updateStations()
                self._listbox.see(min(i, self._listbox.size() - 1))

    def _deleteStation(self, event = None):
        if len(self._listbox.curselection()):
            for i in sorted(self._listbox.curselection(), reverse = True):
                del stations[i]
            self.updateStations()
            self._listbox.see(min(i, self._listbox.size() - 1))

class EditStationMenu(Dialog):
    def __init__(self, master, stationIndex = None):
        self._stationIndex = stationIndex
        if stationIndex is not None:
            self._station = copy.deepcopy(stations[stationIndex])
        else:
            self._station = Station()
            self._stationIndex = len(stations)

        super().__init__(master, "Edit station")

    def _build(self):
        Label(self, text = "Name:").grid(row = 0, column = 0)
        self._nameEntry = Entry(self)
        self._nameEntry.grid(row = 1, column = 0)

        Label(self, text = "Script name:").grid(row = 0, column = 1)
        self._scriptNameEntry = Entry(self)
        self._scriptNameEntry.grid(row = 1, column = 1)

        Label(self, text = "Agency:").grid(row = 2, column = 0)
        self._agencyValue = StringVar(self)
        AutoCombobox(self, textvariable = self._agencyValue, values = getAgencyScriptNames(), width = 17).grid(row = 3, column = 0)

        Label(self, text = "Position:").grid(row = 4, column = 0, columnspan = 3)
        self._positionXEntry = Entry(self)
        self._positionXEntry.grid(row = 5, column = 0)
        self._positionYEntry = Entry(self)
        self._positionYEntry.grid(row = 5, column = 1)
        self._positionZEntry = Entry(self)
        self._positionZEntry.grid(row = 5, column = 2)

        Label(self, text = "Heading:").grid(row = 4, column = 3)
        self._headingEntry = Entry(self)
        self._headingEntry.grid(row = 5, column = 3)

        Label(self, text = "Garage position:").grid(row = 6, column = 0, columnspan = 4)
        self._garageXEntry = Entry(self)
        self._garageXEntry.grid(row = 7, column = 0)
        self._garageYEntry = Entry(self)
        self._garageYEntry.grid(row = 7, column = 1)
        self._garageZEntry = Entry(self)
        self._garageZEntry.grid(row = 7, column = 2)
        self._garageHEntry = Entry(self)
        self._garageHEntry.grid(row = 7, column = 3)

        Label(self, text = "Garage spawn position:").grid(row = 8, column = 0, columnspan = 4)
        self._garageSpawnXEntry = Entry(self)
        self._garageSpawnXEntry.grid(row = 9, column = 0)
        self._garageSpawnYEntry = Entry(self)
        self._garageSpawnYEntry.grid(row = 9, column = 1)
        self._garageSpawnZEntry = Entry(self)
        self._garageSpawnZEntry.grid(row = 9, column = 2)
        self._garageSpawnHEntry = Entry(self)
        self._garageSpawnHEntry.grid(row = 9, column = 3)

        Label(self, text = "Drop off position:").grid(row = 10, column = 0, columnspan = 3)
        self._dropOffXEntry = Entry(self)
        self._dropOffXEntry.grid(row = 11, column = 0)
        self._dropOffYEntry = Entry(self)
        self._dropOffYEntry.grid(row = 11, column = 1)
        self._dropOffZEntry = Entry(self)
        self._dropOffZEntry.grid(row = 11, column = 2)

        Button(self, text = "Edit ambient spawns", command = self._editAmbientSpawns).grid(row = 12, column = 0, columnspan = 4, sticky = E + W)
        Button(self, text = "Save", command = self._saveStation).grid(row = 13, column = 0, columnspan = 4, sticky = E + W)

        self._nameEntry.insert(0, self._station.name)
        self._scriptNameEntry.insert(0, self._station.scriptName)
        self._agencyValue.set(self._station.agency)

        self._positionXEntry.insert(0, self._station.position[0])
        self._positionYEntry.insert(0, self._station.position[1])
        self._positionZEntry.insert(0, self._station.position[2])
        self._headingEntry.insert(0, self._station.heading)

        if self._station.garagePosition[0]:
            self._garageXEntry.insert(0, self._station.garagePosition[0])
            self._garageYEntry.insert(0, self._station.garagePosition[1])
            self._garageZEntry.insert(0, self._station.garagePosition[2])
            self._garageHEntry.insert(0, self._station.garagePosition[3])

        if self._station.garageSpawnPosition[0]:
            self._garageSpawnXEntry.insert(0, self._station.garageSpawnPosition[0])
            self._garageSpawnYEntry.insert(0, self._station.garageSpawnPosition[1])
            self._garageSpawnZEntry.insert(0, self._station.garageSpawnPosition[2])
            self._garageSpawnHEntry.insert(0, self._station.garageSpawnPosition[3])

        if self._station.dropOffPosition[0]:
            self._dropOffXEntry.insert(0, self._station.dropOffPosition[0])
            self._dropOffYEntry.insert(0, self._station.dropOffPosition[1])
            self._dropOffZEntry.insert(0, self._station.dropOffPosition[2])

    def _editAmbientSpawns(self):
        EditAmbientSpawnsMenu(self, self._station)

    def _saveStation(self):
        name = self._nameEntry.get()
        scriptName = self._scriptNameEntry.get()
        agency = self._agencyValue.get()
        position = [self._positionXEntry.get(), self._positionYEntry.get(), self._positionZEntry.get()]
        heading = self._headingEntry.get()
        garagePos = [self._garageXEntry.get(), self._garageYEntry.get(), self._garageZEntry.get(), self._garageHEntry.get()]
        garageSpawn = [self._garageSpawnXEntry.get(), self._garageSpawnYEntry.get(), self._garageSpawnZEntry.get(), self._garageSpawnHEntry.get()]
        dropOff = [self._dropOffXEntry.get(), self._dropOffYEntry.get(), self._dropOffZEntry.get()]

        if not name or not scriptName or not agency or not (position[0] and position[1] and position[2]) or not heading:
            messagebox.showerror("Save unsuccessful", "Name, script name, agency, position, and heading are required")
            return

        if not re.match(r"^[A-Za-z0-9_-]*$", scriptName):
            messagebox.showerror("Save unsuccessful", "Script name must contain only letters, numbers, underscores, and dashes")
            return

        if not agency in getAgencyScriptNames():
            messagebox.showerror("Save unsuccessful", "{} is not a valid agency".format(agency))
            return

        try:
            position = [float(position[0]), float(position[1]), float(position[2])]
            heading = float(heading)
            if garagePos[0] or garagePos[1] or garagePos[2] or garagePos[3]:
                garagePos = [float(garagePos[0]), float(garagePos[1]), float(garagePos[2]), float(garagePos[3])]
            if garageSpawn[0] or garageSpawn[1] or garageSpawn[2] or garageSpawn[3]:
                garageSpawn = [float(garageSpawn[0]), float(garageSpawn[1]), float(garageSpawn[2]), float(garageSpawn[3])]
            if dropOff[0] or dropOff[1] or dropOff[2]:
                dropOff = [float(dropOff[0]), float(dropOff[1]), float(dropOff[2])]
        except ValueError:
            messagebox.showerror("Save unsuccessful", "All position values must be numbers\nIf one field is included on an optional position, all fields for that position are required")
            return

        existingStation = getStationByScriptName(scriptName)
        if self._station.scriptName != scriptName and existingStation:
            if messagebox.askyesno(title = "Overwrite?", message = "A station with the script name {} already exists, overwrite?".format(scriptName)):
                if self._stationIndex < len(stations):
                    del stations[self._stationIndex]
                self._stationIndex = stations.index(getStationByScriptName(scriptName))
            else:
                return

        self._station.name = name
        self._station.scriptName = scriptName
        self._station.agency = agency
        self._station.position = position
        self._station.heading = heading
        self._station.garagePosition = garagePos
        self._station.garageSpawnPosition = garageSpawn
        self._station.dropOffPosition = dropOff
        
        if self._stationIndex < len(stations):
            del stations[self._stationIndex]

        stations.insert(self._stationIndex, self._station)

        self.update = True
        self.close()

class EditAmbientSpawnsMenu(Dialog):
    def __init__(self, master, station):
        self._station = station

        super().__init__(master, "Edit ambient spawns")

    def _build(self):
        self._spawnsFrame = ScrollFrame(self)
        self._spawnsFrame.pack(fill = BOTH, expand = True)

        Button(self, text = "Add spawn", command = self._addSpawn).pack(side = TOP, fill = X)
        Button(self, text = "Done", command = self.close).pack(side = TOP, fill = X)

        self._updateSpawns()

    def _updateSpawns(self):
        master = self._spawnsFrame.interior

        for widget in master.children.values():
            widget.grid_forget()

        Label(master, text = "Chance").grid(row = 0, column = 0)
        Label(master, text = "Position").grid(row = 0, column = 1, columnspan = 3)
        Label(master, text = "Heading").grid(row = 0, column = 4)

        for i, spawn in enumerate(self._station.ambientSpawns):
            row = i + 1

            chance = StringVar(master, spawn.chance)
            Entry(master, textvariable = chance).grid(row = row, column = 0)

            position = {"x": StringVar(master, spawn.position[0]), "y": StringVar(master, spawn.position[1]), "z": StringVar(master, spawn.position[2])}
            Entry(master, textvariable = position["x"]).grid(row = row, column = 1)
            Entry(master, textvariable = position["y"]).grid(row = row, column = 2)
            Entry(master, textvariable = position["z"]).grid(row = row, column = 3)

            heading = StringVar(master, spawn.heading)
            Entry(master, textvariable = heading).grid(row = row, column = 4)      

            trace = partial(self._saveSpawn, i, chance, position, heading)
            position["x"].trace("w", trace)
            position["y"].trace("w", trace)
            position["z"].trace("w", trace)
            heading.trace("w", trace)

            command = partial(EditAmbientSpawnMenu, self, spawn)
            Button(master, text = "Edit spawn", command = command).grid(row = row, column = 5)
       
    def _addSpawn(self):
        self._station.ambientSpawns.append(Station.AmbientSpawnPoint())
        self._updateSpawns()

    def _deleteSpawn(self, index):
        del self._station.ambientSpawns[index]
        self._updateSpawns()

    def _saveSpawn(self, index, chance, position, heading, *args):
        try:
            self._station.chance = float(chance.get())
        except ValueError:
            pass

        try:
            self._station.ambientSpawns[index].position = [float(position["x"].get()), float(position["y"].get()), float(position["z"].get())]
        except ValueError:
            pass

        try:
            self._station.ambientSpawns[index].heading = float(heading.get())
        except ValueError:
            pass

class EditAmbientSpawnMenu(Dialog):
    def __init__(self, master, spawnPoint):
        self._spawnPoint = spawnPoint

        super().__init__(master, "Edit spawn")

    def _build(self):
        self._spawnType = "Random" if self._spawnPoint.spawn is None else "Ped" if type(self._spawnPoint.spawn) is Agency.Loadout.Ped else "Vehicle"
        spawnType = StringVar(self, self._spawnType)
        spawnType.trace("w", self._updateOptions)
        OptionMenu(self, spawnType, self._spawnType, "Random", "Ped", "Vehicle").pack(side = TOP, anchor = CENTER)

        self._optionFrame = Frame(self)
        self._optionFrame.pack(side = TOP, fill = BOTH, expand = True)

        Button(self, text = "Save", command = self._saveSpawn).pack(side = TOP, fill = X)

        self._updateOptions(force = True)

    def _updateOptions(self, *args, force = False):
        if not force:
            if self.getvar(args[0]) == self._spawnType:
                return

            self._spawnType = self.getvar(args[0])

        for widget in self._optionFrame.children.values():
            widget.grid_forget()

        if self._spawnType == "Ped":
            self._spawnPoint.spawn = Agency.Loadout.Ped()

            nameColLabel = Label(self._optionFrame, text = "Model")
            nameColLabel.grid(row = 0, column = 0)
            
            chanceColLabel = Label(self._optionFrame, text = "Chance") 
            chanceColLabel.grid(row = 0, column = 1)

            outfitColLabel = Label(self._optionFrame, text = "Outfit")
            outfitColLabel.grid(row = 0, column = 2)

            inventoryColLabel = Label(self._optionFrame, text = "Inventory")
            inventoryColLabel.grid(row = 0, column = 3)
            
            self._modelName = StringVar(self._optionFrame, self._spawnPoint.spawn.name)
            modelEntry = AutoCombobox(self._optionFrame, textvariable = self._modelName, values = PEDS)
            modelEntry.grid(row = 1, column = 0)

            self._chanceValue = StringVar(self._optionFrame, self._spawnPoint.spawn.chance)
            chanceEntry = Entry(self._optionFrame, textvariable = self._chanceValue)
            chanceEntry.grid(row = 1, column = 1)

            self._outfitName = StringVar(self._optionFrame, self._spawnPoint.spawn.outfit)
            outfitBox = AutoCombobox(self._optionFrame, textvariable = self._outfitName, values = getOutfitScriptNames())
            outfitBox.grid(row = 1, column = 2)

            self._inventoryName = StringVar(self._optionFrame, self._spawnPoint.spawn.inventory)
            inventoryBox = AutoCombobox(self._optionFrame, textvariable = self._inventoryName, values = getInventoryScriptNames())
            inventoryBox.grid(row = 1, column = 3)

            self._randomizeSetting = BooleanVar(self._optionFrame, self._spawnPoint.spawn.randomizeProps)
            randomizeCheck = Checkbutton(self._optionFrame, text = "Randomize props", variable = self._randomizeSetting)
            randomizeCheck.grid(row = 1, column = 4)

            command = partial(EditPedComponentsMenu, self, self._spawnPoint.spawn)
            Button(self._optionFrame, text = "Components", command = command).grid(row = 1, column = 5)
        elif self._spawnType == "Vehicle":
            self._spawnPoint.spawn = Agency.Loadout.Vehicle()

            nameColLabel = Label(self._optionFrame, text = "Model")
            nameColLabel.grid(row = 0, column = 0)

            chanceColLabel = Label(self._optionFrame, text = "Chance")
            chanceColLabel.grid(row = 0, column = 1)

            liveryColLabel = Label(self._optionFrame, text = "Livery")
            liveryColLabel.grid(row = 0, column = 2)

            weaponColLabel = Label(self._optionFrame, text = "Weapon")
            weaponColLabel.grid(row = 0, column = 3)

            self._modelName = StringVar(self._optionFrame, self._spawnPoint.spawn.name)
            modelBox = AutoCombobox(self._optionFrame, textvariable = self._modelName, values = VEHICLES)
            modelBox.grid(row = 1, column = 0)

            self._chanceValue = StringVar(self._optionFrame, self._spawnPoint.spawn.chance)
            chanceEntry = Entry(self._optionFrame, textvariable = self._chanceValue)
            chanceEntry.grid(row = 1, column = 1)

            self._liveryValue = StringVar(self._optionFrame, self._spawnPoint.spawn.livery)
            liveryEntry = Entry(self._optionFrame, textvariable = self._liveryValue)
            liveryEntry.grid(row = 1, column = 2)

            self._weaponValue = StringVar(self._optionFrame, self._spawnPoint.spawn.weapon)
            weaponEntry = Entry(self._optionFrame, textvariable = self._weaponValue)
            weaponEntry.grid(row = 1, column = 3)

            command = partial(EditExtrasMenu, self, self._spawnPoint.spawn)
            editExtrasButton = Button(self._optionFrame, text = "Edit extras", command = command)
            editExtrasButton.grid(row = 1, column = 4)
        else:
            self._spawnPoint.spawn = None

            Label(self._optionFrame, text = "Random spawn type:").grid(row = 0, column = 0)

            self._type = StringVar(self._optionFrame, self._spawnPoint.type)
            OptionMenu(self._optionFrame, self._type, self._spawnPoint.type, "Ped", "Vehicle").grid(row = 1, column = 0)

    def _saveSpawn(self):
        self._spawnPoint.type = self._spawnType
        if self._spawnType == "Ped":
            self._spawnPoint.spawn.name = self._modelName.get()

            try:
                self._spawnPoint.spawn.chance = max(0, min(100, int(self._chanceValue.get())))
            except ValueError:
                pass
            
            self._spawnPoint.outfit = self._outfitName.get()
            self._spawnPoint.inventory = self._inventoryName.get()
            self._spawnPoint.randomizeProps = self._randomizeSetting.get()
        elif self._spawnType == "Vehicle":
            self._spawnPoint.spawn.name = self._modelName.get()

            try:
                self._spawnPoint.spawn.chance = max(0, min(100, int(self._chanceValue.get())))
            except ValueError:
                pass

            if not self._liveryValue.get():
                self._spawnPoint.spawn.livery = 0
            else:
                try:
                    self._spawnPoint.spawn.livery = max(1, int(self._liveryValue.get()))
                except ValueError:
                    pass

            self._spawnPoint.spawn.weapon = self._weaponValue.get()
        else:
            self._spawnPoint.type = self._type.get()

        self.close()

class RegionsTab(Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)

        regions.append(Region("HIGHWAY"))

        regionListFrame = LabelFrame(self, text = "Regions")
        regionListFrame.pack(side = LEFT, fill = BOTH, expand = True)

        self._regionList = regionList = BandedScrollListbox(regionListFrame, selectmode = EXTENDED)
        regionList.pack(side = LEFT, fill = BOTH, expand = True)
        regionList.bind("<Double-Button-1>", self._editRegion)
        regionList.bind("<Delete>", self._deleteRegion)

        regionButtonFrame = Frame(self)
        regionButtonFrame.pack(side = LEFT, fill = Y)

        addButton = Button(regionButtonFrame, text = "Add", command = self._addRegion)
        addButton.pack(fill = X)

        editButton = Button(regionButtonFrame, text = "Edit", command = self._editRegion)
        editButton.pack(fill = X)

        deleteButton = Button(regionButtonFrame, text = "Delete", command = self._deleteRegion)
        deleteButton.pack(fill = X)

    def updateRegions(self):
        self._regionList.delete(0, END)
        for region in regions[1:]:
            self._regionList.insert(END, region.getName())

        self.winfo_toplevel()._backupsTab.updateBackups()

    def _addRegion(self):
        if EditRegionMenu(self).update:
            self.updateRegions()
            self._regionList.see(END)

    def _editRegion(self, event = None):
        if len(self._regionList.curselection()):
            i = self._regionList.curselection()[0] + 1
            if EditRegionMenu(self, i).update:
                self.updateRegions()
                self._regionList.see(min(i, self._regionList.size() - 1))

    def _deleteRegion(self, event = None):
        if len(self._regionList.curselection()):
            for i in sorted(self._regionList.curselection(), reverse = True):
                regions[i + 1].delete()
            self.updateRegions()
            self._regionList.see(min(i + 1, self._regionList.size() - 1))

class EditRegionMenu(Dialog):
    def __init__(self, master, regionIndex = None):
        self._regionIndex = regionIndex
        if regionIndex is not None:
            self._region = copy.deepcopy(regions[regionIndex])
        else:
            self._region = Region()
            self._regionIndex = len(regions)

        self.update = False
        super().__init__(master, "Edit region")

    def _build(self):
        Button(self, text = "Save", command = self._saveRegion).pack(side = BOTTOM, fill = X)

        nameFrame = Frame(self)
        nameFrame.pack(side = TOP, fill = X)

        Label(nameFrame, text = "Name: ").pack(side = LEFT)
        self._nameEntry = Entry(nameFrame)
        self._nameEntry.pack(side = LEFT)

        currentZoneFrame = LabelFrame(self, text = "Current zones")
        currentZoneFrame.pack(side = LEFT, fill = BOTH, expand = True)

        self._currentZoneList = BandedScrollListbox(currentZoneFrame, selectmode = EXTENDED)
        self._currentZoneList.pack(side = LEFT, fill = BOTH, expand = True)

        zoneButtonFrame = Frame(self)
        zoneButtonFrame.pack(side = LEFT)

        addZoneButton = Button(zoneButtonFrame, text = "⮜", command = self._addZone)
        addZoneButton.pack(fill = X)

        removeZoneButton = Button(zoneButtonFrame, text = "⮞", command = self._removeZone)
        removeZoneButton.pack(fill = X)

        availableZoneFrame = LabelFrame(self, text = "Available zones")
        availableZoneFrame.pack(side = LEFT, fill = BOTH, expand = True)

        self._availableZoneList = BandedScrollListbox(availableZoneFrame, selectmode = EXTENDED)
        self._availableZoneList.pack(side = LEFT, fill = BOTH, expand = True)

        self._nameEntry.insert(0, self._region.getName())
        self._updateZones()

    def _updateZones(self):
        self._currentZoneList.delete(0, END)
        for zone in self._region.zones:
            self._currentZoneList.insert(END, ZONES[zone])

        self._availableZones = getAvailableZones()
        if self._regionIndex < len(regions):
            self._availableZones = sorted(self._availableZones + regions[self._regionIndex].zones)
        self._availableZones = list(filter(lambda zone: zone not in self._region.zones, self._availableZones))

        self._availableZoneList.delete(0, END)
        for zone in self._availableZones:
            self._availableZoneList.insert(END, ZONES[zone])

    def _addZone(self):
        if len(self._availableZoneList.curselection()):
            for i in self._availableZoneList.curselection():
                zone = self._availableZones[i]
                self._region.zones.append(zone)
            self._updateZones()

    def _removeZone(self):
        if len(self._currentZoneList.curselection()):
            for i in sorted(self._currentZoneList.curselection(), reverse = True):
                del self._region.zones[i]
            self._updateZones()

    def _saveRegion(self):
        name = self._nameEntry.get()

        if not name:
            messagebox.showerror("Save unsuccessful", "A name is required")
            return

        if not re.match(r"^[A-Za-z0-9_-]*$", name):
            messagebox.showerror("Save unsuccessful", "Name must contain only letters, numbers, underscores, and dashes")
            return

        existingRegion = getRegionByName(name)
        if self._region.getName() != name and existingRegion:
            if messagebox.askyesno(title = "Overwrite?", message = "A region with the name {} already exists, overwrite?".format(name)):
                if self._regionIndex < len(regions):
                    regions[self._regionIndex].delete()
                self._regionIndex = regions.index(getRegionByName(name))
            else:
                return

        self._region.setName(name)

        if self._regionIndex < len(regions):
            regions[self._regionIndex].delete(False)

        regions.insert(self._regionIndex, self._region)
        
        self.update = True
        self.close()

class BackupsTab(Frame):
    def __init__(self, master, *args, **kw):
        super().__init__(master, *args, **kw)

        self._tree = tree = ScrollTreeview(self, columns = ["agency"])
        tree.pack(side = LEFT, fill = BOTH, expand = True)
        tree.bind("<Delete>", self._deleteAgency)

        optionFrame = Frame(self)
        optionFrame.pack(side = LEFT, fill = Y)

        Button(optionFrame, text = "Add", command = self._addAgency).pack(fill = X)
        Button(optionFrame, text = "Edit", command = self._editAgency).pack(fill = X)
        Button(optionFrame, text = "Delete", command = self._deleteAgency).pack(fill = X)

        tree.heading("#0", text = "Backup type/region")
        tree.heading("agency", text = "Agency")

        tree.tag_bind("agency", "<Double-Button-1>", self._editAgency)

        self.updateBackups()

    def updateBackups(self):
        tree = self._tree

        tree.delete(*tree.get_children())

        for backupType in Backup.Types:
            tree.insert("", END, backupType.name, text = backupType.value)
            for region in regions:
                regionID = backupType.name + "." + region.getName()
                tree.insert(backupType.name, END, regionID, text = region.getName(), tags = ["region"])
                backup = region.getBackup(backupType)
                if backup:
                    for agency in backup.agencies:
                        tree.insert(regionID, END, regionID + "." + agency, values = [agency], tags = ["agency"])

    def _addAgency(self):
        item = self._tree.focus()
        tags = self._tree.item(item)["tags"]
        if ("region" in tags or "agency" in tags) and EditBackupAgencyMenu(self, item).update:
            self.updateBackups()
            self._tree.see(item)
            self._tree.selection_set(item)

    def _editAgency(self, event = None):
        item = self._tree.focus()
        tags = self._tree.item(item)["tags"]
        if "agency" in tags:
            parent = self._tree.parent(item)
            index = self._tree.get_children(parent).index(item)
            if EditBackupAgencyMenu(self, item, index).update:
                self.updateBackups()
                self._tree.see(parent)
                self._tree.selection_set(parent)

    def _deleteAgency(self, event = None):
        item = self._tree.focus()
        tags = self._tree.item(item)["tags"]
        if "agency" in tags:
            parent = self._tree.parent(item)
            
            items = item.split(".")
            type = Backup.Types[items[0]]
            region = getRegionByName(items[1])
            backup = region.getBackup(type)

            index = self._tree.get_children(parent).index(item)
            del backup.agencies[index]

            self.updateBackups()
            self._tree.see(parent)
            self._tree.selection_set(parent)
        
class EditBackupAgencyMenu(Dialog):
    def __init__(self, master, item, agencyIndex = None):
        self._agencyIndex = agencyIndex

        item = item.split(".")
        type = Backup.Types[item[0]]
        region = getRegionByName(item[1])
        self._backup = region.getBackup(type)
        if not self._backup:
            self._backup = Backup(type.name, region.getName())
            backups.append(self._backup)

        self.update = False
        super().__init__(master, "Edit backup")

    def _build(self):
        Button(self, text = "Save", command = self._saveAgency).pack(side = BOTTOM, fill = X)

        Label(self, text = "Agency: ").pack(side = LEFT)
        
        self._agencyName = StringVar(self)
        AutoCombobox(self, textvariable = self._agencyName, values = getAgencyScriptNames()).pack(side = LEFT)

        if self._agencyIndex is not None:
            self._agencyName.set(self._backup.agencies[self._agencyIndex])

    def _saveAgency(self):
        agency = self._agencyName.get()

        if not agency:
            messagebox.showerror("Save unsuccessful", "Agency is required")
            return
        
        if not agency in getAgencyScriptNames():
            messagebox.showerror("Save unsuccessful", "{} is not a valid agency".format(agency))
            return

        if not (self._agencyIndex is not None and agency == self._backup.agencies[self._agencyIndex]) and agency in self._backup.agencies:
            messagebox.showerror("Save unsuccessful", "{} is already listed under {} for {}".format(agency, self._backup.type, self._backup.region))
            return

        if self._agencyIndex is not None:
            self._backup.agencies[self._agencyIndex] = agency
        else:
            self._backup.agencies.append(agency)

        self.update = True
        self.close()

class Inventory:
    def __init__(self, name = "", scriptName = "", stunWeapon = None, armor = 0):
        self.name = name
        self._scriptName = scriptName
        self.weapons = list()
        self.stunWeapon = stunWeapon
        self.armor = armor

    def setScriptName(self, scriptName, changeReferences = True):
        if scriptName == self._scriptName:
            return

        if changeReferences:
            for agency in agencies:
                if agency.inventory == self._scriptName:
                    agency.inventory = scriptName
                
                for ped in agency.getPedsWithInventory(self._scriptName):
                    ped.inventory = scriptName

        self._scriptName = scriptName

    def getScriptName(self):
        return self._scriptName

    def delete(self, removeReferences = True):
        if self in inventories:
            inventories.remove(self)

        if removeReferences:
            for agency in agencies:
                if agency.inventory == self._scriptName:
                    agency.inventory = ""
                
                for ped in agency.getPedsWithInventory(self._scriptName):
                    ped.inventory = ""

    class Weapon:
        def __init__(self, inventory, name = WEAPON_IDs[0], chance = 100, components = None):
            self.inventory = inventory
            self.name = name
            self.chance = chance
            if components is None:
                self.components = list()
            else:
                self.components = components

class Outfit:
    def __init__(self, name = "", scriptName = ""):
        self.name = name
        self._scriptName = scriptName
        self.variations = list()

    def setScriptName(self, scriptName, changeReferences = True):
        if scriptName == self._scriptName:
            return

        if changeReferences:
            for agency in agencies:
                for ped in agency.getPedsWithOutfit(self._scriptName):
                    ped.outfit = scriptName

        self._scriptName = scriptName

    def getScriptName(self):
        return self._scriptName

    def delete(self, removeReferences = True):
        if self in outfits:
            outfits.remove(self)

        if removeReferences:
            for agency in agencies:
                for ped in agency.getPedsWithOutfit(self._scriptName):
                    ped.outfit = ""

    def combineVariations(self, other):
        for variation in other.variations:
            variationCopy = copy.deepcopy(variation)
            variationCopy.outfit = self
            self.variations.append(variationCopy)

    def getVariationByScriptName(self, scriptName):
        if scriptName:
            for variation in self.variations:
                if variation.getScriptName() == scriptName:
                    return variation
        
        return None

    def getVariationScriptNames(self):
        return list(filter(None, map(lambda variation: variation.getScriptName(), self.variations)))

    

    class Variation:
        def __init__(self, outfit, name = "", scriptName = "", base = "", gender = "male", components = None, props = None):
            self.outfit = outfit
            self.name = name
            self._scriptName = scriptName
            self.base = base
            self.gender = gender
            if components is None:
                self.components = list()
            else:
                self.components = components
            if props is None:
                self.props = list()
            else:
                self.props = props            

        def setScriptName(self, scriptName, changeReferences = True):
            if scriptName == self._scriptName:
                return

            if self._scriptName and changeReferences:
                for variation in self.outfit.variations:
                    if variation.base == self._scriptName:
                        variation.base = scriptName

                for agency in agencies:
                    for ped in agency.getPedsWithVariation(self._scriptName):
                        outfit = ped.outfit.split(".")
                        outfit[1] = scriptName
                        ped.outfit = ".".join(outfit)

            self._scriptName = scriptName

        def getScriptName(self):
            return self._scriptName

        def delete(self, removeReferences = True):
            if self in self.outfit.variations:
                self.outfit.variations.remove(self)

            if removeReferences:
                for variation in self.outfit.variations:
                    if variation.base == self._scriptName:
                        variation.base = ""

                for agency in agencies:
                    for ped in agency.getPedsWithVariation(self._scriptName):
                        outfit = ped.outfit.split(".")
                        ped.outfit = outfit[0]
                            
        class Component:
            def __init__(self, id, drawable, texture):
                self.id = id
                self.drawable = drawable
                self.texture = texture

class Agency:
    def __init__(self, name = "", shortName = "", scriptName = "", parent = "", inventory = "", textureDict = "", textureName = "", exclude = False):
        self.name = name
        self.shortName = shortName
        self._scriptName = scriptName
        self.parent = parent
        self.inventory = inventory
        self.loadouts = list()
        self.textureDict = textureDict
        self.textureName = textureName
        self.exclude = exclude

    def setScriptName(self, scriptName, changeReferences = True):
        if scriptName == self._scriptName:
            return

        if changeReferences:
            for agency in agencies:
                if agency.parent == self._scriptName:
                    agency.parent = scriptName

            for backup in backups:
                if self._scriptName in backup.agencies:
                    backup.agencies[backup.agencies.index(self._scriptName)] = scriptName

        self._scriptName = scriptName

    def getScriptName(self):
        return self._scriptName

    def delete(self, removeReferences = True):
        if self in agencies:
            agencies.remove(self)

        if removeReferences:
            for agency in agencies:
                if agency.parent == self._scriptName:
                    agency.parent = ""

            for backup in backups:
                if self._scriptName in backup.agencies:
                    backup.agencies.remove(self._scriptName)

    def getPedsWithOutfit(self, outfit):
        peds = list()
        for loadout in self.loadouts:
            for ped in loadout.peds:
                if ped.outfit == outfit:
                    peds.append(ped)
        
        return peds

    def getPedsWithVariation(self, variation):
        peds = list()
        for loadout in self.loadouts:
            for ped in loadout.peds:
                outfit = ped.outfit.split(".")
                if len(outfit) > 1 and outfit[0] == self._scriptName and outfit[1] == variation:
                    peds.append(ped)

        return peds

    def getPedsWithInventory(self, inventory):
        peds = list()
        for loadout in self.loadouts:
            for ped in loadout.peds:
                if ped.inventory == inventory:
                    peds.append(ped)

        return peds

    class Loadout:
        class Flags(IntFlag):
            RESPONDS_AS_TRANSPORT = auto()
            RESPONDS_AS_BACKUP = auto()
            SPAWNS_AMBIENTLY = auto()
            SWAT = auto()

            def __str__(self):
                flagNames = {
                    Agency.Loadout.Flags.RESPONDS_AS_TRANSPORT: "RespondsAsTransport",
                    Agency.Loadout.Flags.RESPONDS_AS_BACKUP: "RespondsAsBackup",
                    Agency.Loadout.Flags.SPAWNS_AMBIENTLY: "SpawnsAmbiently",
                    Agency.Loadout.Flags.SWAT: "SWAT"
                }

                return flagNames[self]

            @classmethod
            def toFlag(cls, string):
                for flag in cls:
                    if str(flag) == string:
                        return flag

                return None

        def __init__(self, agency, name = "", chance = 100, vehicles = None, peds = None, numPeds = None, flags = 0):
            self.agency = agency
            self.name = name
            self.chance = chance
            self._flags = flags
            if vehicles is not None:
                self.vehicles = vehicles
            else:
                self.vehicles = list()
            if peds is not None:
                self.peds = peds
            else:
                self.peds = list()
            if numPeds is not None:
                self.numPeds = numPeds
            else:
                self.numPeds = {"min": 1, "max": 1}

        def setFlag(self, flag, state):
            if flag in Agency.Loadout.Flags:
                if state:
                    self._flags |= flag
                else:
                    self._flags &= ~flag

        def checkFlag(self, flag):
            return self._flags & flag

        def hasFlags(self):
            return self._flags != 0

        class Vehicle:
            def __init__(self, name = "", chance = 100, livery = 0, weapon = "", extras = None):
                self.name = name
                self.chance = chance
                self.livery = livery
                self.weapon = weapon
                if extras is not None:
                    self.extras = extras
                else:
                    self.extras = [-1] * 15

        class Ped:
            def __init__(self, name = "", chance = 100, outfit = "", inventory = "", components = None, props = None, randomizeProps = True):
                self.name = name
                self.chance = chance
                self.outfit = outfit
                self.inventory = inventory
                self.randomizeProps = randomizeProps

                self.components = components
                if components is None:
                    self.components = list()

                self.props = props
                if props is None:
                    self.props = list()

class Station:
    def __init__(self, name = "", scriptName = "", agency = "", position = None, heading = 0, garagePosition = None, garageSpawnPosition = None, dropOffPosition = None, ambientSpawns = None):
        self.name = name
        self.scriptName = scriptName
        self.agency = agency
        self.position = position
        self.heading = heading
        self.dropOffPosition = dropOffPosition
        self.garagePosition = garagePosition
        self.garageSpawnPosition = garageSpawnPosition
        self.ambientSpawns = ambientSpawns

        if position is None:
            self.position = [0] * 3
        if garagePosition is None:
            self.garagePosition = [None] * 4
        if garageSpawnPosition is None:
            self.garageSpawnPosition = [None] * 4
        if dropOffPosition is None:
            self.dropOffPosition = [None] * 3

        if ambientSpawns is None:
            self.ambientSpawns = list()

    class AmbientSpawnPoint:
        def __init__(self, chance = 100, position = None, heading = 0, type = "Ped", spawn = None):
            self.chance = chance
            self.position = position
            self.heading = heading
            self.type = type
            self.spawn = spawn

            if position is None:
                self.position = [0] * 3

class Region:
    def __init__(self, name = "", zones = None):
        self._name = name

        self.zones = zones
        if zones is None:
            self.zones = list()

    def setName(self, name):
        if name == self._name:
            return

        for backup in backups:
            if backup.region == self._name:
                backup.region = name

        self._name = name

    def getName(self):
        return self._name

    def delete(self, removeReferences = True):
        if self in regions:
            regions.remove(self)

        if removeReferences:
            for backup in backups:
                if backup.region == self._name:
                    backups.remove(backup)

    def getBackup(self, type):
        for backup in backups:
            if backup.region == self._name and backup.type == type.name:
                return backup
        return None

class Backup:
    class Types(Enum):
        LOCAL_PATROL = "LocalPatrol"
        STATE_PATROL = "StatePatrol"
        LOCAL_SWAT = "LocalSWAT"
        NOOSE_SWAT = "NooseSWAT"
        LOCAL_AIR = "LocalAir"
        NOOSE_AIR = "NooseAir"
        AMBULANCE = "Ambulance"
        FIRETRUCK = "FireTruck"
        FEMALE_LOCAL = "FemaleLocalPatrol"
        FEMALE_STATE = "FemaleStatePatrol"
        K9_LOCAL = "K9LocalPatrol"
        K9_STATE = "K9StatePatrol"
        CORONER = "Coroner"

    def __init__(self, type, region, agencies = None):
        self.type = type
        self.region = region
        self.agencies = agencies

        if not agencies:
            self.agencies = list()

MainWindow()
