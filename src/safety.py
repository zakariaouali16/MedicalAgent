import re

def detect_emergency(user_input: str) -> bool:
    """
    Analyzes user input for high-risk keywords indicating a medical emergency.
    Returns True if the input suggests an immediate threat to life.
    """
    
    # Convert to lowercas for easier matching
    text = user_input.lower()

    # 1. DIRECT KEYWORD MATCHING (Fastest)
    # List of unambiguous emergency terms
    emergency_keywords = [
        "call 911",
        "suicide",
        "kill myself",
        "want to die",
        "crushing chest pain",
        "heart attack",
        "stroke",
        "dying",            # <--- ADD THIS
        "feel like i am dying",
        "can't breathe",
        "difficulty breathing",
        "unconscious",
        "passed out",
        "bleeding heavily",
        "deep cut",
        "poison",
        "overdose",
        "baby not moving",
        "seizure"
    ]

    for keyword in emergency_keywords:
        if keyword in text:
            return True

    # 2. REGEX PATTERNS (Smarter)
    # Catches variations like "chest is hurting" or "can not breathe"
    patterns = [
        r"chest.*(pain|pressure|tightness|hurt)",  # Matches "chest really hurts"
        r"(cant|can't|cannot).*breathe",           # Matches "I cannot breathe"
        r"(numb|weak).*face",                       # Stroke symptom
        r"(slurred).*speech",                       # Stroke symptom
        r"(sudden).*(blindness|vision loss)"        # Stroke symptom
    ]

    for pattern in patterns:
        if re.search(pattern, text):
            return True

    return False

# Quick test block to run this file directly
if __name__ == "__main__":
    print("--- Testing Safety Module ---")
    test_input = "I want to kill myself"
    is_emergency = detect_emergency(test_input)
    print(f"Input: '{test_input}'")
    print(f"Is Emergency? {is_emergency}") 
    
    test_input_2 = "I have a mild headache"
    print(f"\nInput: '{test_input_2}'")
    print(f"Is Emergency? {detect_emergency(test_input_2)}")