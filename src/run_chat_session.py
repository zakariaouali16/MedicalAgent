def run_chat_session():
    print("--- 🏥 CareNavigator Initialized (Type 'q' to quit) ---")
    
    # 1. Start with an empty list to track the whole conversation
    messages = []
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['q', 'quit']:
            break
            
        # 2. Add the new user message to th history
        messages.append(HumanMessage(content=user_input))
        
        # 3. Pass the FULL history to the agent
        output = agent_app.invoke({"messages": messages})
        
        if output.get("is_emergency"):
            print("🚨 SYSTEM ALERT: This sounds like a medical emergency.")
            print("Please hang up and call 911 immediately.")
            break
        
        # 4. Get the AI's response and add IT to the history too
        ai_msg = output['messages'][-1]
        messages.append(ai_msg) 
        
        print(f"Agent: {ai_msg.content}")