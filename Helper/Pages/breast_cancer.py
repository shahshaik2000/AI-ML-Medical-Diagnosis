import streamlit as st
import pickle
import numpy as np
from Helper.basic_diagnosis import get_prescription

def run():
    st.title("🩸 Breast Cancer Prediction")
    # Load the pre-trained model
    try:
        with open("./Models/breast_cancer.pkl", 'rb') as model_file:
            model = pickle.load(model_file)
    except FileNotFoundError:
        st.error("Model file not found. Please check the file path.")
        st.stop()
    except Exception as e:
        st.error(f"❌ An error occurred while loading the model: {e}")
        st.stop()
    
    st.write("This page is dedicated to breast cancer prediction.")

    

   # User Input Form for heart disease prediction
    texture_mean = st.number_input("Texture Mean", min_value=0.0)
    smoothness_mean = st.number_input("Smoothness Mean", min_value=0.0)
    compactness_mean = st.number_input("Compactness Mean", min_value=0.0)
    concave_points_mean = st.number_input("Concave Points Mean", min_value=0.0)
    symmetry_mean = st.number_input("Symmetry Mean", min_value=0.0)
    fractal_dimension_mean = st.number_input("Fractal Dimension Mean", min_value=0.0)

    texture_se = st.number_input("Texture Standard Error", min_value=0.0)
    area_se = st.number_input("Area Standard Error", min_value=0.0)
    smoothness_se = st.number_input("Smoothness Standard Error", min_value=0.0)
    compactness_se = st.number_input("Compactness Standard Error", min_value=0.0)
    concavity_se = st.number_input("Concavity Standard Error", min_value=0.0)
    concave_points_se = st.number_input("Concave Points Standard Error", min_value=0.0)

    symmetry_se = st.number_input("Symmetry Standard Error", min_value=0.0)
    fractal_dimension_se = st.number_input("Fractal Dimension Standard Error", min_value=0.0)

    texture_worst = st.number_input("Texture Worst", min_value=0.0)
    area_worst = st.number_input("Area Worst", min_value=0.0)
    smoothness_worst = st.number_input("Smoothness Worst", min_value=0.0)
    compactness_worst = st.number_input("Compactness Worst", min_value=0.0)
    concavity_worst = st.number_input("Concavity Worst", min_value=0.0)
    concave_points_worst = st.number_input("Concave Points Worst", min_value=0.0)

    symmetry_worst = st.number_input("Symmetry Worst", min_value=0.0)
    fractal_dimension_worst = st.number_input("Fractal Dimension Worst", min_value=0.0)

    # Submit button for the form
    if st.button("🔍 Predict"):
        # Prepare input data for prediction
        input_data = np.array([[texture_mean, smoothness_mean, compactness_mean, 
                                concave_points_mean, symmetry_mean, fractal_dimension_mean,
                                texture_se, area_se, smoothness_se, compactness_se, 
                                concavity_se, concave_points_se, symmetry_se, 
                                fractal_dimension_se, texture_worst, area_worst, 
                                smoothness_worst, compactness_worst, concavity_worst, 
                                concave_points_worst, symmetry_worst, fractal_dimension_worst]])
        # Make prediction using the loaded model
        prediction = model.predict(input_data)
        
        # Store diagnosis in session state (specific to breast cancer page)
        if prediction[0] == 0:
            st.session_state.breast_cancer_diagnosis = "Benign Tumor"
            st.success("Benign Tumor - No immediate concern, but follow regular checkups.")
        else:
            st.session_state.breast_cancer_diagnosis = "Malignant Tumor"
            st.error("Malignant Tumor - Requires medical attention. Consult a specialist.")

        # Reset prescription when a new diagnosis is made
        st.session_state.breast_cancer_prescription = None

    # Display Diagnosis and Prescription Recommendations if available
    if "breast_cancer_diagnosis" in st.session_state:
        st.markdown("---")
        st.info(f"**Diagnosis:** {st.session_state.breast_cancer_diagnosis}")
        # Generate prescription recommendations based on diagnosis
        if st.button("📜 Generate Prescription Recommendations"):
            st.session_state.breast_cancer_prescription = get_prescription(st.session_state.breast_cancer_diagnosis)

        if "breast_cancer_prescription" in st.session_state and st.session_state.breast_cancer_prescription:
            st.markdown("---")
            st.subheader("💊 Treatment Recommendations")
            st.success("**Prescription Guidelines:**")
            st.write(st.session_state.breast_cancer_prescription)
            st.markdown("""
                **📌 Important Notes:**
                - Consult an oncologist for a detailed evaluation.
                - Further tests like biopsy, MRI, or PET scan may be required.
                - Treatment may include surgery, chemotherapy, or radiation therapy.
            """)
    # Navigation button to return to the main page
    if st.button("← Back to Diagnosis"):
        st.session_state.page = "diagnosis"
        st.rerun()
