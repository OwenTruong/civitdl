import unittest
import subprocess
import os
import shutil
from pathlib import Path
import traceback

from dotenv import load_dotenv

# TODO: Store api key securely

# This end to end testing will mainly ensure that no program crashing bugs exist. This testing does not guarantee the program will download the correct data.

## Variables ##

root_dirpath = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

model_dirpath = os.path.join(root_dirpath, 'test', 'models')

batch_data_dirpath = os.path.join(root_dirpath, 'test', 'data')

testvenv_dirpath = os.path.join(root_dirpath, 'testvenv')

testlog_filepath = os.path.join(root_dirpath, 'test', 'models', 'testlog.txt')

config_testlog_filepath = os.path.join(
    root_dirpath, 'test', 'models', 'config_testlog.txt')


## Install Module ##

subprocess.run(
    ['python', '-m', 'venv', testvenv_dirpath])
activate_cmd = 'testvenv\\Scripts\\activate' if subprocess.run(
    ['uname'], capture_output=True, text=True).stdout.strip() == 'Windows' else 'source testvenv/bin/activate'
subprocess.run(['pip', 'install', root_dirpath])


## Helpers ##

def run_civitdl(sources, path, options=[], show_error=True):
    with open(testlog_filepath, 'a', encoding='UTF-8') as file:
        result = subprocess.run(
            ['civitdl', *sources, Path(os.path.join(model_dirpath, path)).resolve(), *options, '--verbose'], text=True, capture_output=True)

        file.write(result.stdout)

        if result.returncode != 0 or result.stderr != '':
            if show_error:
                print(f'Return Code: {result.returncode}')
                print(f'Stderr: {result.stderr}')
            raise Exception(result.stderr)
        else:
            return result


def run_civitconfig(subcommand, options=[], show_error=True):
    with open(config_testlog_filepath, 'a', encoding='UTF-8') as file:
        result = subprocess.run(
            ['civitconfig', subcommand, *options, '--verbose'], text=True, capture_output=True)

        file.write(result.stdout)

        if result.returncode != 0 or result.stderr != '':
            if show_error:
                print(f'Return Code: {result.returncode}')
                print(f'Stderr: {result.stderr}')
            raise Exception(result.stderr)
        else:
            return result


def civitdl_test(id, sources, options=[]):
    try:
        print(f'Civitdl General Test {id}:')
        res = run_civitdl(sources, f'./general/test{id}', options)
        print(f'Civitdl General Test {id} success!')
    except Exception as e:
        print(f'Civitdl General Test {id} failed!')


def civitdl_error_test(id, sources, options=[]):
    try:
        print(f'Civitdl Error Test {id}:')
        res = run_civitdl(sources, './error', options, show_error=False)
        print(f'Civitdl Error Test {id} failed!')
    except Exception as e:
        # traceback.print_exc()
        # print(e)
        print(f'Civitdl Error Test {id} success!')


def civitconfig_test(id, subcommand, options=[]):
    try:
        print(f'Civitconfig General Test {id}:')
        res = run_civitconfig(subcommand, options)
        print(f'Civitconfig General Test {id} success!')
    except:
        print(f'Civitconfig General Test {id} failed!')


def civitconfig_error_test(id, subcommand, options=[]):
    try:
        print(f'Civitconfig Error Test {id}:')
        res = run_civitconfig(subcommand, options, show_error=False)
        print(f'Civitconfig Error Test {id} failed!')
    except Exception as e:
        # traceback.print_exc()
        # print(e)
        print(f'Civitconfig Error Test {id} success!')


## Setup ##
print('Starting Setup')
os.makedirs(model_dirpath, exist_ok=True)

load_dotenv(os.path.join(root_dirpath, '.env'))  # for local testing

if os.environ['API_KEY'] is None or os.environ['API_KEY'] == '':
    print('Please provide an api key before running the tests.')
    exit(1)

subprocess.run(['civitconfig', 'default', '--api-key', os.environ['API_KEY'], '--verbose'],
               stdout=subprocess.DEVNULL)

## Tests ##
print('Starting Tests')

civitdl_test(1, ['123456'])
civitdl_test(2, ['123456', '23456'], ['--sorter', 'tags'])
civitdl_test(3, [os.path.join(batch_data_dirpath,
                              'batchtest1.txt')], ['--limit-rate', '1M'])
civitdl_test(4, ['123456'], ['--no-with-prompt', '--pause-time', '5'])

civitconfig_test(1, 'default')
civitconfig_test(2, 'sorter')
civitconfig_test(3, 'alias')
civitconfig_test(
    4, 'default', ['--sorter', 'tags', '--limit-rate', '10M', '--without-model'])
civitconfig_test(5, 'sorter', ['--add', 'alpha',
                 os.path.join(batch_data_dirpath, 'sort.py')])
civitconfig_test(6, 'default', ['--sorter', 'alpha'])
civitconfig_test(7, 'sorter', ['--delete', 'alpha'])
civitconfig_error_test(1, 'default', ['--sorter', 'alpha'])
civitconfig_test(8, 'alias', ['--add', 'test', './models'])
civitconfig_test(9, 'alias', ['--add', 'test2', 'test2/goforit'])
civitconfig_test(10, 'alias', ['--delete', 'test'])
civitconfig_test(11, 'alias', ['--delete', 'test2'])


## Clean up ##
print('Starting Cleaning')

shutil.rmtree(testvenv_dirpath)
