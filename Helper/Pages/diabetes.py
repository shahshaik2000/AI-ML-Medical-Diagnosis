import streamlit as st
import pickle
import numpy as np
from Helper.basic_diagnosis import get_prescription  # Import prescription function

def run():
    # Load the pre-trained model
    try:
        with open("./Models/diabetes.pkl", 'rb') as model_file:
            model = pickle.load(model_file)
    except FileNotFoundError:
        st.error("⚠️ Model file not found! Please check the file path.")
        st.stop()
    except Exception as e:
        st.error(f"❌ An error occurred while loading the model: {e}")
        st.stop()

    # Title & Instructions
    st.title("🩻 Diabetes Prediction")
    st.write("Please enter the following details to make a prediction:")
    st.markdown("---")

    # Initialize session states for diabetes-specific diagnosis & prescription
    if "diabetes_diagnosis" not in st.session_state:
        st.session_state["diabetes_diagnosis"] = None
    if "diabetes_prescription" not in st.session_state:
        st.session_state["diabetes_prescription"] = None

    # User Input Form for heart disease predictions
    pregnancies = st.number_input("No. of Pregnancies", min_value=0, step=1)
    glucose = st.number_input("Glucose Level", min_value=0.0)
    blood_pressure = st.number_input("Blood Pressure (mmHg)", min_value=0.0)
    skin_thickness = st.number_input("Skin Thickness (mm)", min_value=0.0)
    insulin = st.number_input("Insulin (µU/ml)", min_value=0.0)
    bmi = st.number_input("BMI", min_value=0.0)
    diabetes_pedigree_function = st.number_input("Diabetes Pedigree Function", min_value=0.0)
    age = st.number_input("Age (years)", min_value=0)

    # Submit button for the form
    if st.button("🔍 Predict"):
        # Prepare input data for prediction
        input_data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                                insulin, bmi, diabetes_pedigree_function, age]])
        
        # Make prediction using the loaded model
        prediction = model.predict(input_data)
        
        # Store diagnosis in session state (specific to diabetes page)
        if prediction[0] == 1:
            st.session_state["diabetes_diagnosis"] = "High probability of diabetes"
        else:
            st.session_state["diabetes_diagnosis"] = "Low probability of diabetes"

        # Reset prescription when new prediction is made
        st.session_state["diabetes_prescription"] = None

        st.success(f"🩺 **Prediction:** {st.session_state['diabetes_diagnosis']}")

    # Display Diagnosis and Prescription Recommendations if available
    if st.session_state["diabetes_diagnosis"]:
        st.markdown("---")
        st.info(f"**Diagnosis:** {st.session_state['diabetes_diagnosis']}")

        # Generate prescription recommendations based on diagnosis
        if st.button("📜 Generate Prescription Recommendations"):
            st.session_state["diabetes_prescription"] = get_prescription(st.session_state["diabetes_diagnosis"])

    # Display Prescription (if available)
    if st.session_state["diabetes_prescription"]:
        st.markdown("---")
        st.subheader("💊 Treatment Recommendations")
        st.success("**Prescription Guidelines:**")
        st.write(st.session_state["diabetes_prescription"])
        st.markdown("""
        **📌 Important Notes:**
        - These recommendations should be reviewed by a qualified doctor.
        - Regular monitoring of blood sugar levels is essential.
        - A healthy lifestyle, diet, and exercise are crucial.
        """)

    # Navigation button to return to the main page
    if st.button("⬅️ Back to Diagnosis Page"):
        st.session_state.page = "diagnosis"
        st.rerun()
