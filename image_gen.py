import torch
import streamlit as st
from diffusers import StableDiffusionPipeline

def load_sd_model():
    pipe = StableDiffusionPipeline.from_pretrained(
        "stabilityai/sd-turbo",
        torch_dtype=torch.float32,
        safety_checker=None
    )
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = pipe.to(device)
    pipe.enable_attention_slicing()
    return pipe

pipe = load_sd_model()

def generate_image(topic: str):
    """
    Generate an educational image for a given topic
    """
    prompt = f"Simple educational diagram explaining {topic}, clean illustration style"
    result = pipe(
        prompt,
        num_inference_steps=5,
        guidance_scale=0.0
    )
    return result.images[0]
