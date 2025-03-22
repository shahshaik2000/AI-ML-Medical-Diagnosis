import streamlit as st
import pickle
import numpy as np
from Helper.basic_diagnosis import get_prescription

def run():
    # Load the pre-trained model
    try:
        with open("./Models/liver.pkl", 'rb') as model_file:
            model = pickle.load(model_file)
    except FileNotFoundError:
        st.error("Model file not found. Please check the file path.")
        st.stop()
    except Exception as e:
        st.error(f"❌ An error occurred while loading the model: {e}")
        st.stop()

    # Title of the app
    st.title("🫀 Liver Disease Predictor")
    st.write("Please enter the following details to make a prediction:")

    # Input fields for user data
    age = st.number_input("Age (in years)", min_value=0, step=1)
    gender = st.number_input("Gender (0: Male; 1: Female)", min_value=0, max_value=1, step=1)
    total_bilirubin = st.number_input("Total Bilirubin (in mg/dL)", min_value=0.0)
    direct_bilirubin = st.number_input("Conjugated Bilirubin (in mg/dL)", min_value=0.0)
    alkaline_phosphatase = st.number_input("Alkaline Phosphatase (in IU/L)", min_value=0.0)
    alamine_aminotransferase = st.number_input("Alamine Aminotransferase (in IU/L)", min_value=0.0)
    aspartate_aminotransferase = st.number_input("Aspartate Aminotransferase (in IU/L)", min_value=0.0)
    total_proteins = st.number_input("Total Proteins (in g/dL)", min_value=0.0)
    albumin = st.number_input("Albumin (in g/dL)", min_value=0.0)
    albumin_and_globulin_ratio = st.number_input("Albumin and Globulin Ratio", min_value=0.0)

    # User Input Form for heart disease prediction
    if st.button("🔍 Predict"):
        # Prepare input data for prediction
        input_data = np.array([[age, gender, total_bilirubin, direct_bilirubin,
                                alkaline_phosphatase, alamine_aminotransferase,
                                aspartate_aminotransferase, total_proteins,
                                albumin, albumin_and_globulin_ratio]])
        # Make prediction using the loaded model
        prediction = model.predict(input_data)
        
        # Store diagnosis in session state
        if prediction[0] == 1:
            st.session_state.liver_diagnosis = "Liver Disease Detected"
            st.success("The model predicts that you have liver disease. Please consult a doctor.")
        else:
            st.session_state.liver_diagnosis = "No Liver Disease"
            st.error("The model predicts that you do not have liver disease.")

        # Reset prescription when a new diagnosis is made
        st.session_state.liver_prescription = None

    # Display Diagnosis and Prescription Recommendations if available
    if "liver_diagnosis" in st.session_state:
        st.markdown("---")
        st.info(f"**Diagnosis:** {st.session_state.liver_diagnosis}")
        # Generate prescription recommendations based on diagnosis
        if st.button(" 📜 Generate Prescription Recommendations"):
            st.session_state.liver_prescription = get_prescription(st.session_state.liver_diagnosis)

        if "liver_prescription" in st.session_state and st.session_state.liver_prescription:
            st.markdown("---")
            st.subheader("💊 Treatment Recommendations")
            st.success("**Prescription Guidelines:**")
            st.write(st.session_state.liver_prescription)
            st.markdown("""
                **📌 Important Notes:**
                - Consult a hepatologist for further tests like ultrasound or liver biopsy.
                - Maintain a healthy diet, avoiding alcohol and processed foods.
                - Medication may be required based on liver enzyme levels.
            """)
    # Navigation button to return to the main page
    if st.button("← Back to Diagnosis"):
        st.session_state.page = "diagnosis"
        st.rerun()
