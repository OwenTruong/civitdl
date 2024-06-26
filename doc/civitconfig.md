# Civitconfig
- In this page, we will go over on how to configure the program with civitconfig command.
- Run `civitconfig --help` when you need help on some options!

<br/>

## Navigate
- [README Page](/README.md)
- [Alias Page](/doc/alias.md)
- [API Key Page](/doc/api_key.md)
- [Civitconfig / Configuration Page](/doc/civitconfig.md)
- [Civitdl Page](/doc/civitdl.md)
- [Civitmisc Page](/doc/civitmisc.md)
- [Sorter Page](/doc/sorter.md)

<br/>

## Table Of Contents
- [Civitconfig](#civitconfig)
  - [Navigate](#navigate)
  - [Table Of Contents](#table-of-contents)
  - [Defaults](#defaults)
    - [Set sorter](#set-sorter)
      - [What is a sorter?](#what-is-a-sorter)
    - [Set max image](#set-max-image)
    - [Set api key](#set-api-key)
      - [Why do we need an api key?](#why-do-we-need-an-api-key)
    - [Set with prompt](#set-with-prompt)
    - [Other possible defaults to set](#other-possible-defaults-to-set)
  - [Sorters](#sorters)
    - [List sorters](#list-sorters)
    - [Add a sorter](#add-a-sorter)
    - [Delete a sorter](#delete-a-sorter)
  - [Aliases](#aliases)
    - [List aliases](#list-aliases)
    - [Add an alias](#add-an-alias)
    - [Delete an alias](#delete-an-alias)
  - [Settings](#settings)
    - [Reset Config](#reset-config)
    - [Download Config](#download-config)

<br/>

## Defaults
Defaults set the defaults for options that are used in `civitdl` command.
- See `civitconfig default --help`

<br/>

### Set sorter
- This sets the default sorter to use when `civitdl` is run without the option `-s` or `--sorter` 

#### What is a sorter?
- Sorter is a way to manage multiple downloaded models with ease. It separates each model downloaded into multiple directores.
- See [sorter doc](./sorter.md)

To set the default sorter to `mysorter`:
- Shorthand: `civitconfig default -s mysorter`
- Longhand: `civitconfig default --sorter mysorter`

Set the sorter you want to use to organize your checkpoint, lora and other models' directories.
Do note that you can only set sorters that have been added to the config.

<br/>

### Set max image
- This sets the default max images to download from civitai when `civitdl` is run without the option `-i` or `--max-images`

To set the default max images to N (N >= 0): 
- Shorthand: `civitconfig default -i N`
- Longhand: `civitconfig default --max-images N`

Set the default max image to a number you are comfortable with when you run `civitdl`

<br/>

### Set api key
- This sets the default api key to use when `civitdl` is run without the option `-k` or `--api-key`

#### Why do we need an api key?
- Some model authors require the user to log in before downloading their model.
- See [API Key](./api_key.md) for instructions.

To set the default api key, use the below option and the program will securely prompt you for your api key.
- Shorthand: `civitconfig default -k`
- Longhand: `civitconfig default --api-key`

<br/>

### Set with prompt
- This sets the default attribute `with-prompt` on whether to download images when `civitdl` is run without the option `-p` or `--with-prompt` or `--no-with-prompt`

To set the default attribute for enabling `with-prompt`:
- Shorthand: `civitconfig default -p`
- Longhand: `civitconfig default --with-prompt`

To set the default attribute for disabling `with-prompt`:
- Longhand: `civitconfig default --no-with-prompt`

<br>

### Other possible defaults to set
- There are options like `--nsfw-mode`, `--with-prompt`, `--limit-rate`, `--retry-count` and `--pause-time` that you can set defaults for!
- See `civitconfig default --help` for more info.
- See [civitdl doc](./civitdl.md#options) on what each option do.

<br>


## Sorters
- List, add, and remove sorters from program.
- See [sorter doc](./sorter.md)

<br/>

### List sorters
- Run `civitconfig sorter` to list the sorters saved to the program.

<br/>

### Add a sorter
- Adds and saves sorter to program. Must be a .py file with a function called `sort_model`. See [sorter doc](./sorter.md) on requirements.
- Shorthand: `civitconfig sorter -a mysorter /path/to/sorter.py`
- Longhand: `civitconfig sorter --add mysorter /path/to/sorter.py`

<br/>

### Delete a sorter
- Removes sorter from program.
- Shorthand: `civitconfig sorter -d mysorter`
- Longhand: `civitconfig sorter --delete mysorter`

<br/>

## Aliases
- List, add, and remove aliaases from program.
- See [alias doc](./alias.md)

<br/>

### List aliases
- Run `civitconfig alias` to list the aliases saved to the program.

<br/>

### Add an alias
- Shorthand: `civitconfig alias -a alias-name /path/to/the/alias/dir`
- Longhand: `civitconfig alias --add alias-name /path/to/the/alias/dir`
- See [alias doc](./alias.md) on how to add relative alias.

<br/>

### Delete an alias
- Shorthand: `civitconfig alias -d alias-name`
- Longhand: `civitconfig alias --delete alias-name`


<br/>

## Settings
- Collection of options related to the civitconfig program itself.
- Ability to reset and download configs.

<br/>

### Reset Config
- Shorthand: `civitconfig settings -r`
- Longhand: `civitconfig settings --reset`
- Run to reset configuration to the most recent default configuration.
- All of your previous configs will be added to a trash directory in the program's data directory.

<br/>


### Download Config
- Shorthand: `civitconfig settings -d /path/to/zipped-config.zip`
- Longhand: `civitconfig settings --download /path/to/zipped-config.zip`
- Run to download your configuration as a zip file.