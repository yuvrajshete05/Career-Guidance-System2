import google.generativeai as genai

# Use your actual API key here
genai.configure(api_key="AIzaSyB90I1SwWaUCMttTSv1mLRYP2ySpOUpYIY")

try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("What is Infosys?")
    print("Success! Response from Gemini API:")
    print(response.text)
except Exception as e:
    print("Failed to get a response from Gemini API.")
    print("Error details:", e)