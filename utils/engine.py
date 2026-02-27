import google.generativeai as genai
from core.key_manager import key_manager

def get_gemini_response(prompt, temperature=0.7):
    """
    Fetches a response from Gemini using the Round Robin key manager.
    """
    try:
        # 1. Get the current key from Round Robin
        current_key = key_manager.get_next_gemini_key()
        
        # 2. Configure the library
        genai.configure(api_key=current_key)
        
        # 3. Initialize the model 
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        # 4. Execute the prompt
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
            )
        )
        return response.text

    except Exception as e:
        # Fail-Soft Mechanism: In a production scenario, we would loop back 
        # to the key_manager to grab the next key if we hit a 429 error.
        return f"Engine Error: {str(e)}"