# Civitmisc
- In this page, we will go over various tasks (WIP) that do not directly relate to configuration and downloading model from the API.
- Run `civitmisc --help` when you need help on some options!

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
- [Civitmisc](#civitmisc)
  - [Navigate](#navigate)
  - [Table Of Contents](#table-of-contents)
  - [Cache](#cache)
    - [Scan Model](#scan-model)

<br/>

## Cache
Operations relating to the cache. The cache currently contains the file path and hash of each model that have been downloaded. Note that only one file path may be stored, so if you tried to download the same model multiple time in different directories, the file path saved will be the last time you downloaded the same model.
- If a file path is stored in cache, then the next time `civitdl` is requested to download the same model, it will automatically copy the file from the file path stored in the cache.
- See `civitconfig cache --help`

<br/>

### Scan Model
- This scans a directory recursively to find model files with matching file names. The syntax is `mid_x-vid_y` in the file name where `mid` is model id, `vid` is version id, and `x` & `y` are substitued with valid model and version ids. Please try not to change the file name so that `-s` or `--scan-model` works properly. It is fine to modify directory/folder name.
- This is also useful if you want to check if any of your downloaded models have been corrupted as SHA256 is used to check the integrity of every model file `scan-model` finds.
- Shorthand: `civitmisc cache -s /path/to/directory`
- Longhand: `civitmisc cache -s /path/to/directory`

