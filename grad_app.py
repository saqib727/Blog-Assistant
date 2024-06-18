import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import google.generativeai as genai
import json
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import gradio as gr

load_dotenv()
client = AzureOpenAI(api_key=os.getenv('openai_api'), azure_endpoint="https://stats.openai.azure.com/", api_version="2024-02-01")

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
    }
)

def generate_blog(blog_title, keywords, num_words, num_images, custom_prompt=""):
    prompt_parts = [
        f"Generate a Comprehensive, Engaging blog post relevant to the given Title \"{blog_title}\" and keywords Include \"{keywords}\". Make sure to incorporate these keywords in the blog post and also add the subheadings where needed. The blog should be approximately {num_words} words in length, suitable for an online audience. Ensure the content is original and maintains a consistent tone throughout."
    ]

    response = model.generate_content(prompt_parts)

    # Image generation
    if not custom_prompt:
        custom_prompt = f"Create a blog post image for a blog titled '{blog_title}' which incorporates the following keywords: {keywords}. The image should visually represent the theme of the {blog_title} and {keywords}, using elements and symbols related to the keywords. It should be engaging, modern, and visually appealing, with a color scheme that complements the topic. Include relevant icons, illustrations, or abstract designs that reflect the essence of the keywords and make the blog title stand out prominently in the image."

    response_img = client.images.generate(
        model="Dalle3",
        prompt=custom_prompt,
        size="1024x1024",
        quality="standard",
        n=num_images
    )

    image_url = json.loads(response_img.model_dump_json())['data'][0]['url']

    return response.text, image_url

iface = gr.Interface(
    fn=generate_blog,
    inputs=["text", "text", "number", "number", "text"],
    outputs=["text", "image"],
    title="😎BlogCraft: Your Writing Assistant",
    description="Now you can craft perfect blogs with the help of AI. No Worries, you are at the right place!",
    sidebar=[
        gr.Textbox(label="Blog Title", placeholder="Enter Blog Title"),
        gr.Textbox(label="Keywords", placeholder="Keywords (comma-separated)"),
        gr.Slider(label="Num of words", min_value=250, max_value=1000, step=100),
        gr.Number(label="Number of Images", default=1, min_value=1, max_value=5, step=1),
        gr.Textbox(label="Optional Custom Prompt", placeholder="Optional Custom Prompt (leave blank to use default)")
    ],
    live=True
)

if __name__ == "__main__":
    iface.launch()
