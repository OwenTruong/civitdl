# civitai-batch-download

Uses CLI to batch download models, metadatas (including description of model, author, base model, example prompts and etc.) and example images of checkpoint and lora models.

## Description

There are three ways to batch download using this script:
- batchdir -> given the path to a folder, it finds all of the safetensors file and extract the model id from the filename if it exists.
    - ex: some_kind_of_model-123456.safetensors, model id is 123456
- batchfile -> given the path to a comma separated text file (recommend .txt) that contains numbers or urls, it extracts all of the model ids from the file.
- batchstr -> specify a comma separated list of model id and/or url as arguments.

## Getting Started

### Dependencies
1. Requires Python 3.10 or later.
2. Requires request package. Run "pip3 install -r requirements.txt" if request package is not installed.


### Installing
* Git clone project

### Executing program

#### batchdir
* Args: ./main.py batchdir \<source model folder path> \<destination model folder path>
* Make sure model id is the last number in the text file. 
    * Example, some times, model makers like to include their epoch count in their safetensors filename so make sure that is not the last number. Suppose the model id is 123456: amazing_lora-00020-123456.safetensors.
* Examples:
    * ./main.py batchdir ~/loras ~/sorted-loras
        * Will get the model id from all of your safetensors' filename in ~/loras recursively
    * ./main.py batchdir ./stable-diffusion-webui/models/Lora/unfiltered ./stable-diffusion-webui/models/Lora/filtered --filter=tags


#### batchfile 
* Args: ./main.py batchfile \<txt file path> \<destination model folder path>
* Make sure everything is comma separated. txt files are recommended. 
* The list can be made out of model id or civitai.com urls. 
* If you need a specific version of a model, copy paste the url of the specific version in the txt file, and it would download the correct one.
* Examples:
    * ./main.py batchfile ./custom/batchfile.txt ~/sorted-models --filter=tags
    * ./main.py batchfile ./custom/batchfile.txt ~/sorted-models --custom-filter=./custom/filter.py
* See [batchfile.txt](./custom/batchfile.txt) for example of a batchfile


#### batchstr
* Args: ./main.py batchstr \<comma separated string of model id / url> \<destination model folder path>
* Accepts model id or urls separated by commas as an argument.
* Examples:
    * ./main.py batchstr "https://civitai.com/models/7808/easynegative, 79326" ~/Downloads/ComfyUI/models/loras

#### Filters
* Beyond downloading models, it is possible to specify some filters, or rules, on how to organize the model folders when batch downloading multiple models.
* There are two built-in filters: tags and basic.
    * "tags" filters the models by the model type (i.e. if lora is trained on a 1.5 or 2.0 or SDXL base model) and tags associated with them on CivitAI. 
        * Example, if a model was trained on 1.5, and has tags - Anime, Character -, it would be filtered as so: /SD_1.5/Anime/Character/yaemiko-lora-nochekaiser/yaemiko-lora-nochekaiser-123456.safetensors
        * See [filters.py](./lib/filters.py?plain=1#L13) for available tags in the filter.
    * "basic" does not filter anything. It just downloads all of the models' data inside destination path folder specified in the arguments. It is also the default filter function used.
        * Example: 
            * Running script: ./main.py batchstr "123456" ~/models
            * The model for 123456 is a Yae Miko character lora by coincidence. The folder that includes the models folder, json and example images are stored in the following path: ~/models/yaemiko-lora-nochekaiser

#### Creating Custom Filters
* To create a custom filter, please create a python file with any filename. The only thing that is important is that the python file must contain a function called filter_model that has the following signatures: filter_model(Dict,Dict,str,str) -> str
* Please see [filter.py](./custom/filter.py) in custom folder for an example.


## Help

Please create an issue if you encounter any problem, bugs or if you have a feature request.

## TODO
* Save bandwidth by enabling the option to move safetensors file instead of downloading a fresh new copy in batchdir.
* Turn it into a python package so it can be installed globally.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
