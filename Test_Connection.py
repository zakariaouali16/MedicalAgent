from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel

# Initialize connection (Keep your project ID here)
vertexai.init(project="medicalagent-487007", location="us-central1")

# Define the "System Instruction" - This tells the AI its job
system_instruction = [
    "You are a helpful medical intake assistant.",
    "Your goal is to collect symptom information from patients to help doctors.",
    "You do NOT give diagnoses.",
    "Always be empathetic and clear."
]

# Load the model with the system instruction
model = GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=system_instruction
)

# Test with a new prompt
response = model.generate_content("Hello! I have a patient with a headache. How can you help me?")
print(response.text)