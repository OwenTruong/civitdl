import sys
from get_lora_api import download_model


download_model(dst_dir_path='manuel-test',
               model_id=sys.argv[1], version_id=115273)
