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

test_failed = False


civitdl_test_no = 0
civitdl_error_test_no = 0
civitconfig_test_no = 0
civitconfig_error_test_no = 0


## Install Module ##

subprocess.run(
    ['python', '-m', 'venv', testvenv_dirpath])
activate_cmd = 'testvenv\\Scripts\\activate' if os.name == 'nt' else 'source testvenv/bin/activate'
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


def civitdl_test(sources, options=[]):
    global civitdl_test_no
    civitdl_test_no += 1
    try:
        print(f'Civitdl General Test {civitdl_test_no}:')
        res = run_civitdl(sources, f'./general/test{civitdl_test_no}', options)
        print(f'Civitdl General Test {civitdl_test_no} success!')
    except Exception as e:
        print(f'Civitdl General Test {civitdl_test_no} failed!')
        global test_failed
        test_failed = True


def civitdl_error_test(sources, options=[]):
    global civitdl_error_test_no
    civitdl_error_test_no += 1
    try:
        print(f'Civitdl Error Test {civitdl_error_test_no}:')
        res = run_civitdl(sources, './error', options, show_error=False)
        print(f'Civitdl Error Test {civitdl_error_test_no} failed!')
        global test_failed
        test_failed = True
    except Exception as e:
        # traceback.print_exc()
        # print(e)
        print(f'Civitdl Error Test {civitdl_error_test_no} success!')


def civitconfig_test(subcommand, options=[]):
    global civitconfig_test_no
    civitconfig_test_no += 1
    try:
        print(f'Civitconfig General Test {civitconfig_test_no}:')
        res = run_civitconfig(subcommand, options)
        print(f'Civitconfig General Test {civitconfig_test_no} success!')
    except:
        print(f'Civitconfig General Test {civitconfig_test_no} failed!')
        global test_failed
        test_failed = True


def civitconfig_error_test(subcommand, options=[]):
    global civitconfig_error_test_no
    civitconfig_error_test_no += 1
    try:
        print(f'Civitconfig Error Test {civitconfig_error_test_no}:')
        res = run_civitconfig(subcommand, options, show_error=False)
        print(f'Civitconfig Error Test {civitconfig_error_test_no} failed!')
        test_failed = True
    except Exception as e:
        # traceback.print_exc()
        # print(e)
        print(f'Civitconfig Error Test {civitconfig_error_test_no} success!')


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

civitconfig_test('default', ['--no-with-color'])

civitdl_test(['123456'], ['--limit-rate', '1M',
             '--max-images', '20', '--nsfw-mode', '0'])
civitdl_test(['123456', '23456'], ['--sorter', 'tags',
             '--max-images', '20', '--nsfw-mode', '1'])
civitdl_test([os.path.join(batch_data_dirpath,
                           'batchtest1.txt')])
civitdl_test(['123456'], ['--no-with-prompt', '--pause-time', '5'])
civitdl_test(['https://civitai.com/api/download/models/317633'])
civitdl_test(['123456'], ['--with-color'])

civitconfig_test('default')
civitconfig_test('sorter')
civitconfig_test('alias')
civitconfig_test('default', ['--sorter', 'tags',
                 '--limit-rate', '10M', '--without-model'])
civitconfig_test('default', ['--sorter', 'basic',
                 '--limit-rate', '0', '--no-without-model'])
civitconfig_test('default', ['--with-color'])
civitconfig_test('default', ['--no-with-color'])

civitconfig_test('sorter', ['--add', 'alpha',
                 os.path.join(batch_data_dirpath, 'sort.py')])
civitconfig_test('default', ['--sorter', 'alpha'])
civitconfig_test('sorter', ['--delete', 'alpha'])
civitconfig_error_test('default', ['--sorter', 'alpha'])
civitconfig_test('alias', ['--add', 'test', './models'])
civitconfig_test('alias', ['--add', 'test2', 'test2/goforit'])
civitconfig_test('alias', ['--delete', 'test'])
civitconfig_test('alias', ['--delete', 'test2'])

civitdl_test(['123456'])
civitconfig_test('default', ['--with-color'])


## Clean up ##
print('Starting Cleaning')

shutil.rmtree(testvenv_dirpath)


if test_failed:
    print('End to End Test Failed!')
    exit(1)
else:
    print('End to End Test Success!')
    exit(0)
