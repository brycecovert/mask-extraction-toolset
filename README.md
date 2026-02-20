# Mask Extraction LoRA

A ComfyUI-based toolchain for generating high-quality alpha masks from images using [Qwen2.5-VL-Image-Edit-2511](https://huggingface.co/Qwen/Qwen-Image-Edit-2511).

## Problem

Existing mask generation tools have limitations:
- **SAM** emits binary yes/no masks, not suitable for compositing
- **Qwen Image Layered** outputs relatively small layers

This toolchain solves that by generating clean, high-resolution grayscale alpha masks suitable for professional compositing work.

## Example Results

| Input | Output |
|-------|--------|
| ![](https://huggingface.co/Notid/qwen-edit-2511-mask-extraction/resolve/main/images/img_00002_.png) | Prompt: "Create a black and white alpha mask for the object with a red outline" |
| ![](https://huggingface.co/Notid/qwen-edit-2511-mask-extraction/resolve/main/images/img_00003_.png) | Prompt: "Create a black and white alpha mask for the woman, excluding the pinecone" |
| ![](https://huggingface.co/Notid/qwen-edit-2511-mask-extraction/resolve/main/images/img_00012_.png) | Prompt: "Create a black and white alpha mask for the tree and its foliage" |

## Usage

### LoRA

Download the LoRA from HuggingFace: [Notid/qwen-edit-2511-mask-extraction](https://huggingface.co/Notid/qwen-edit-2511-mask-extraction)

**Trigger word:** `Create a black and white alpha mask of the ...`

Example prompts:
- `Create a black and white alpha mask of the bucket in the bottom left`
- `Create a black and white alpha mask of the object with the red outline`
- `Create a black and white alpha mask of the hat, excluding the man's head`

### Dataset

The training dataset is available on HuggingFace: [Notid/mask_pairs](https://huggingface.co/datasets/Notid/mask_pairs/viewer/default/train?row=99)

## Toolchain Contents

- **ComfyUI workflow** - Generate high-quality alpha masks using text descriptions or bounding boxes
- **ComfyUI workflow** - Generate sample images for dataset creation
- **Mask comparison tool** - Review and edit generated mask pairs for refinement

## Potential Improvements

- **Human samples** - The current dataset has very few samples of humans. Adding more high-quality human portrait pairs would improve mask quality for people.
- **Fine detail (hair)** - More training samples with complex hair details would likely improve the model's ability to generate clean edges around hair and fine strands.

## License

This project is provided as-is for mask extraction workflows.
