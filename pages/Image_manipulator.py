import streamlit as st
from PIL import Image
import base64
import boto3
import io
import json
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", False)
DEFAULT_SEED = os.getenv("DEFAULT_SEED", 12345)
MAX_SEED = 4294967295
MODEL_ID = "stability.stable-diffusion-xl-v1"
NEGATIVE_PROMPTS = [
    "bad anatomy", "distorted", "blurry",
    "pixelated", "dull", "unclear",
    "poorly rendered",
    "poorly Rendered face",
    "poorly drawn face",
    "poor facial details",
    "poorly drawn hands",
    "poorly rendered hands",
    "low resolution",
    "Images cut out at the top, left, right, bottom.",
    "bad composition",
    "mutated body parts",
    "blurry image",
    "disfigured",
    "oversaturated",
    "bad anatomy",
    "deformed body features",
    "poorly rendered",
    "poor background details",
]
# Complete preset_style list: https://platform.stability.ai/docs/api-reference#tag/v1generation/operation/textToImage
STYLES_MAP = {
    "Photographic": "photographic",
    "Cinematic": "cinematic",
    "Comic Book": "comic-book",
    "Origami": "origami",
    "Analog Film": "analog-film",
    "Fantasy Art": "fantasy-art",
    "Line Art": "line-art",
    "Neon Punk": "neon-punk",
    "3D Model": "3d-model",
    "Digital Art": "digital-art",
    "Enhance": "enhance",
    "Pixel Art": "pixel-art",
    "Tile Texture": "tile-texture",
    "None": "None",
}

bedrock_runtime = boto3.client('bedrock-runtime')


@st.cache_data(show_spinner=False)
def gen_img_from_bedrock(image, prompt, style, seed=DEFAULT_SEED):
    # Convert the uploaded image to base64
    image_bytes = base64.b64encode(image.getvalue()).decode()
    
    body = json.dumps({
        # "image_prompts": [
        #     {
        #         "imageBase64": image_bytes
        #     }
        # ],
        "init_image": image_bytes,
        "text_prompts": [
            {
                "text": prompt
            }
        ],
        "cfg_scale": 10,
        "seed": seed,
        "steps": 50,
        "style_preset": style,
        "negative_prompts": NEGATIVE_PROMPTS
    })
    accept = "application/json"
    contentType = "application/json"
    response = bedrock_runtime.invoke_model(
        body=body, modelId=MODEL_ID, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())
    image_bytes = response_body.get("artifacts")[0].get("base64")
    image_data_one = base64.b64decode(image_bytes.encode())
    st.session_state['image_data_one'] = image_data_one
    return image_data_one


@st.cache_data
def get_image(image_data_one):
    return Image.open(io.BytesIO(image_data_one))


if __name__ == '__main__':
    # Create the page title
    st.set_page_config(
        page_title='Amazon Bedrock Stable Diffusion', page_icon='./bedrock.png')
    st.title('Stable Diffusion Image Generator with Amazon Bedrock')
    # Create a sidebar with text examples
    with st.sidebar:
        # Selectbox
        style_key = st.sidebar.selectbox(
            "Choose image style",
            STYLES_MAP.keys(),
            index=0)

        seed_input = st.sidebar.number_input(
            "Seed", value=DEFAULT_SEED, placeholder=DEFAULT_SEED, key="numeric")
        st.text ("Max Seed: " + str(MAX_SEED) )

        seed = seed_input

    # File upload for the input image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if not uploaded_file:
        st.warning("Please upload an image")
        st.stop()

    # Display the uploaded image
    st.image(uploaded_file)

    # Input prompt
    prompt = st.text_input('Input your prompt')
    if not prompt:
        st.warning("Please input a prompt")
        # Block the image generation if there is no input prompt
        st.stop()

    # Generate button
    if st.button("Generate", type="primary"):
        if uploaded_file and len(prompt) > 0:
            st.markdown(f"""
            This will show an image using **Stable Diffusion** with your desired prompt entered: {prompt}
            """)
            # Create a spinner to show the image is being generated
            with st.spinner('Generating image based on prompt'):
                if not DEBUG:
                    style = STYLES_MAP[style_key]
                    # Send request to Bedrock
                    image_data_one = gen_img_from_bedrock(
                        image=uploaded_file, prompt=prompt, style=style, seed=seed)
                    st.success('Generated stable diffusion image')

    # Display the generated image if available
    if st.session_state.get("image_data_one", None):
        image = get_image(st.session_state.image_data_one)
        st.image(image)

        # Download button for the generated image
        download_button = st.download_button(
            label="Download Image",
            data=st.session_state.image_data_one,
            file_name="generated_image.png",
            key="download_button"
        )

    if DEBUG:
        st.write(st.session_state)
