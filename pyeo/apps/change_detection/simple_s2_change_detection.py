"""A simple change detection script that downloads, stacks and classifies an image"""

import submodules.pyeo as pc
import configparser
import argparse
import os

#Reading in config file
parser = argparse.ArgumentParser(description='Automatically detect and report on change')
parser.add_argument('--conf', dest='config_path', action='store', default=r'change_detection.ini',
                    help="Path to the .ini file specifying the job.")
args = parser.parse_args()

conf = configparser.ConfigParser()
conf.read(args.config_path)
sen_user = conf['sent_2']['user']
sen_pass = conf['sent_2']['pass']
project_root = conf['forest_sentinel']['root_dir']
aoi_path = conf['forest_sentinel']['aoi_path']
start_date = conf['forest_sentinel']['start_date']
end_date = conf['forest_sentinel']['end_date']
log_path = conf['forest_sentinel']['log_path']
cloud_cover = conf['forest_sentinel']['cloud_cover']
cloud_certainty_threshold = int(conf['forest_sentinel']['cloud_certainty_threshold'])
sen2cor_path = conf['sen2cor']['path']

pc.create_file_structure(project_root)
log = pc.init_log(log_path)


l1_image_path = os.path.join(project_root, r"images/L1")
l2_image_path = os.path.join(project_root, r"images/L2")
planet_image_path = os.path.join(project_root, r"images/planet")
merged_image_path = os.path.join(project_root, r"images/merged")
stacked_image_path = os.path.join(project_root, r"images/stacked")
catagorised_image_path = os.path.join(project_root, r"output/categories")
probability_image_path = os.path.join(project_root, r"output/probabilities")

#Query and download
log.info("Downloading")
pc.sent2_query(sen_user, sen_pass, aoi_path, start_date, end_date, l1_image_path, )

# Atmospheric correction
log.info("Applying sen2cor")
pc.atmospheric_correction(l1_image_path, l2_image_path, sen2cor_path)

# Aggregating layers into single image
log.info("Aggregating layers")
pc.aggregate_and_mask_10m_bands(l2_image_path, merged_image_path, cloud_certainty_threshold)



# 2.3 export to .tif

# # ############################################################################################################
# # ###### 3. Post processing                                                                  #################
# # ######    3.1 cloud masking  = DONE                                                        #################
# # ######    3.2 image tools: resample/clip/re-project/masking/plot                           #################
# # ######    3.3 regional mosaics                                                             #################
# # ######    3.4 time series stacks                                                           #################
# # ######    3.5 fusion tools: co-registration/ stacking                                      #################
# # ############################################################################################################

# 3.1 cloud mask

# 3.1.1 default masking using generated mask from Sen2Cor
# 3.1.2 option for user-input mask (a advanced random-forest based cloud masking)

# 3.2 image tools:
#  resample
#  os.system('gdalwarp -overwrite -tr 25 25 -r cubic ' + i + ' ' + iout)
#  clip
#  re-project
#  masking with user input layer (e.g. sea)

#3.3 regional mosaics

#3.4 time series stacks

#3.5 fusion tools: co-registration

# # ############################################################################################################
# # ###### 4. Analysing                                                                        #################
# # ######    4.1 change maps                                                                  #################
# # ######    4.2 annual stacks                                                                #################
# # ######    4.3 time series stacks / temporal statistics                                     #################
# # ######    4.4 real-time detection / alerts                                                 #################
# # ######    4.5 validation                                                                   #################
# # ############################################################################################################

#4.1 change maps: random forest based change detection

#4.2 annual stacks

#4.3 time series and temporal statistics

#4.4 real-time detection / alerts


#4.5 validation