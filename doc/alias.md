# Alias
- In this page, we will go over what aliases are, their purpose, and how to utilize them.
- Run `civitconfig alias --help` when you need help on some options!

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
- [Alias](#alias)
  - [Navigate](#navigate)
  - [Table Of Contents](#table-of-contents)
  - [What Are Aliases?](#what-are-aliases)
    - [Example Of Substitution / Usage:](#example-of-substitution--usage)
    - [Example Of Relative Alias Usage:](#example-of-relative-alias-usage)
  - [Configuring Alias](#configuring-alias)
    - [List aliases](#list-aliases)
    - [Add an alias](#add-an-alias)
    - [Delete an alias](#delete-an-alias)
  - [Example of adding, using, and deleting an alias](#example-of-adding-using-and-deleting-an-alias)

<br/>

## What Are Aliases?
- Aliases in `civitdl` are a way to subsitute keywords with some paths for rootdir (last argument a user provides to `civitdl`). 
  - `civitdl source1 source2 ... sourceN rootdir-path`
- This was made to be more convenient for users who do not wish to remember or write out a long path to the root directory at where they would like to download their models.

<br/>

### Example Of Substitution / Usage:

Suppose we have an alias named `@models` 
  that is mapped to the path `/home/ubuntu/ComfyUI/models`

Then we run the following command to download Anything v3 to the subdirectories inside following root directory, `/home/ubuntu/ComfyUI/models/checkpoints`
  -  `civitdl 66 @models/checkpoints`
  -  The above command translates to 
      -  `civitdl 66 /home/ubuntu/ComfyUI/models/checkpoints`

Assuming that we are using the basic sorter, the ckpt file path is equivalent to the following: 
  - `/home/ubuntu/ComfyUI/models/checkpoints/anythingV3_fp16/anythingV3_fp16-mid_66-vid_75.ckpt`

<br/>

### Example Of Relative Alias Usage:

A relative alias is an alias where its path contains another alias.

Suppose we have two aliases `@models` and `@loras`
  - `@models` is mapped to the path `/home/ubuntu/ComfyUI/models`
  - `@loras` is the relative alias that is mapped to the path `@models/loras`

To download a lora with a model id of 80848 to the subdirectories inside the following root directory, `/home/ubuntu/ComfyUI/models/loras`
  - `civitdl 80848 @loras`
  - The above command translates to
    - `civitdl 80848 /home/ubuntu/ComfyUI/models/loras`

Assuming that we are using the basic sorter, the lora file path is equivalent to the following:
  - `/home/ubuntu/ComfyUI/models/loras/hatsunemiku1-000006/hatsunemiku1-000006-mid_80848-vid_85767.safetensors`

For details on sorters, please head to [sorter doc](./sorter.md)

<br/>

## Configuring Alias
- Duplicate of [alias section in configuration](./configuration.md#aliases)

<br/>

### List aliases
- Run `civitconfig alias` to list the aliases saved to the program.

<br/>

### Add an alias
- Path can be relative or absolute.
- Shorthand: `civitconfig alias -a alias-name /path/to/the/alias/dir`
- Longhand: `civitconfig alias --add alias-name /path/to/the/alias/dir`

<br/>

### Delete an alias
- Shorthand: `civitconfig alias -d alias-name`
- Longhand: `civitconfig alias --delete alias-name`

<br/>

## Example of adding, using, and deleting an alias
```bash
civitconfig alias -a @loras /home/ubuntu/ComfyUI/models/loras
civitdl 123456 @loras
civitconfig alias -d @loras
```
