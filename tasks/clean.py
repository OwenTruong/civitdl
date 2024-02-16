import glob
import os
import shutil

try:
    os.remove('./log.txt')
except:
    print('./log.txt not found')

try:
    matching_directories = glob.glob('**/*.egg-info', recursive=True)
    for dir_path in matching_directories:
        try:
            shutil.rmtree(dir_path)
        except Exception as e:
            print(e)
except Exception as e:
    print(e)

try:
    shutil.rmtree('./test/models')
except:
    print('./test/models not found')

try:
    shutil.rmtree('./dist')
except:
    print('./dist not found')

try:
    shutil.rmtree('./build')
except:
    print('./build not found')
