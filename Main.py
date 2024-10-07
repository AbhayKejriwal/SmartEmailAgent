import GmailAPI as ml
import EmailAsst as astn
import json
import os

def createInitialLabels():
  ml.create_label("Important Emails", "#000000", "#cc3a21")
  ml.create_label("Not Important", "#000000", "#ffad47")
  ml.create_label("Spam", "#000000", "#4a86e8")
  ml.create_label("Cannot Classify", "#000000", "#cccccc")

def processEmails(emails):
  for email in emails:
      # message = email.pop('Message')
      try:
        response = astn.generate(email)
        # print(response)
        res = json.loads(response) # Parse the JSON string into a dictionary
        email['Summary'] = res['Summary']
        email['Category'] = res['Category'] 
        ml.addLabels(email, [res['Category']])
      except:
        print("Error in processing response.")

def main():
  labels = ['INBOX'] # this line specifies the label of the emails to be read
  state = "is:unread" # this line specifies the state of the emails to be read
  emails = ml.getEmails(labels, state)
  
  if not emails:
    print("No emails found.")
  else:
    processEmails(emails)

if __name__ == "__main__":
  main()