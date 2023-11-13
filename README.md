# civitdl (civitai-batch-download)

Uses CLI to batch download Stable Diffusion models from CivitAI, metadata (including description of model, author, base model, example prompts and etc.) and example images (default is 3) of checkpoint and lora models. One thing to note is that for **sfw models**, currently, the program is set to only **download sfw images**. Please note that there may be sfw models that are rated as nsfw by CivitAI (and vice versa).

## Description

There are two ways to batch download using this script (NOTE: batchdir has been removed):
- batchfile -> given the path to a comma separated text file (recommend .txt) that contains numbers or urls, it extracts all of the model ids from the file.
- batchstr -> specify a comma separated list of model id and/or url as arguments.

## Getting Started

### Dependencies
* Python3
* `requirements.txt`


### Installing

#### Install using PIP
* `pip3 install civitdl`
  * Use `pip install civitdl` if `pip3` is not found.

#### Build from source
* Download the project:
    * `git clone https://github.com/OwenTruong/civitdl.git`
* Inside terminal, run:
    * `cd civitdl`
* Then run:
    * `pip3 install -r requirements.txt`
        * Use `pip install -r requirements.txt ` if `pip3` is not found.
* Then run:
    * `make install`
* Now the module is available globally (example):
    * `civitdl batchstr 123456 ./`

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


### Executing program

#### batchfile 
* Args: 
    * `civitdl batchfile <txt file path> <destination model folder path>`
* Make sure everything is comma separated. txt files are recommended. 
* The comma separated list can be made out of model id, civitai.com/models or civitai.com/api/download/models urls. 
* If you need a specific version of a model, copy paste the url of the specific version in the txt file, and it would download the correct one.
  * Example of a url with a specific version id: `https://civitai.com/models/197273?modelVersionId=221861`
* Examples:
    * `civitdl batchfile ./custom/batchfile.txt ~/sorted-models --filter=tags`
    * `civitdl batchfile ./custom/batchfile.txt ~/sorted-models --custom-filter=./custom/filter.py`
* See [batchfile.txt](./custom/batchfile.txt) for example of a batchfile


#### batchstr
* Args: 
    * `civitdl batchstr <comma separated string of model id / url> <destination model folder path>`
* Accepts model id or urls separated by commas as an argument (accepts the same type of comma separated list as batchfile).
* Examples:
    * `civitdl batchstr "https://civitai.com/models/7808/easynegative, 79326" ~/Downloads/ComfyUI/models/loras`

#### Filters
* Beyond downloading models, it is possible to specify some filters, or rules, on how to organize the model folders when batch downloading multiple models.
* There are two built-in filters: tags and basic.
    * "tags" filters the models by the model type (i.e. if lora is trained on a 1.5 or 2.0 or SDXL base model) and tags associated with them on CivitAI. 
        * Example, if a model was trained on 1.5, and has tags - Anime, Character -, it would be filtered as so: 
          * Running script: `civitdl batchstr 123456 ~/models --filter="tags"`
            * `~/models/SD_1.5/Anime/Character/yaemiko-lora-nochekaiser/yaemiko-lora-nochekaiser-mid_123456-vid_134605.safetensors`
        * See [filters.py](./src/civitai_batch_download/filters.py?plain=1#L13) for available tags in the filter.
    * "basic" does not filter anything. It just downloads all of the models' data inside destination path folder specified in the arguments. It is also the default filter function used.
        * Example: 
            * Running script: `civitdl batchstr "123456" ~/models`
            * The model for 123456 is a Yae Miko character lora. The folder that includes the models folder, json and example images are stored in the following path: ~/models/yaemiko-lora-nochekaiser

#### Creating Custom Filters
* To create a custom filter, please create a python file with any filename. The only thing that is important is that the python file must contain a function called filter_model that has the following signatures: filter_model(Dict,Dict,str,str) -> str
* Please see [filter.py](./custom/filter.py) in custom folder for an example.
  * Other examples include the built in one [filters.py](./src/civitai_batch_download/filters.py).



## Help

Please create an issue if you encounter any problem, bugs or if you have a feature request.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
