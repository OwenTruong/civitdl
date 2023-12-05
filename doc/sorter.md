# Sorter
- In this page, we will go over what sorters are, how to use them, and how to create them.

<br/>

## Navigate
- [README Page](../README.md)
- [Alias Page](./alias.md)
- [API Key Page](./api_key.md)
- [Configuration Page](./configuration.md)
- [Sorter Page](./sorter.md)

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
- A sorter provides a way for users to automatically organize their downloaded models. A sorter is able to change the parent directory's name, and create subdirectores. More is explained below.

When one downloads a model with `civitdl`, a few other files are downloaded too - images and json metadata for the model. In order to make things organized, the downloaded model, images and jsons are grouped together and stored in a **parent directory**.

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
      | anythingV3_fp16-mid_66-vid_75.json
      | 517.jpeg
      | 525.jpeg
      | 526.jpeg
```

`basic` is the **default** sorter, and it is possible to change the parent directory name from `anythingv3_fp16` to any other name in a custom sorter.

<br/>

### Example of tag sorter creating subdirectories

With sorters, we can also customize the **subdirectories** of the parent directory. `tags` sorter offer a way to sort by SD version (SD1.5, SDXL, and etc.) and by tags.

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
          | hatsunemiku1-000006/
            | hatsunemiku1-000006-mid_80848-vid_85767.safetensors
            | hatsunemiku1-000006-mid_80848-vid_85767.json
            | 972495.jpeg
            | 972496.jpeg
            | 972497.jpeg
```



<br/>

## How to use or configure them?

### Using a sorter is really simple as shown in the previous section
- To use the default sorter, run without `-s` or `--sorter`, else run with the sorter option.
- `civitdl source1 source2 ... sourceN /path/to/the/root/dir -s tags`

### Configuring sorters
- To set a default sorter to use in `civitdl`, go to [set sorter section in configuration](./configuration.md#set-sorter)
- To list, add, and delete sorters, go to [sorters section in configuration](./configuration.md#sorters)

<br/>

## How to create a sorter?

1. Create a python file (name of file does not matter).
2. Create a function named exactly `sort_model`
   1. There should be four parameter:
      1. `(model_dict: Dict, version_dict: Dict, filename: str, root_path: str)`
   2. The return type should be a parent directory path string.
      1.  The path returned will be where the model will be downloaded
   3. Please also add some description, or doc string, to your custom sort_model as that would be printed out to the terminal when a user runs `civitconfig sorter`

Example image of running `civitconfig` to display description of sorters.
![Image of running civitconfig sorter and seeing the description of each sorter](./images/sorter/printing-out-available-sorters.png)

```python
def sort_model(model_dict: Dict, version_dict: Dict, filename: str, root_path: str):
    """This string here describes the following model."""
    return '/path/to/parent/directory/of/model'
```

Please see [sort.py](/custom/sort.py) in custom folder for an example.
- Also see [model_dict-example.json](/custom/model_dict-example.json) for an example of the values in model_dict.
- Also see [verson_dict-example.json](/custom/version_dict-example.json) for an example of the values in version_dict.


