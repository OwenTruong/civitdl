# Sorter
- In this page, we will go over what sorters are, how to use them, and how to create them.

<br/>

## Navigate
- [README Page](/README.md)
- [Alias Page](/doc/alias.md)
- [API Key Page](/doc/api_key.md)
- [Configuration Page](/doc/configuration.md)
- [Sorter Page](/doc/sorter.md)


<br/>

## Table Of Contents
- [Sorter](#sorter)
  - [Navigate](#navigate)
  - [Table Of Contents](#table-of-contents)
  - [What is a sorter?](#what-is-a-sorter)
    - [Example of basic sorter](#example-of-basic-sorter)
    - [Example of tag sorter creating subdirectories](#example-of-tag-sorter-creating-subdirectories)
  - [How to use or configure them?](#how-to-use-or-configure-them)
    - [Using a sorter is really simple as shown in the previous section](#using-a-sorter-is-really-simple-as-shown-in-the-previous-section)
    - [Configuring sorters](#configuring-sorters)
  - [How to create a sorter?](#how-to-create-a-sorter)

<br/>

## What is a sorter?
- A sorter provides a way for users to automatically organize their downloaded models. A sorter is able to change a parent directory's name, and create subdirectores. More is explained below.

When one downloads a model with `civitdl`, the model's example images and json metadata are also downloaded.
- A parent directory describes the parent directory a model, metadata or images are download to.

The reason we want to download the images and metadatas too are because it helps to have a reference of what a model does locally, plus on the off chance that the model is pulled off of civitai one day, we can still refer to the model locally.

<br/>

### Example of basic sorter 

For example, suppose we download Anything v3 
using `basic` sorter in root directory "`Stable-diffusion`" of Auto1111 
(for some reason, ckpt dir in Auto1111 is called Stable-diffusion...): 

`civitdl 66 ./stable-diffusion-webui/models/Stable-diffusion -s basic`

--- RESULT ---
```
stable-diffusion-webui/
| models/
  | Stable-diffusion/
    | anythingv3_fp16/
      | anythingV3_fp16-mid_66-vid_75.ckpt
      | extra_data-vid_75/
        | model_dict-mid_66-vid_75.json
        | 517.jpeg
        | 525.jpeg
        | 526.jpeg
```

`basic` is the **default** sorter, and it is possible to change the parent directory name from `anythingv3_fp16` to any other name in a **custom sorter**.
- It is also possible to change the directory path of metadata and images in a **custom sorter**

`basic` does not really do anything besides creating a parent directory right under root directory (or in our case here, the ckpt directory).

**NOTE: mid_66-vid_75 just means the model id is 66 and the version id is 75. I will move this note to a more appropriate spot later.**

<br/>

### Example of tag sorter creating subdirectories

With sorters, we can also customize the **subdirectories** of the parent directory. `tags` sorter offer a way to sort by SD version (SD1.5, SDXL, and etc.) and by civitai tags parsed from the metadata.

For example, suppose we download a Hatsune Miku lora with model id 80848
using `tags` sorter in a root directory "`Lora`" of Auto1111:

`civitdl 80848 ./stable-diffusion-webui/models/Lora -s tags`

--- RESULT ---
```
stable-diffusion-webui/
| models/
  | Lora/
    | SD_1.5/
      | anime/
        | character/
          | "Hatsune Miku 初音ミク | 23 Outfits | Character Lora 9289"/
            | hatsunemiku1-000006-mid_80848-vid_85767.safetensors
            | extra_data-vid_85767/
              | model_dict-mid_80848-vid_85767.json
              | 972495.jpeg
              | 972496.jpeg
              | 972497.jpeg
```



<br/>

## How to use or configure them?

### Using a sorter is really simple as shown in the previous section
- To use the default sorter, run without `-s` or `--sorter`, else run with the sorter option.
  - `civitdl source1 ... sourceN /path/to/root/dir -s tags`
- To run a sorter from filepath, just provide the path to the sorter python file.
  - `civitdl source1 ... sourceN /path/to/root/dir -s /path/to/sorter.py`



### Configuring sorters
- To set a default sorter to use in `civitdl`, go to [set sorter section in configuration](./configuration.md#set-sorter)
- To list, add, and delete sorters, go to [sorters section in configuration](./configuration.md#sorters)

<br/>

## How to create a sorter?

1. Create a python file (name of file does not matter).
2. Create a function named exactly `sort_model`
   1. There should be four parameter:
      1. `(model_dict: Dict, version_dict: Dict, filename: str, root_path: str)`
   2. The return type should be a list of exactly three string paths.
      1. Model Parent Directory Path string
      2. Metadata Parent Directory Path string
      3. Images Parent Directory Path string
   3. Please also add some description, or doc string, to your custom sort_model as that would be printed out to the terminal when a user runs `civitconfig sorter`

Example image of running `civitconfig` to display description of sorters.
![Image of running civitconfig sorter and seeing the description of each sorter](./images/sorter/printing-out-available-sorters.png)

```python
def sort_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """This string here describes the following model."""
    model_dir_path = '/path/to/model/parent/dir'
    metadata_dir_path = '/path/to/metadata/parent/dir'
    image_dir_path = '/path/to/image/parent/dir'
    return [
      model_dir_path, # Parent dir of where the downloaded model should be in
      metadata_dir_path, # Parent dir of where the JSON metadata should be in
      image_dir_path # Parent dir of where the images should be in
    ]
```

Please see [sort.py](/custom/sort.py) in custom folder for an example.
- Also see [model_dict-example.json](/custom/model_dict-example.json) for an example of the values in model_dict.
- Also see [verson_dict-example.json](/custom/version_dict-example.json) for an example of the values in version_dict.


