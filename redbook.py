import streamlit as st
import requests
from PIL import Image
import io
from streamlit_folium import st_folium
import folium
import random

# Configuration
API_URL = "http://localhost:8000/classify"  # Update if your FastAPI is hosted elsewhere

# CLIP Classes
CLIP_CLASSES = [
"Орешниковая соня",
"Водяная полевка",
"Заяц",
"Обыкновенный ёж",
"Обыкновенная водяная землеройка",
"Водяная летучая мышь",
"Двухцветная кожистая",
"Лесная летучая мышь",
"Брандтова летучая мышь",
"Бурый ушастик",
"Рыжая вечерница",
"Горностай",
"Ласка",
"Хорек",
"Барсук",
"Каменная куница",
"Лесная куница",
"Гнездо"
]

# Initialize session state for mock statistics
if 'classification_history' not in st.session_state:
    st.session_state.classification_history = []

# App Title
st.title("CLIP Image Classifier")

# Tabs for Navigation
tabs = st.tabs(["Classify Image", "Statistics"])

with tabs[0]:
    st.header("Upload and Classify Image")
    
    # Image Upload
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        
        # Prepare the image for API
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        buffered.seek(0)
        
        # Send image to FastAPI for classification
        with st.spinner('Classifying...'):
            try:
                files = {'file': (uploaded_file.name, buffered, uploaded_file.type)}
                response = requests.post(API_URL, files=files)
                response.raise_for_status()
                classification_result = response.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Error: {e}")
                classification_result = None
        
        if classification_result:
            st.success("Classification Result:")
            st.json(classification_result)
            
            # Update classification history
            st.session_state.classification_history.append(classification_result)
            
            # Display Map with Marker (Mock: Moscow Coordinates)
            st.header("Location of the Image")
            moscow_coords = [55.7558, 37.6176]
            folium_map = folium.Map(location=moscow_coords, zoom_start=10)
            folium.Marker(
                location=moscow_coords,
                popup="Image Location: Moscow",
                tooltip="Moscow"
            ).add_to(folium_map)
            
            st_folium(folium_map, width=700)
            
with tabs[1]:
    st.header("Classification Statistics")
    
    if st.session_state.classification_history:
        st.subheader("Previous Classification Results")
        # Display as a table
        for idx, result in enumerate(st.session_state.classification_history, 1):
            st.write(f"**Result {idx}:**")
            st.json(result)
        
        st.subheader("Class Distribution")
        # Calculate distribution
        distribution = {cls: 0 for cls in CLIP_CLASSES}
        for result in st.session_state.classification_history:
            pred_class = result.get("predicted_class")
            if pred_class in distribution:
                distribution[pred_class] += 1
        
        # Display as bar chart
        print(distribution)
        st.bar_chart(distribution)
    else:
        st.info("No classification history available.")

# Mock Data for Initial Statistics (Optional)
# You can populate st.session_state.classification_history with mock data here if needed
# Example:
# if not st.session_state.classification_history:
#     mock_results = [
#         {"predicted_class": random.choice(CLIP_CLASSES), "confidence": random.uniform(0.5, 1.0)},
#         {"predicted_class": random.choice(CLIP_CLASSES), "confidence": random.uniform(0.5, 1.0)}
#     ]
#     st.session_state.classification_history.extend(mock_results)
