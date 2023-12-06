# Config
- In this page, we will go over three types of configurations: default, sorters, and aliases.
- Run `civitconfig --help` when you need help on some options!

<br/>

## Navigate
- [README Page](/README.md)
- [Alias Page](/doc/alias.md)
- [API Key Page](/doc/api_key.md)
- [Configuration Page](/doc/configuration.md)
- [Sorter Page](/doc/sorter.md)


<br/>

## Table Of Contents
- [Config](#config)
  - [Navigate](#navigate)
  - [Table Of Contents](#table-of-contents)
  - [Defaults](#defaults)
    - [Set max image](#set-max-image)
    - [Set sorter](#set-sorter)
      - [What is a sorter?](#what-is-a-sorter)
    - [Set api key](#set-api-key)
      - [Why do we need an api key?](#why-do-we-need-an-api-key)
  - [Sorters](#sorters)
    - [List sorters](#list-sorters)
    - [Add a sorter](#add-a-sorter)
    - [Delete a sorter](#delete-a-sorter)
  - [Aliases](#aliases)
    - [List aliases](#list-aliases)
    - [Add an alias](#add-an-alias)
    - [Delete an alias](#delete-an-alias)

<br/>

## Defaults
Defaults set the defaults for options that are used in `civitdl` command.

<br/>

### Set max image
- This sets the default max images to download from civitai when `civitdl` is run without the option `-i` or `--max-images`

To set the default max images to N (N >= 0): 
- Shorthand: `civitconfig default -i N`
- Longhand: `civitconfig default --max-images N`

Set the default max image to a number you are comfortable with when you run `civitdl`

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

### Set api key
- This sets the default api key to use when `civitdl` is run without the option `-k` or `--api-key`

#### Why do we need an api key?
- Some model authors require the user to log in before downloading their model.
- See [API Key](./api_key.md) for instructions.

To set the default api key, use the below option and the program will securely prompt you for your api key.
- Shorthand: `civitconfig default -k`
- Longhand: `civitconfig default --api-key`

<br/>

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



