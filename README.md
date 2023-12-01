# civitdl v2.0 (civitai-batch-download)

**Note v2 has some changes regarding the cli args of the program. Please read the README below or run `civitdl --help` for the new arguments.

Uses CLI to batch download Stable Diffusion models from CivitAI, metadata (including description of model, author, base model, example prompts and etc.) and example images (default is 3) of checkpoint and lora models. One thing to note is that for **sfw models**, currently, the program is set to only **download sfw images**. Please note that there may be sfw models that are rated as nsfw by CivitAI (and vice versa).

## Description

There are two ways to batch download using this script:
- batchfile -> given the path to a comma separated text file that contains numbers or urls, it extracts all of the model ids from the file.
- batchstr -> specify a comma separated list of model id and/or url as arguments.

## Getting Started

### Dependencies
* Python3
* `requirements.txt`


### Installing

#### Install using PIP
* `pip3 install civitdl`
  * Use `pip install civitdl` if `pip3` is not found.
  * Run `civitdl --help` for args and options.

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
    * `civitdl 123456 ./`

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

#### Note in v2, it is now possible to use both batchfile and batchstr without specifying batchfile or batchstr as an argument.
- New Args:
  - `civitdl source1 source2 ... sourceN dst_root_directory`
- Example:
  - `civitdl 123456 batchfile ./models`

#### batchfile 
* Make sure everything is comma separated. txt files are recommended. 
* The comma separated list can be made out of model id, civitai.com/models or civitai.com/api/download/models urls. 
* If you need a specific version of a model, copy paste the url of the specific version in the txt file, and it would download the correct one.
  * Example of a url with a specific version id: `https://civitai.com/models/197273?modelVersionId=221861`
* Examples:
    * `civitdl ./custom/batchfile.txt ~/sorted-models --sorter=tags`
    * `civitdl ./custom/batchfile.txt ~/sorted-models --sorter=./custom/sort.py`
* See [batchfile.txt](./custom/batchfile.txt) for example of a batchfile


#### batchstr
* Accepts model id or urls separated by commas as an argument (accepts the same type of comma separated list as batchfile).
* Examples:
    * `civitdl https://civitai.com/models/7808/easynegative 79326 ~/Downloads/ComfyUI/models/loras`

#### Sorters (previously called filters)
* Beyond downloading models, it is possible to specify some sorters, or rules, on how to organize the model folders when batch downloading multiple models.
* There are two built-in sorters: tags and basic.
    * "tags" sorters the models by the model type (i.e. if lora is trained on a 1.5 or 2.0 or SDXL base model) and tags associated with them on CivitAI. 
        * Example, if a model was trained on 1.5, and has tags - Anime, Character -, it would be sorted as so: 
          * Running script: `civitdl 123456 ~/models -s "tags"`
            * `~/models/SD_1.5/Anime/Character/yaemiko-lora-nochekaiser/yaemiko-lora-nochekaiser-mid_123456-vid_134605.safetensors`
        * See [tags.py](./src/civitdl/config/sorter/tags.py) for available tags in the sorter.
    * "basic" does not sort anything. It just downloads all of the models' data inside destination path folder specified in the arguments. It is also the default sorter function used.
        * Example: 
            * Running script: `civitdl 123456 ~/models`
            * The model for 123456 is a Yae Miko character lora. The folder that includes the models folder, json and example images are stored in the following path: ~/models/yaemiko-lora-nochekaiser

#### Creating Custom Sorters
* To create a custom sorter, please create a python file with any filename. The only thing that is important is that the python file must contain a function called sort_model that has the following signatures: sort_model(Dict,Dict,str,str) -> str
* Please see [sort.py](./custom/sort.py) in custom folder for an example.
* Example of running custom sorter:
  * `civitdl 123456 ~/models -s ./custom/sort.py`


## Help

Please create an issue if you encounter any problem, bugs or if you have a feature request.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
