import streamlit as st
from PIL import Image
import base64
from io import BytesIO
import time
import cv2
import os
import numpy as np
import text_slicer as slicer
import converter

# Page configuration
st.set_page_config(
    page_title="InkMe - Text to Handwriting Converter",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E3A59;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
    }
    .sub-header {
        text-align: center;
        color: #6C7B95;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .demo-text {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .handwriting-preview {
        background-color: #fff;
        border: 2px dashed #ddd;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        min-height: 200px;
        font-family: 'Courier New', monospace;
        line-height: 1.8;
        background-image: 
            repeating-linear-gradient(
                transparent,
                transparent 24px,
                #e0e0e0 24px,
                #e0e0e0 26px
            );
    }
    .download-section {
        background-color: #f1f3f4;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">InkMe</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform your digital text into beautiful, personalized handwritten documents</p>', unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([1, 1])

png_file = None
png_files = []
writing_style = None

with col1:
    st.markdown("### Upload a PNG of Your Handwriting")
    st.markdown("It needs to be a grid of 6 rows x 10 columns drawn on a blank white paper.")
    st.markdown("The top half must contain capital letters from A-Z, with the last 4 grid cells being blank.")
    st.markdown("The bottom half must contain lowercase letters from a-z, with the last 4 grid cells being blank.")
    st.markdown("There should be no spaces between each stroke of a letter.")
    png_files = st.file_uploader("Upload a PNG", type = ["png", "jpg"], accept_multiple_files=True)
    if (len(png_files) > 0):
        if writing_style is None:
            writing_style = png_files[0]
        png_file = writing_style
    else:
        png_file = None
    if (png_file is not None):
        slicer.slice(png_file.name)

    st.markdown("### Input Your Text")
    
    user_text = ""
    
    user_text = st.text_area(
        "Enter your text here:",
        height=200,
        placeholder="",
        help="Enter the text you want to convert to handwriting",
        key="input1"
    )

    # Handwriting style options
    st.markdown("### Customize Your Handwriting")
    
    handwritings = []
    for f in png_files:
        handwritings.append(f.name)
    handwriting = st.selectbox(
        "Choose handwriting style:",
        handwritings
    )
    writing_style = png_files[handwritings.index(handwriting)]
    png_file = writing_style
    if (png_file is not None):
        slicer.slice(png_file.name)
    
    col_style1, col_style2 = st.columns(2)
    with col_style1:
        pen_color = st.selectbox(
            "Pen color:",
            ["Blue", "Black", "Dark Blue", "Purple", "Green"]
        )
        
        paper_type = st.selectbox(
            "Paper type:",
            ["Lined", "Plain", "Graph", "Vintage"]
        )

with col2:
    if png_file is not None:
        st.markdown("### Handwriting Preview:")
        image = Image.open(png_file)
        image = slicer.correct_image_orientation(image)
        st.image(image, use_container_width=True)
    if (len(user_text) > 0):
        converter.text_to_handwriting(user_text)
        st.markdown("### Output Preview:")
        op_image = Image.open("output_sentence.png")
        if op_image is not None:
            st.image(op_image, use_container_width=True)
          