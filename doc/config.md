# Config
- In this page, we will go over three types of configurations: default, sorters, and aliases.

Run `civitconfig --help` when you need help on some options!


## Defaults
- Defaults set the defaults for options that are used in `civitdl` command.

### Set max image
This sets the default max images to download from civitai when `civitdl` is run without the option `-i` or `--max-images`

To set the default max images to 10: 
- Shorthand: `civitconfig default -i 10`
- Longhand: `civitconfig default --max-images 10`

Set the default max image to a number you are comfortable with when you run `civitdl`

Example of setting max images each time one runs `civitdl` without default: `civitdl 123456 ./models --max-images 10`

### Set sorter
This sets the default sorter to use when `civitdl` is run without the option `-s` or `--sorter` 

#### What is a sorter?
- Sorter is a way to manage multiple downloaded models with ease. It separates each model downloaded into multiple directores.
- See [sorter doc](./sorter.md)

To set the default sorter to `tags` (note: one of the built in sorters):
- Shorthand: `civitconfig default -s tags`
- Longhand: `civitconfig default --sorter tags`

Set the sorter you want to use to organize your checkpoint, lora and other models' directories.
Do note that you can only set sorters that have been added to the config.

Example of setting sorter each time one runs `civitdl` without default: `civitdl 123456 ./models --sorter tags`


### Set api key



## Sorters

### List sorters

### Add a sorter

### Delete a sorter




## Aliases

### List aliases

### Add an alias

### Delete an alias



