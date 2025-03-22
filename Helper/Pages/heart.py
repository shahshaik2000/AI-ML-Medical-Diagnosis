import streamlit as st
import pickle
import pandas as pd
from Helper.basic_diagnosis import  get_prescription

def run():
    st.title("❤️ Heart Disease Prediction")

    # Load the pre-trained model
    try:
        model = pickle.load(open("./Models/heart.pkl", 'rb'))
    except FileNotFoundError:
        st.error("⚠️ Model file not found! Please check the file path.")
        st.stop()

    st.write("This page helps predict heart disease probability based on medical parameters.")
    st.markdown("---")

    # Initialize session state variables for diagnosis and prescription
    if "heart_diagnosis" not in st.session_state:
        st.session_state["heart_diagnosis"] = None
    if "heart_prescription" not in st.session_state:
        st.session_state["heart_prescription"] = None

    # User Input Form for heart disease prediction
    with st.form(key='heart_disease_form'):
        age = st.text_input("Age (in years)")
        sex = st.text_input("Sex (1 = Male; 0 = Female)")
        cp = st.text_input("Chest Pain Type")
        trestbps = st.text_input("Resting Blood Pressure (in mm Hg)")
        chol = st.text_input("Serum Cholesterol (in mg/dl)")
        fbs = st.text_input("Fasting Blood Sugar > 120 mg/dl (1 = True; 0 = False)")
        restecg = st.text_input("Resting Electrocardiograph Results")
        thalach = st.text_input("Maximum Heart Rate Achieved")
        exang = st.text_input("Exercise Induced Angina (1 = Yes; 0 = No)")
        oldpeak = st.text_input("ST Depression Induced by Exercise Relative to Rest")
        slope = st.text_input("The Slope of the Peak Exercise ST Segment")
        ca = st.text_input("Number of Major Vessels (0-3) Colored by Fluoroscopy")
        thal = st.text_input("Thal: 1 = Normal; 2 = Fixed Defect; 3 = Reversible Defect")
        # Submit button for the form
        submit_button = st.form_submit_button("🔍 Predict")

    if submit_button:
        # Prepare input data for prediction
        input_data = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]],
                                  columns=['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang',
                                           'oldpeak', 'slope', 'ca', 'thal'])

        # Make prediction using the loaded model
        try:
            prediction = model.predict(input_data)
            prediction_proba = model.predict_proba(input_data)

            # Calculate confidence of the prediction
            confidence = max(prediction_proba[0])  # Probability of the predicted class

            # Store diagnosis result in session state
            st.session_state["heart_diagnosis"] = "High probability of heart disease" if prediction[0] == 1 else "Low probability of heart disease"
            
            # Display the prediction result with confidence level
            st.success(f"🩺 **Prediction:** {st.session_state['heart_diagnosis']} (Confidence: {confidence:.2%})")

            # Reset prescription when new diagnosis is made
            st.session_state["heart_prescription"] = None

        except Exception as e:
            st.error(f"❌ Error processing input: {e}")

    # Display Diagnosis and Prescription Recommendations if available
    if st.session_state["heart_diagnosis"]:
        st.markdown("---")
        st.info(f"**Diagnosis:** {st.session_state['heart_diagnosis']}")

        if st.button("📜 Generate Prescription Recommendations"):
            # Generate prescription recommendations based on diagnosis
            st.session_state["heart_prescription"] = get_prescription(st.session_state["heart_diagnosis"])

        if st.session_state["heart_prescription"]:
            st.markdown("---")
            st.subheader("💊 Treatment Recommendations")
            st.success("**Prescription Guidelines:**")
            st.write(st.session_state["heart_prescription"])
            st.markdown("""
                **📌 Important Notes:**
                - These recommendations should be reviewed by a qualified cardiologist.
                - Additional tests may be required for confirmation.
                - Maintain regular heart checkups and a healthy lifestyle.
            """)
    # Navigation button to return to the main page
    st.markdown("---")
    if st.button("⬅️ Back to Main Page"):
        st.session_state.page = "diagnosis"
        st.rerun()
