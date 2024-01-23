# civitdl
- The main command for downloading models in batches (includings its metadata, images and etc.)!

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
- [civitdl](#civitdl)
  - [Navigate](#navigate)
  - [Table Of Contents](#table-of-contents)
  - [Executing program in v2](#executing-program-in-v2)
    - [Sources](#sources)
      - [Note about Model ID vs Version ID of a model](#note-about-model-id-vs-version-id-of-a-model)
      - [batchfile](#batchfile)
  - [Options](#options)

<br/>

## Executing program in v2
- New Args:
  - `civitdl source1 source2 ... sourceN dst_root_directory`
- Example usage:
  - `civitdl 123456 ./batchfile.txt ./models`
- Run `civitdl --help` for help with arguments.

<br/>

### Sources
- Sources can be either one of the following
  - Model ID
  - `civitai.com/models` url
  - `civitai.com/api/downloads/models` url
  - `/path/to/batchfile.txt` batch file path
- Examples
  - `civitdl https://civitai.com/models/7808/easynegative 79326 ~/Downloads/ComfyUI/models/loras`

<br/>

#### Note about Model ID vs Version ID of a model
- If you need a specific version of a model, copy paste the url of the specific version in the txt file, and it would download the correct one.
  - Example of a url with a specific version id: `https://civitai.com/models/197273?modelVersionId=221861`
    - `197273` is the model id and `221861` is the version id.

<br/>

#### batchfile 
* Batchfile contain a comma separated list of sources.
* Examples:
    * `civitdl ./custom/batchfile.txt ~/sorted-models --sorter tags`
* See [batchfile.txt](./custom/batchfile.txt) for example of a batchfile

<br/>

## Options
- Run `civitdl --help` to check what options are available!
- To change the default for each options, see [ciitconfig doc](./civitconfig.md)

<br/>

`--sorter <sorter-name / path>` | `-s <sorter-name / path>`
- Specifies which sorter to use. The default uses the basic sorter.
- See [sorter doc](./doc/sorter.md) for more info.
- Example: `civitdl 123456 ./loras -s tags`

<br/>

`--max-images <number>` | `-i <number>`
- Specifies the max images to download for each model. The default is 3 images.
- Example: `civitdl 80848 ./loras -i 20`

<br/>

`--api-key` | `-k`
- Running with this option will prompt the user to type in their API key.
- See [api key doc](/doc/api_key.md) for help on how to get and use API key.
- Example: `civitdl 123456 ./loras -k`

<br/>

`--with-prompt` | `-p` | `--no-with-prompt`
- Running with the option will download an image's JSON prompt/metadata alongside the image. By default, civitdl downloads with prompt.
- Use `--no-with-prompt` to disable downloading images' JSON prompt/metadata.
- Example: `civitdl 80848 ./loras --with-prompt`

<br/>

`--limit-rate <byte-value>`
- Limit the number of bytes downloaded per second for models only. By default, no limit rate is applied.
  - Images are not included for now since the size per image is usually really small. Might be added later on in v2.
- Example: `civitdl 80848 ./loras --limit-rate 5M`
  - `1K` for 1 KB/s, `1M` for 1 MB/s, `1G` for 1 GB/s.

<br/>

`--retry-count <number>`
- Specifies the number of times to retry downloading the same model if it fails. Default is 3.
- Example: `civitdl 80848 ./loras --retry-count 10`

<br/>

`--pause-time <seconds>`
- Specifies how many seconds to pause between each model download. The default is 3 seconds.
- Example: `civitdl 123456 6 ./loras --pause-time 5`

<br/>

`--cache-mode <0 | 1 | 2>`
- Specifies the cache mode for each model. The default is `1`.
- Cache modes:
  - `0` - no cache mode
    -  Program will not add the current model's file path and hashes to cache.
    -  Program will not use stored cache to check if current model has already been downloaded before.
  - `1` - lax mode
    - Program will add the current model's file path and hashes to cache.
    - Program will check cache if the current model has been downloaded before.
      - If so, program will attemp to copy the model locally given path to the local model.
  - `2` - strict mode
    - Does what `1` does, but also validate the local model by creating SHA256 and BLAKE3 hashes for the previously downloaded model to make sure that the file path given by the cache is actually the correct model (and to make sure it has not been corrupted).
    - Warning that this will be slower than `1` because hashes will be computed for each check.
    - `NOT IMPLEMENTED YET`

<br/>

`--model-overwrite` | `--no-model-overwrite`
- Running with the option will download model even if it already exists at the destination path. By default, civitdl will not overwrite models.
- Use `--no-model-overwrite` to disable overwriting model that already exist at the destination path.
- Example: `civitdl 80848 ./loras --model-overwrite`

<br/>

`--verbose`
- Prints out traceback and other logs.

<br/>

`--version` | `-v`
- Get version of the program.
