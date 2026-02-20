# Mask extractor

Problem: There are many good resources for simple mask generation, SAM, Qwen Image Layered, but these each have downsides. SAM works by emitting binary yes/no masks, and Qwen Image Layered outputs relatively small layers. This toolchain was created to build a tool to solve that problem.

A picture's worth a thousand words
(picture of SAM vs LoRA outputs)

If you would like to use this LoRA, download the weights from huggingface and use the example workflow (embedded in png)

Contents of this repository:
* A ComfyUI workflow to generate high quality alpha masks using description (create a mask of the person in green) or bounding boxes (create a mask of the item in the red outline)
* A ComfyUI workflow to generate sample images from a much smaller LoRA
* A tool for editing the resulting dataset from above

You can use this toolchain to generate and review more samples for further refinement
