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

<br/>

## How to create a sorter?
