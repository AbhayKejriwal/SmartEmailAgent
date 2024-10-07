import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
with open("Prefs.txt", "r", encoding="utf-8") as f:
  prefs = f.read()


def generate(message):
  genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
  model = genai.GenerativeModel(model_name="gemini-1.5-flash")
  
  prompt = """You are a personal email assistant. Your job is to know the user's priorities, preferences and requirements about their email and filter out the content and display it in the set format.

    #User Preferences & Special Instructions: """ + prefs + """

    The email message is provide in HTML format and the output should be strictly returned in the specified JSON format with no other prefix or suffix. Filter the right content according to my requirements, provide a brief summary of the mail content and categorize the mail. The various default categories are: \"Priority\", \"NotImportant\", \"Spam\" and \"CannotClasify\"(not enough data in preferences to categorize the mail).

    OUTPUT FORMAT:
    {
    \"Summary\": \"<summary_of_the_mail>\",
    \"Category\": \"<category_of_the_mail>\"
    }

    EMAIL MESSAGE in HTML format:
    \"\"\"""" + message + """\"\"\"
    
    """
  # print(prompt)
  try:
    response = model.generate_content(prompt)
    return response.text
  except Exception as e:
    print("Error in generating response.")
    print(e)
    return None

def main():
  with open("1917a9d2c104454d.html", "r", encoding="utf-8") as f:
    message = f.read()
  summary = generate(message)
  with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary)


if __name__=="__main__":
  # generate("Hello, this is a test message")
  main()