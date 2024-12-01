# -- Application Used Libraries : 
import streamlit as st
import base64
import time
import cv2 as cv
import numpy as np

# -- Custom Application Styling :
st.markdown(
    """
    <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700&display=swap');

        .header-title {
            font-family: 'Poppins', sans-serif;
            font-size: 2.5rem;
            font-weight: bold;
            color: #ffffff; /* White */
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .header-subtitle {
            font-family: 'Poppins', sans-serif;
            font-size: 1.2rem;
            color: #ffd8ff; /* Light Violet */
        }
        .icon {
            width: 50px;
            height: 50px;
        }
        .icon-small {
            width: 42px;
            height: 42px;
        }
        .divider {
            border-top: 2px solid #6C63FF; /* Violet */
            margin: 20px 0;
        }
        .solid-border {
            border: 3px solid rgba(30, 10, 50);
            border-radius: 3px;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            background-color: rgba(23, 2, 37); /* Optional for better visibility */
            width: 100%;
            height: 100%;
            box-sizing: border-box;
        }
        .animated-border {
            background-color: rgba(255, 255, 255, 0);
            padding: 20px;
            border-radius: 3px;
            border: 3px solid transparent;
            border-image-slice: 1;
            animation: gradient-border 3s infinite;
            text-align: center;
            box-sizing: border-box;
            width: 100%;
            height: 100%;
        }
        @keyframes gradient-border {
            0% {
                border-image-source: linear-gradient(90deg, #ff00ff, #00ffff);
            }
            50% {
                border-image-source: linear-gradient(180deg, #00ffff, #ff00ff);
            }
            100% {
                border-image-source: linear-gradient(270deg, #ff00ff, #00ffff);
            }
        }
        .column-label {
            font-family: 'Poppins', sans-serif;
            font-weight: bold;
            font-size: 1.1rem;
            color: #6C63FF; /* Violet */
            margin-bottom: 10px;
        }
        .column-label2 {
            font-family: 'Poppins', sans-serif;
            font-weight: bold;
            font-size: 1.1rem;
            color: #ffffff; /* Violet */
            margin-bottom: 10px;
        }
        .column-container {
            margin-bottom: 20px; /* Add margin to bottom of each column */
        }
        /* Ensure equal padding and size for both columns */
        .col-image {
            padding: 20px;
            width: 100%;
            height: auto;
            object-fit: cover;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div class="header-title">
        <img src="https://img.icons8.com/ios-filled/100/6C63FF/artificial-intelligence.png" class="icon" alt="AI Icon">
        ImageLab Studio
    </div>
    <div class="header-subtitle">
        A space to explore and <span style="color: #ff00ff;">enhance images</span> through advanced processing techniques
    </div>
    <div class="divider"></div>
    """,
    unsafe_allow_html=True
)

# -- File Uploader 
uploaded_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
st.divider()

# -- Sidebar & Filters List 
filters = ['Gray Scale', 'Thresholding', 'Edge Detection', 'Morphological']
selected_filter = st.sidebar.selectbox(':violet[Please Select Filter To Apply !]', filters)

# -- Screen Divider :
col1, col2 = st.columns(2)

col1.markdown('<div class="column-label">Original Image Processing</div>', unsafe_allow_html=True)
if not uploaded_image :
    col1.markdown(
    f"""
    <div class="solid-border column-container">
        <img src="https://i.postimg.cc/vmybb3Tt/no-img-preview.png" class="icon-small" alt="Icon Preview">
    </div>
    """,
    unsafe_allow_html=True)
    col2.empty()

else:
    # -- Reading Uploaded Image :
    image_data = uploaded_image.read()
    np_img = np.frombuffer(image_data, np.uint8)
    # -- Decoding Uploaded Image :
    img = cv.imdecode(np_img, cv.IMREAD_COLOR)

    # -- Encoding Uploaded Orginal Image :
    _, buffer = cv.imencode('.jpg', img)
    encoded_org_image = base64.b64encode(buffer).decode("utf-8")   

    # -- Showing Image :
    col1.markdown(
        f"""
        <div class="animated-border column-container">
            <img src="data:image/jpeg;base64,{encoded_org_image}" 
                 style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
        </div>
        """,
        unsafe_allow_html=True
    )

    # -- Filters Setup : 
    if selected_filter == 'Gray Scale' :
        gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        # -- Encoding Manipulated Image :
        _, buffer = cv.imencode('.jpg', gray_scale_img)
        encoded_image = base64.b64encode(buffer).decode("utf-8")
        
        col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
        time.sleep(3)
        col2.markdown(
            f"""
            <div class="solid-border column-container">
                <img src="data:image/jpeg;base64,{encoded_image}" 
                    style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
            </div>
            """,
            unsafe_allow_html=True
        )

    elif selected_filter == 'Thresholding' :
        thresholing_value = st.sidebar.slider("Determine Thresholding Value", 0, 255, 127)
        gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
        _, thresholding_img = cv.threshold(gray_scale_img, thresholing_value, 255, cv.THRESH_BINARY)
        # -- Encoding Manipulated Image :
        _, buffer = cv.imencode('.jpg', thresholding_img)
        encoded_image = base64.b64encode(buffer).decode("utf-8")
        col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
        time.sleep(3)
        col2.markdown(
            f"""
            <div class="solid-border column-container">
                <img src="data:image/jpeg;base64,{encoded_image}" 
                    style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
            </div>
            """,
            unsafe_allow_html=True
        )

    elif selected_filter == 'Edge Detection' :
        edge_detection_selected = st.sidebar.radio("Select Edge Detection Type :", ["Canny", "Sobel"])
        if edge_detection_selected == 'Canny' :
            l_th = st.sidebar.slider("Lower Thresholding", 0, 127, 62)
            u_th = st.sidebar.slider("Upper Thresholding", 128, 255, 182)
            gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            canny = cv.Canny(gray_scale_img, l_th, u_th)
            # -- Encoding Manipulated Image :
            _, buffer = cv.imencode('.jpg', canny)
            encoded_image = base64.b64encode(buffer).decode("utf-8")
            col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
            time.sleep(3)
            col2.markdown(
                f"""
                <div class="solid-border column-container">
                    <img src="data:image/jpeg;base64,{encoded_image}" 
                        style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True
            )
        elif edge_detection_selected == 'Sobel' :
            gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            sobel_x = cv.Sobel(gray_scale_img, cv.CV_64F, 1, 0, ksize=3)  
            sobel_y = cv.Sobel(gray_scale_img, cv.CV_64F, 0, 1, ksize=3)  
            sobel_combined = cv.magnitude(sobel_x, sobel_y)
            # -- Encoding Manipulated Image :
            _, buffer = cv.imencode('.jpg', sobel_combined)
            encoded_image = base64.b64encode(buffer).decode("utf-8")
            col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
            time.sleep(3)
            col2.markdown(
                f"""
                <div class="solid-border column-container">
                    <img src="data:image/jpeg;base64,{encoded_image}" 
                        style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True
            )

    elif selected_filter == 'Morphological' :
        morphologica_selected = st.sidebar.radio("Morphological Operations Type :", ["Erosion", "Dilation", "Opening", "Closing", "Gradient", "Top Hat", "Black Hat"])

        if morphologica_selected == 'Erosion' :
            gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            kernel = np.ones((5, 5), np.uint8)
            erosion_img = cv.erode(gray_scale_img, kernel, iterations = 1)
            # -- Encoding Manipulated Image :
            _, buffer = cv.imencode('.jpg', erosion_img)
            encoded_image = base64.b64encode(buffer).decode("utf-8")
            col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
            time.sleep(3)
            col2.markdown(
                f"""
                <div class="solid-border column-container">
                    <img src="data:image/jpeg;base64,{encoded_image}" 
                        style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True
            )
        elif morphologica_selected == 'Dilation' :
            gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            kernel = np.ones((5, 5), np.uint8)
            erosion_img = cv.dilate(gray_scale_img, kernel, iterations = 1)
            # -- Encoding Manipulated Image :
            _, buffer = cv.imencode('.jpg', erosion_img)
            encoded_image = base64.b64encode(buffer).decode("utf-8")
            col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
            time.sleep(3)
            col2.markdown(
                f"""
                <div class="solid-border column-container">
                    <img src="data:image/jpeg;base64,{encoded_image}" 
                        style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True
            )
        elif morphologica_selected == 'Opening' :
            gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            kernel = np.ones((5, 5), np.uint8)
            erosion_img = cv.morphologyEx(gray_scale_img, cv.MORPH_OPEN, kernel)
            # -- Encoding Manipulated Image :
            _, buffer = cv.imencode('.jpg', erosion_img)
            encoded_image = base64.b64encode(buffer).decode("utf-8")
            col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
            time.sleep(3)
            col2.markdown(
                f"""
                <div class="solid-border column-container">
                    <img src="data:image/jpeg;base64,{encoded_image}" 
                        style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True
            )
        elif morphologica_selected == 'Closing' :
            gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            kernel = np.ones((5, 5), np.uint8)
            erosion_img = cv.morphologyEx(gray_scale_img, cv.MORPH_OPEN, kernel)
            # -- Encoding Manipulated Image :
            _, buffer = cv.imencode('.jpg', erosion_img)
            encoded_image = base64.b64encode(buffer).decode("utf-8")
            col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
            time.sleep(3)
            col2.markdown(
                f"""
                <div class="solid-border column-container">
                    <img src="data:image/jpeg;base64,{encoded_image}" 
                        style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True
            )
        elif morphologica_selected == 'Gradient' :
            gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            kernel = np.ones((5, 5), np.uint8)
            erosion_img = cv.morphologyEx(gray_scale_img, cv.MORPH_GRADIENT, kernel)
            # -- Encoding Manipulated Image :
            _, buffer = cv.imencode('.jpg', erosion_img)
            encoded_image = base64.b64encode(buffer).decode("utf-8")
            col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
            time.sleep(3)
            col2.markdown(
                f"""
                <div class="solid-border column-container">
                    <img src="data:image/jpeg;base64,{encoded_image}" 
                        style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True
            )
        elif morphologica_selected == 'Top Hat' :
            gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            kernel = np.ones((5, 5), np.uint8)
            erosion_img = cv.morphologyEx(gray_scale_img, cv.MORPH_TOPHAT, kernel)
            # -- Encoding Manipulated Image :
            _, buffer = cv.imencode('.jpg', erosion_img)
            encoded_image = base64.b64encode(buffer).decode("utf-8")
            col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
            time.sleep(3)
            col2.markdown(
                f"""
                <div class="solid-border column-container">
                    <img src="data:image/jpeg;base64,{encoded_image}" 
                        style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True
            )
        elif morphologica_selected == 'Black Hat' :
            gray_scale_img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
            kernel = np.ones((5, 5), np.uint8)
            erosion_img = cv.morphologyEx(gray_scale_img, cv.MORPH_BLACKHAT, kernel)
            # -- Encoding Manipulated Image :
            _, buffer = cv.imencode('.jpg', erosion_img)
            encoded_image = base64.b64encode(buffer).decode("utf-8")
            col2.markdown('<div class="column-label2">Manipulated Image</div>', unsafe_allow_html=True)
            time.sleep(3)
            col2.markdown(
                f"""
                <div class="solid-border column-container">
                    <img src="data:image/jpeg;base64,{encoded_image}" 
                        style="border-radius: 3px; width: 100%; height: auto; object-fit: cover;">
                </div>
                """,
                unsafe_allow_html=True
            )



