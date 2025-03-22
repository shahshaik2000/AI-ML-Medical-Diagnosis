import streamlit as st
from PyPDF2 import PdfReader
from Helper.basic_diagnosis import basic_diagnosis, get_prescription
from Helper.Pages import heart, breast_cancer, diabetes, kidney, liver
from PIL import Image

# Load and resize images for the application
image = Image.open("Images/image_2.png")
image1 = Image.open("Images/image_3.png")
resized_image = image.resize((500, 300))  # (width, height)
resized_image1 = image1.resize((200, 150))  # (width, height)

# Initialize session state for navigation and data storage
if "page" not in st.session_state:
    st.session_state.update({
        "page": "welcome",
        "diagnosis": None,
        "prescription": None,
        "pdf_text": ""
    })

# Welcome Page
if st.session_state.page == "welcome":
    st.title("Welcome to the Medical Diagnosis App")
    st.write("This app helps you identify possible medical conditions based on your symptoms.")
    st.image(resized_image, use_container_width=False)

    # Navigation button to start the diagnosis process
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Click Here To Start →"):
            st.session_state.page = "diagnosis"
            st.rerun()

# Diagnosis Page
elif st.session_state.page == "diagnosis":
    st.write("### Specialized Predictions")
    
    # Buttons for different medical conditions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("❤️ Heart Disease", key="heart"):
            st.session_state.page = "heart"
            st.rerun()
    with col2:
        if st.button("🩸 Breast Cancer", key="breast_cancer"):
            st.session_state.page = "breast_cancer"
            st.rerun()
    with col3:
        if st.button("🩻 Diabetes", key="diabetes"):
            st.session_state.page = "diabetes"
            st.rerun()

    col4, col5, col6 = st.columns(3)
    with col4:
        if st.button("🩺 Kidney Disease", key="kidney"):
            st.session_state.page = "kidney"
            st.rerun()
    with col5:
        if st.button("🫀 Liver Disease", key="liver"):
            st.session_state.page = "liver"
            st.rerun()

    # Display basic medical diagnosis section
    st.title("Basic Medical Diagnosis")
    
    # Center the image using columns
    col_left, col_center, col_right = st.columns([1, 6, 1])
    with col_center:
        st.image(resized_image1, use_container_width=False)

    # Sidebar for user input and PDF upload
    st.sidebar.header("Your Medical Data")
    
    # PDF file uploader for symptom extraction
    uploaded_file = st.sidebar.file_uploader("Upload a PDF file", type=["pdf"])
    if uploaded_file is not None:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            # Extract text from the PDF and store it in session state
            st.session_state.pdf_text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    # Text area for user to input symptoms
    st.sidebar.write("Enter symptoms as text.")
    symptom_text = st.sidebar.text_area("Enter your symptoms:")

    # Combine symptoms from user input and PDF text
    text_symptoms = [s.strip() for s in symptom_text.split(",") if s.strip()]
    all_symptoms = text_symptoms  # You can uncomment this line to include selected symptoms from a multiselect

    # Diagnosis button to process symptoms and generate diagnosis
    if st.sidebar.button("Diagnose"):
        if all_symptoms or st.session_state.pdf_text:
            full_input = f"{st.session_state.pdf_text} {' '.join(all_symptoms)}"
            # Call the basic diagnosis function with combined input
            st.session_state.diagnosis = basic_diagnosis(full_input)
        else:
            st.sidebar.warning("Please enter at least one symptom or upload a PDF")

    # Display the diagnosis results
    if st.session_state.diagnosis:
        st.success(f"Possible conditions based on your symptoms:\n\n{st.session_state.diagnosis}")
        
        # Button to generate prescription recommendations based on diagnosis
        if st.button("📜Generate Prescription Recommendations"):
            st.session_state.prescription = get_prescription(st.session_state.diagnosis)
        
        # Display prescription recommendations if available
        if st.session_state.prescription:
            st.title("Prescription Recommendations")
            st.write("Here are some possible treatment recommendations for your diagnosed conditions.")
            st.success(f"Recommended Prescription:\n\n{st.session_state.prescription}")
            st.write("- Consult your physician for proper medical guidance.")
            st.write("- Follow a healthy lifestyle and prescribed medications.")
            
    else:
        # Warning message when no diagnosis is available yet
        st.warning("No diagnosis yet. Please enter symptoms and click Diagnose.")
     
    # Navigation button to return to the welcome page
    col8, col7 = st.columns([1, 1])
    with col8:
        if st.button("⬅️  Previous"):
            st.session_state.page = "welcome"
            st.rerun()

# Conditional rendering of specific disease pages based on user selection
elif st.session_state.page == "heart":
    heart.run()
elif st.session_state.page == "breast_cancer":
    breast_cancer.run()
elif st.session_state.page == "diabetes":
    diabetes.run()
elif st.session_state.page == "kidney":
    kidney.run()
elif st.session_state.page == "liver":
    liver.run()