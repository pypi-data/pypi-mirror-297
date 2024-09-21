from PIL import Image
from controlnet_aux import OpenposeDetector

from diffusers import StableDiffusionControlNetPipeline, UniPCMultistepScheduler
import torch
from diffusers.utils import load_image
from diffusers import ControlNetModel
openpose = OpenposeDetector.from_pretrained('lllyasviel/ControlNet')
image = load_image("/Users/sebastianperalta/simply/corp/.envs/corp/lib/python3.12/site-packages/mbodied/resources/color_image.png")
image = openpose(image)
controlnet = ControlNetModel.from_pretrained('lllyasviel/sd-controlnet-openpose', torch_dtype=torch.float16)
pipe = StableDiffusionControlNetPipeline.from_pretrained('runwayml/stable-diffusion-v1-5', controlnet=controlnet, safety_checker=None, torch_dtype=torch.float16)
pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_xformers_memory_efficient_attention()
pipe.enable_model_cpu_offload()
result_image = pipe('6d pose estimation', image, num_inference_steps=20).images[0]
result_image.save('output_image.png')


# import json
# import os
# from PIL import Image as PILModule
# from embdata.sense import Image

#if u need proxy
#os.environ['http_proxy'] = "http://127.0.0.1:1080"
#os.environ['https_proxy'] = "http://127.0.0.1:1080"

# img = Image("/Users/sebastianperalta/simply/corp/.envs/corp/lib/python3.12/site-packages/mbodied/resources/color_image.png", encoding="jpeg").pil

# from dwpose import DwposeDetector
# model = DwposeDetector.from_pretrained_default()
# imgOut,j,source = model(img,
#     include_hand=True,
#     include_face=False,
#     include_body=True,
#     image_and_json=True,
#     detect_resolution=512)

# #openpose json
# f = open("keypoints.json","w")
# f.write(json.dumps(j))
# f.close()

# #openpose image
# imgOut.save("openpose.jpg")

# #detected resolution image
# source.save("source.jpg")

# del model