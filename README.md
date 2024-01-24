# civitdl (civitai-batch-download)

**Note v2 has some changes regarding the cli args of the program. Please read the README below or run `civitdl --help` for the new arguments!**
- To see changes to v2, go to [Changes in v2](#changes-in-v2-from-v1) section.

Uses CLI to batch download Stable Diffusion models, metadata (including description of model, author, base model, example prompts and etc.) and example images (default is 3) of checkpoints, loras, and TI models from civitai!

One thing to note is that for sfw models, currently, the program is set to only download sfw images. Please note that there may be sfw models that are rated as nsfw by CivitAI (and vice versa).

<br/>

## Navigate
- [README Page](/README.md)
- [Alias Page](/doc/alias.md)
- [API Key Page](/doc/api_key.md)
- [Civitconfig / Configuration Page](/doc/civitconfig.md)
- [Civitdl Page](/doc/civitdl.md)
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
    - [Quick Start](#quick-start)
      - [Configuration Program Options - civitconfig](#configuration-program-options---civitconfig)
  - [Changes in v2 from v1](#changes-in-v2-from-v1)
  - [Troubleshooting](#troubleshooting)
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
make install # Now program is installed globally unless you are using a virtual env
# make install2 # Run this if make install fails
```

### Quick Start
To get started quickly, copy the command below.
- See [civitdl doc](/doc/civitdl.md) for more info.

``` bash
civitdl 123456 ./models
```
- Replace `123456` your model of choice (it can be a civitai.com url or model id).
- Replace `./models` with the directory you wish to download the model to.

<br/>

#### Configuration Program Options - civitconfig
- Configuring the program might make your life easier. You would be able to set default sorter, max images, and api key to use without running any of those options in the main program!
  - You would also be able to add and delete sorters and aliases from the program.
  - Check [civitconfig doc](/doc/civitconfig.md).
- Run `civitconfig --help` to check what options are available!

<br/>

## Changes in v2 from v1
- basic and tags sorter now downloads metadata and images to `/parent_dir/extra_data/` instead of to `/parent_dir/`
- Sorter is now more flexible/customizable (i.e. able to select individual paths model, metadata and images should go to)
- Added support for providing API Key to program to download restricted models.
  - See [api key doc](/doc/api_key.md)
- Added multiple new options to the main program, civitdl.
  - See [civitdl doc](/doc/civitdl.md)
- Added configuration to set defaults for options, and to create alias + sorters.
  - See [civitconfig doc](/doc/civitconfig.md) 
- Concurrently download images.
- Isolates each image's prompt/metadata from the model's metadata.
- Able to retry download if model fails initially.
- Faster requests.
- Added features to skip model download if model already exists in path, or locally in cache.

<br/>

## Troubleshooting

------

If you encounter similar warning on Linux/Windows while building and installing manually:
```bash
  WARNING: The script civitdl is installed in '/home/OwenTruong/.local/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
```

For Linux, please concat the path to your PATH env, example:
```bash
echo 'PATH="$HOME/.local/bin:"$PATH' >> ~/.bashrc
source ~/.bashrc
```

For Windows, this may help: https://www.computerhope.com/issues/ch000549.htm

If you are building from source and the following packages are not available `setuptools, wheel, build`, please install them with `pip install setuptools wheel build`

------

If you are building the project and python unsuccessfully installs the program with `make install`, and displays the package's name as `UNKNOWN`, it is likely because you are trying to install the package globally. Either run `make install2` or use virtual env `python -m venv venv && source ./venv/bin/activate && make install`.

------

<br/>



## Contributing

Thanks for the interest in the project!

Please create an issue if you encounter any problem, bugs or if you have a feature request.

To debug things, it is recommended to run with `--verbose` option.
* Running in verbose allows users to print tracebacks and other messages useful for debugging.
* Example: `civitdl 123456 ./models --verbose`

To work on an issue:
* Please create a fork.
* Then clone your fork locally.
* Then create a local branch that describes the issue.
* Once you have commited your changes, push the branch to your forked repository.
* Then open a pull request to this repository.

<br/>

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](./License) file for details
