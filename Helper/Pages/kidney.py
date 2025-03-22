import streamlit as st
import pickle
import numpy as np
from Helper.basic_diagnosis import get_prescription  # Import prescription function

def run():
    # Load the pre-trained model
    try:
        with open("./Models/kidney.pkl", 'rb') as model_file:
            model = pickle.load(model_file)
    except FileNotFoundError:
        st.error("⚠️ Model file not found! Please check the file path.")
        st.stop()
    except Exception as e:
        st.error(f"❌ An error occurred while loading the model: {e}")
        st.stop()

    # Title & Instructions
    st.title("🩺 Kidney Disease Prediction")
    st.write("Please enter the following details to make a prediction:")
    st.markdown("---")

    # Initialize session states for kidney-specific diagnosis & prescription
    if "kidney_diagnosis" not in st.session_state:
        st.session_state["kidney_diagnosis"] = None
    if "kidney_prescription" not in st.session_state:
        st.session_state["kidney_prescription"] = None

    # Input fields for user data
    age = st.number_input("Age (in years)", min_value=0, step=1)
    blood_pressure = st.number_input("Blood Pressure (in mm/Hg)", min_value=0.0)
    specific_gravity = st.number_input("Specific Gravity", min_value=0.0)
    albumin = st.number_input("Albumin (0, 1, 2, 3, 4, 5)", min_value=0, max_value=5, step=1)
    sugar = st.number_input("Sugar (0, 1, 2, 3, 4, 5)", min_value=0, max_value=5, step=1)
    red_blood_cells = st.number_input("Red Blood Cells (0: Abnormal; 1: Normal)", min_value=0, max_value=1, step=1)
    pus_cell = st.number_input("Pus Cell (0: Abnormal; 1: Normal)", min_value=0, max_value=1, step=1)
    pus_cell_clumps = st.number_input("Pus Cell Clumps (0: Not Present; 1: Present)", min_value=0, max_value=1, step=1)
    bacteria = st.number_input("Bacteria (0: Not Present; 1: Present)", min_value=0, max_value=1, step=1)
    blood_glucose_random = st.number_input("Blood Glucose Random (in mgs/dl)", min_value=0.0)
    blood_urea = st.number_input("Blood Urea (in mgs/dl)", min_value=0.0)
    serum_creatinine = st.number_input("Serum Creatinine (in mgs/dl)", min_value=0.0)
    sodium = st.number_input("Sodium (in mEq/L)", min_value=0.0)
    potassium = st.number_input("Potassium (in mEq/L)", min_value=0.0)
    haemoglobin = st.number_input("Haemoglobin (in gms)", min_value=0.0)
    packed_cell_volume = st.number_input("Packed Cell Volume", min_value=0.0)
    white_blood_cell_count = st.number_input("White Blood Cell Count (in cells/cumm)", min_value=0.0)
    red_blood_cell_count = st.number_input("Red Blood Cell Count (in millions/cmm)", min_value=0.0)
    hypertension = st.number_input("Hypertension (0: No; 1: Yes)", min_value=0, max_value=1, step=1)
    diabetes_mellitus = st.number_input("Diabetes Mellitus (0: No; 1: Yes)", min_value=0, max_value=1, step=1)
    coronary_artery_disease = st.number_input("Coronary Artery Disease (0: No; 1: Yes)", min_value=0, max_value=1, step=1)
    appetite = st.number_input("Appetite (0: Good; 1: Poor)", min_value=0, max_value=1, step=1)
    pedal_edema = st.number_input("Pedal Edema (0: No; 1: Yes)", min_value=0, max_value=1, step=1)
    anemia = st.number_input("Anemia (0: No; 1: Yes)", min_value=0, max_value=1, step=1)

    # User Input Form for heart disease prediction
    if st.button("🔍 Predict"):
        # Prepare input data for prediction
        input_data = np.array([[age, blood_pressure, specific_gravity, albumin, sugar,
                                red_blood_cells, pus_cell, pus_cell_clumps, bacteria,
                                blood_glucose_random, blood_urea, serum_creatinine,
                                sodium, potassium, haemoglobin, packed_cell_volume,
                                white_blood_cell_count, red_blood_cell_count,
                                hypertension, diabetes_mellitus, coronary_artery_disease,
                                appetite, pedal_edema, anemia]])
        
        # Make prediction using the loaded model
        prediction = model.predict(input_data)
        
        # Store diagnosis in session state (specific to kidney page)
        if prediction[0] == 1:
            st.session_state["kidney_diagnosis"] = "High probability of kidney disease"
        else:
            st.session_state["kidney_diagnosis"] = "Low probability of kidney disease"

        # Reset prescription when new prediction is made
        st.session_state["kidney_prescription"] = None

        st.success(f"🩺 **Prediction:** {st.session_state['kidney_diagnosis']}")

    # Display Diagnosis and Prescription Recommendations if available
    if st.session_state["kidney_diagnosis"]:
        st.markdown("---")
        st.info(f"**Diagnosis:** {st.session_state['kidney_diagnosis']}")

        # Generate prescription recommendations based on diagnosis
        if st.button("📜 Generate Prescription Recommendations"):
            st.session_state["kidney_prescription"] = get_prescription(st.session_state["kidney_diagnosis"])

    # Display Prescription (if available)
    if st.session_state["kidney_prescription"]:
        st.markdown("---")
        st.subheader("💊 Treatment Recommendations")
        st.success("**Prescription Guidelines:**")
        st.write(st.session_state["kidney_prescription"])
        st.markdown("""
        **📌 Important Notes:**
        - These recommendations should be reviewed by a qualified nephrologist.
        - Follow-up tests may be required for confirmation.
        - Maintain regular checkups and a kidney-healthy lifestyle.
        """)

    # Navigation button to return to the main page
    if st.button("⬅️ Back to Diagnosis Page"):
        st.session_state.page = "diagnosis"
        st.rerun()
