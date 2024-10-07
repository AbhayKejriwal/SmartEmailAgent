import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

load_dotenv()
with open("Prefs.txt", "r", encoding="utf-8") as f:
  prefs = f.read()

def generate(email):
  genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
  model = genai.GenerativeModel(model_name="gemini-1.5-flash")
  
  prompt = """You are a personal email assistant. Your job is to know the user's details, priorities, preferences and requirements about their email and filter out the content and display it in the set format.

  #User Details, Preferences & Special Instructions: """ + prefs + """

  The email message is provide in HTML format and the output should be strictly returned in the specified JSON format with no other prefix or suffix. Filter the right content according to my requirements, provide a brief summary of the mail content and categorize the mail. The various default categories are: \"Priority\", \"Not Important\", \"Useless\" and \"Cannot Clasify\"(not enough data in preferences to categorize the mail).

  !!!The output should be strictly returned in the specified JSON format with no prefix or suffix like json. You do not need to specify it is a JSON output. It is assumed it is a pure json without any issue!!!
  OUTPUT FORMAT:
  {
  \"Summary\": \"<summary_of_the_mail>\",
  \"Category\": \"<category_of_the_mail>\"
  }

  EMAIL MESSAGE:
  """ + email + """
  
  """
  # print(prompt)
  try:
    response = model.generate_content(prompt)
    return response.text
  except Exception as e:
    print("Error in generating response.")
    print(e)
    return None

# Driver and test code
def main():
  with open("1917a9d2c104454d.txt", "r", encoding="utf-8") as f:
    message = f.read()
  summary = generate(message)
  print(summary)


if __name__=="__main__":
  # generate("Hello, this is a test message")
  main()