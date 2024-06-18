import streamlit as st
import os
from dotenv import load_dotenv
from openai import AzureOpenAI
import google.generativeai as genai
import json
from streamlit_carousel import carousel
from google.generativeai.types import HarmCategory, HarmBlockThreshold



load_dotenv()
client=AzureOpenAI(api_key=os.getenv('openai_api'),azure_endpoint="https://stats.openai.azure.com/",api_version="2024-02-01")

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))


single_image=dict(
        title="",
        text="",
        img=""
        
        )

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
  safety_settings ={
      HarmCategory.HARM_CATEGORY_HATE_SPEECH:HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
      HarmCategory.HARM_CATEGORY_HARASSMENT:HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
      HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT:HarmBlockThreshold.BLOCK_NONE,
      HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:HarmBlockThreshold.BLOCK_NONE
      
  }
)


st.set_page_config(layout="wide")
#title of app
st.title("😎BlogCraft: Your Writing Assistant")

#subheader
st.subheader("Now you can craft perfect blogs with help of AI. No Worries, you are at right place!")

#sidebar for user input
with st.sidebar:
    st.title(" Blog Details")
    st.subheader("Enter Detail of Blog, you want to Generate")
    
    #blog title
    blog_title=st.text_input("Enter Blog Title")
    
    #keywword input
    keywords=st.text_area("Keywords (comma-seprated)")
    
    #number of words
    num_words=st.slider("Num of words",min_value=250,max_value=1000,step=100)
    
    #number of images
    num_images=st.number_input("Number of Images",min_value=1,max_value=5,step=1)
    
    # Optional custom prompt
    custom_prompt = st.text_area("Optional Custom Prompt (leave blank to use default)")
    
    #Sumbit button
    sumbit_button=st.button("Generate a Blog")
    
    #prompt parts
    prompt_parts=[f"Generate a Comprehensive, Engaging blog post relevant to the given Title \"{blog_title}\" and keywords Include \"{keywords}\". Make sure to incorporate these keywords in the blog post and also add the subheadings where needed. The blog should be approximately {num_words} words in length, suitable for an online audience. Ensure the content is original and maintains a consistent tone throughout."]
    
    
if sumbit_button:
    response=model.generate_content(prompt_parts)
    
      # Determine image generation prompt
    if custom_prompt:
        image_prompt = custom_prompt
    else:
        image_prompt = f"Create a blog post image for a blog titled '{blog_title}' which incorporates the following keywords: {keywords}. The image should visually represent the theme of the {blog_title} and {keywords}, using elements and symbols related to the keywords. It should be engaging, modern, and visually appealing, with a color scheme that complements the topic. Include relevant icons, illustrations, or abstract designs that reflect the essence of the keywords and make the blog title stand out prominently in the image."
    
    
    #📍 If you are using openai key then use following
    # images_gallery=[]
    # for i in range(num_images):
        
    #   response_img=client.images.generate(
    #          model="Dalle3",
    #          prompt=f"Create a blog post image for a blog titled '{blog_title}' which incorporates the following keywords: {keywords}. The image should visually represent the theme of the {blog_title} and {keywords}, using elements and symbols related to the keywords. It should be engaging, modern, and visually appealing, with a color scheme that complements the topic. Include relevant icons, illustrations, or abstract designs that reflect the essence of the keywords and make the blog title stand out prominently in the image.",
    #          size="1024x1024",
    #          quality="standard",
    #          n=num_images,)
    #     new_img=single_image.copy()
    #     new_img["title"]=f"Image{i+1}"
    #     new_img["text"]=f"{blog_title}"
    #     new_img["img"]=response_img.data[0].url
    #     images_gallery.append( new_img)
     
    # st.title("Your Blog Images:")   
    # carousel(items=images_gallery,width=1)

    #📍if you are using azure Openai then use following method!
    response_img=client.images.generate(
    model="Dalle3",
    prompt=f"Create a blog post image for a blog titled '{blog_title}' which incorporates the following keywords: {keywords}. The image should visually represent the theme of the {blog_title} and {keywords}, using elements and symbols related to the keywords. It should be engaging, modern, and visually appealing, with a color scheme that complements the topic. Include relevant icons, illustrations, or abstract designs that reflect the essence of the keywords and make the blog title stand out prominently in the image.",
    size="1024x1024",
    quality="standard",
    n=1, #dalle3 supports 1 image via openai but you can change as you want
    
    )
    
    image_url = json.loads(response_img.model_dump_json())['data'][0]['url']

    
    st.image(image_url,caption=
             "Generated Image")

    st.title("Your Blog Post")
    st.write(response.text)
    
