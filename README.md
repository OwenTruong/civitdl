# civitdl (civitai-batch-download)

**Note v2 has some changes regarding the cli args of the program. Please read the README below or run `civitdl --help` for the new arguments!**
- To see changes to v2, go to [Changes in v2](#changes-in-v2-from-v1) section.

Uses CLI to batch download Stable Diffusion models from CivitAI, metadata (including description of model, author, base model, example prompts and etc.) and example images (default is 3) of checkpoint, lora, and TI models!

One thing to note is that for sfw models, currently, the program is set to only download sfw images. Please note that there may be sfw models that are rated as nsfw by CivitAI (and vice versa).

<br/>

## Navigate
- [README Page](/README.md)
- [Alias Page](/doc/alias.md)
- [API Key Page](/doc/api_key.md)
- [Configuration Page](/doc/configuration.md)
- [Sorter Page](/doc/sorter.md)

<br/>

## Table Of Contents
- [civitdl (civitai-batch-download)](#civitdl-civitai-batch-download)
  - [Navigate](#navigate)
  - [Table Of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Dependencies](#dependencies)
    - [Installing](#installing)
      - [Install using PIP](#install-using-pip)
      - [Build from source](#build-from-source)
      - [Troubleshooting](#troubleshooting)
    - [Quick Start](#quick-start)
    - [Executing program v2](#executing-program-v2)
      - [Sources](#sources)
        - [Note about Model ID vs Version ID of a model](#note-about-model-id-vs-version-id-of-a-model)
        - [batchfile](#batchfile)
      - [Main Program Options - civitdl](#main-program-options---civitdl)
      - [Configuration Program Options - civitconfig](#configuration-program-options---civitconfig)
  - [Changes in v2 from v1](#changes-in-v2-from-v1)
  - [Contributing](#contributing)
  - [License](#license)

<br/>

## Getting Started

### Dependencies
* Python3
* `requirements.txt`

<br/>

### Installing

#### Install using PIP
```bash
pip3 install civitdl
```
- Use `pip install civitdl` if `pip3` is not found.

<br/>

#### Build from source
```bash
git clone https://github.com/OwenTruong/civitdl.git # Clone the project
cd civitdl # CD into project directory
pip install -r requirements.txt # use pip3 if pip is not found
make install # Now program is installed globally unless you are using a virtual env
```

<br/>

#### Troubleshooting

If you encounter the following warning on Linux:
```bash
  WARNING: The script civitdl is installed in '/home/OwenTruong/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

Please concat the path to your PATH env, example:
```bash
echo 'PATH="$HOME/.local/bin:"$PATH' >> ~/.bashrc
source ~/.bashrc
```

If you are building from source and the following packages are not available `setuptools, wheel, build`, please install them with `pip install setuptools wheel build`

<br/>

### Quick Start
To get started quickly, copy the command below.

``` bash
civitdl model_id rootpath
```
- Replace `model_id` your model of choice.
- Replace `rootpath` with the directory you wish to download the model to.

<br/>

### Executing program v2
- New Args:
  - `civitdl source1 source2 ... sourceN dst_root_directory`
- Example usage:
  - `civitdl 123456 ./batchfile.txt ./models`
- Run `civitdl --help` for help with arguments.


<br/>

#### Sources
- Sources can be either one of the following
  - Model ID
  - `civitai.com/models` url
  - `civitai.com/api/downloads/models` url
  - `/path/to/batchfile.txt` batch file path
- Examples
  - `civitdl https://civitai.com/models/7808/easynegative 79326 ~/Downloads/ComfyUI/models/loras`

<br/>

##### Note about Model ID vs Version ID of a model
- If you need a specific version of a model, copy paste the url of the specific version in the txt file, and it would download the correct one.
  - Example of a url with a specific version id: `https://civitai.com/models/197273?modelVersionId=221861`

<br/>

##### batchfile 
* Batchfile contain a comma separated list of sources.
* Examples:
    * `civitdl ./custom/batchfile.txt ~/sorted-models --sorter tags`
* See [batchfile.txt](./custom/batchfile.txt) for example of a batchfile

<br/>

#### Main Program Options - civitdl
- Run `civitdl --help` to check what options are available!

Three options are available
- `-i <number>` or `--max-images <number>`
  - Specifies the max images to download for each model.
  - Example: `civitdl 123456 ./loras -i 20`
- `-s <sorter-name / path>` or `--sorter <sorter-name / path>`
  - Specifies which sorter to use. The default uses the basic sorter.
  - See [sorter doc](./doc/sorter.md) for more infor.
  - Example: `civitdl 123456 ./loras -s tags`
- `-k` or `--api-key`
  - Running with this option will prompt the user to type in their API key.
  - See [api key doc](/doc/api_key.md) for help on how to get and use API key.
  - Example: `civitdl 123456 ./loras -k`

<br/>

#### Configuration Program Options - civitconfig
- Configuring the program may make your life easier. You would be able to set default sorter, max images, and api key to use without running any of those options in the main program!
  - You would also be able to add and delete sorters and aliases from the program.
  - Check [configuration doc](/doc/configuration.md).
- Run `civitconfig --help` to check what options are available!

<br/>

## Changes in v2 from v1
- basic and tags sorter now downloads metadata and images to `/parent_dir/extra_data/` instead of to `/parent_dir/`
- Sorter is now more flexible/customizable (i.e. able to select individual paths model, metadata and images should go to)
- Added support for providing API Key to program to download restricted models.
  - See [api key doc](/doc/api_key.md)
- Added configuration to set defaults for options, and to create alias + sorters.
  - See [config doc](/doc/configuration.md) 



## Contributing

Thanks for the interest in the project!

Please create an issue if you encounter any problem, bugs or if you have a feature request.

To run the script in development mode, run `-v` or `--dev` option.
* Running in development mode allows users to print tracebacks and other messages useful for debugging.
* Example: `civitdl 123456 ./models -d`

To work on an issue:
* Please create a fork.
* Then clone your fork locally.
* Then create a local branch that describes the issue.
* Once you have commited your changes, push the branch to your forked repository.
* Then open a pull request to this repository.

<br/>

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](./License) file for details
