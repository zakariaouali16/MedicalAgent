CareNavigator: Medical Intake Assistant
CareNavigator is a LangGraph-powered medical triage assistant designed to conduct patient intake interviews. It gathers symptom details—onset, severity, and duration—and provides a summary recommendation for care.

🚀 Key Features
Intelligent Intake: Uses a state machine (LangGraph) to ensure specific information (Onset, Severity, and Duration) is collected before moving to triage.

Emergency Detection: Includes a dedicated safety layer that monitors for critical keywords (e.g., "chest pain," "heart attack," "can't breathe") and triggers an immediate emergency alert.

Automated Triage: Once data is collected, a "Triage Nurse" agent classifies urgency (Low to Critical) and recommends the appropriate level of care (Home, Urgent Care, or ER).

Vertex AI Integration: Powered by the gemini-2.5-flash model via Google Vertex AI.

🛠️ Project Structure
agent.py: Defines the LangGraph workflow, including the safety check, chatbot investigator, and triage decision nodes.

safety.py: Contains the logic for keyword and regex-based emergency detection.

main.py: The entry point for the chat session, handling the user interface loop and history.

utils.py: Helper functions for loading environment variables and project secrets.

⚙️ Setup
Environment Variables: Create a .env file in the root directory and add your GCP project ID:

Code snippet
PROJECT_ID=your-google-cloud-project-id
(Referenced in utils.py)

Installation: Ensure you have the required libraries installed:

Bash
pip install langgraph langchain_core langchain_google_vertexai python-dotenv
Run the Assistant:

Bash
python main.py
📝 Usage
Launch the script and describe your symptoms to the agent.

The agent will ask follow-up questions until it has enough data to summarize your case.

Type q or quit at any time to exit the session.

⚠️ Disclaimer
This tool is a medical intake assistant prototype. It does not provide official medical diagnoses and is intended for informational triage purposes only. In the event of a real emergency, always call local emergency services immediately.