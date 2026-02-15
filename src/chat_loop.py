import vertexai
from vertexai.generative_models import GenerativeModel, ChatSession

# 1. Initialize Connection
vertexai.init(project="medicalagent-487007", location="us-central1")

# 2. Define the Persona
system_instruction = [
    "You are a helpful medical intake assistant named MedBot.",
    "Your goal is to collect symptom information (onset, severity, duration) from patients.",
    "Do NOT provide medical diagnoses. Advise users to see a doctor for serious issues.",
    "Keep your responses concise and empathetic."
]

# 3. Load the Modell 
model = GenerativeModel(
    "gemini-2.5-flash",
    system_instruction=system_instruction
)

# 4. Start the Chat Session (This remembers history!)
chat = model.start_chat()

print("--- MedBot MVP Started (Type 'quit' to exit) ---")

while True:
    # Get user input
    user_input = input("You: ")
    
    # Exit condition
    if user_input.lower() in ["quit", "exit"]:
        print("MedBot: Goodbye and take care!")
        break
    
    # Send message to Gemini and print response
    try:
        response = chat.send_message(user_input)
        print(f"MedBot: {response.text}")
    except Exception as e:
        print(f"Error: {e}")