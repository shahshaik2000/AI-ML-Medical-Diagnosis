import ollama

# Initialize the Ollama client
client = ollama.Client()

# Define the model and the input prompt
model = "llama3.2:1b"  # Replace with your model name

# System prompt for diagnosis analysis
system1 = """Analyze the provided context and extract the key symptoms accurately.  
Summarize the diagnosis concisely in 2-3 sentences, ensuring clarity and informativeness.  
Focus on medically relevant details while avoiding unnecessary information or speculation.  
Present the symptoms in a structured manner and ensure the diagnosis is precise.  

Answer:  
MAIN SYMPTOMS: [List the key symptoms clearly]  
DIAGNOSIS SUMMARY: [Provide a concise and informative diagnosis] 
"""

# System prompt for treatment suggestions
system2 = """Based on the provided symptoms and medical history, suggest possible treatment approaches.  
Focus on general symptom management strategies, commonly recommended medications (without specific prescriptions), and alternative therapies.  
Ensure the response is concise, informative, and practical.  

Answer:  
TREATMENT SUGGESTIONS: [Briefly outline general treatment approaches and commonly used medications]  
LIFESTYLE & HOME REMEDIES: [Provide simple, effective wellness tips and non-medical alternatives]  
"""

def basic_diagnosis(text):
    """
    Generate a diagnosis based on the provided text input.
    
    Args:
        text (str): The input text containing symptoms and medical history.
    
    Returns:
        str: A summarized diagnosis response from the Ollama model.
    """
    response = client.generate(model=model, system=system1, prompt=text)
    return response.response

def get_prescription(text):
    """
    Generate treatment suggestions based on the provided symptoms.
    
    Args:
        text (str): The input text containing symptoms.
    
    Returns:
        str: Suggested treatment options based on the analysis from the Ollama model.
    """
    response = client.generate(model=model, system=system2, prompt=text)
    return response.response
