import GmailAPI as ml
import EmailAsst as astn
import json

def createInitialLabels():
  ml.create_label("Priority", "#000000", "#cc3a21")
  ml.create_label("Not Important", "#000000", "#ffad47")
  ml.create_label("Useless", "#000000", "#4a86e8")
  # ml.create_label("Cannot Classify", "#000000", "#cccccc")

def processEmails(emails, count):
  for email in emails:
    try:
      response = astn.generate(str(email))
    except:
      try:
        response = astn.generate(str(email))
      except:
        print("An error occurred while generating response.")
        continue
    
    try:
      # Parse the JSON string into a dictionary
      res = json.loads(response)
    except:
      try:
        res = json.loads(response)
      except:
        print("An error occurred while parsing the response.")
        continue
    
    email['Summary'] = res['Summary']
    email['Category'] = res['Category'] 

    if res['Category'] != 'Cannot Classify':
      ml.addLabels(email, [res['Category']])
      if res['Category'] != 'Priority':
        ml.removeLabels(email, ['INBOX'])
    else:
      print("Cannot classify email. Label not added.")

    print("Emails Processed:", count)
    count += 1
  return

def batchProcessEmails(mails, batch_size):
  for i in range(0, len(mails), batch_size):
    print("Batch", i//batch_size + 1) # printing the batch number
    
    batch = mails[i:i+batch_size]
    print("Processing", len(batch), "emails.") # printing the number of emails in the batch
    
    emails = ml.getEmails(batch)
    processEmails(emails, i+1)  
  return 

def main():
  labels = ['INBOX'] # this line specifies the label of the emails to be read
  state = "is:unread" # this line specifies the state of the emails to be read
  
  mails = ml.listEmails(labels, state)
  batch_size = 10
  
  if not mails:
    print("No emails found.")
  else:
    print(len(mails), "emails found.")
    batchProcessEmails(mails, batch_size)
    print("Processing Complete. No more emails to process or remaining emails cannot be classified due to lack of prefs.")
  return

if __name__ == "__main__":
  main()