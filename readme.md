# BlogCraft: Your Writing Assistant 🖊️

 BlogCraft is a web application built with Streamlit that leverages AI to assist in crafting blog posts effortlessly.

# Overview
BlogCraft integrates several powerful AI models to generate both written content and visually appealing blog post images based on user inputs.

# Features

- AI-powered Blog Generation: Generate comprehensive blog posts based on user-provided titles, keywords, and desired word count.
- Customizable Image Creation: Automatically create blog post images that complement the content and engage readers.
- User-friendly Interface: Simple sidebar inputs for blog details such as title, keywords, and desired content length.

# Getting Started

To run BlogCraft locally, follow these steps:

1) Clone the repository:
```
git clone https://github.com/saqib727/Blog-assistant
cd blogcraft
```
2) Setup environment variables:
- Create a .env file in the root directory.
- Add the following keys:
```
openai_api=YOUR_OPENAI_API_KEY
GEMINI_API_KEY=YOUR_GEMINI_API_KEY

```

3) Run the application:
```
streamlit run app.py
```
4) use BlogCraft:
- Enter your blog title, keywords, and desired word count in the sidebar.
- Optionally, provide a custom prompt for more tailored content.
- Click on "Generate a Blog" to see the AI-generated blog post and accompanying image.

# Technologies Used
- Streamlit: Frontend framework for building interactive web applications.
- OpenAI's Gemini: API for generating textual content with advanced AI models.
- Azure OpenAI: API for generating blog post images using AI models.
