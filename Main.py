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
    response = astn.generate(str(email))
    res = json.loads(response) # Parse the JSON string into a dictionary
    print(res)
    
    email['Summary'] = res['Summary']
    email['Category'] = res['Category'] 

    if res['Category'] != 'Cannot Classify':
      ml.addLabels(email, [res['Category']])
      if res['Category'] != 'Priority':
        ml.removeLabels(email, ['INBOX'])
    print("Emails Processed:", count)
    count += 1
  return count


def main():
  labels = ['INBOX'] # this line specifies the label of the emails to be read
  state = "is:unread" # this line specifies the state of the emails to be read
  
  # emails = ml.getEmails(labels, state)
  mails = ml.listEmails(labels, state)
  batch_size = 10
  
  if not mails:
    print("No emails found.")
  else:
    print(len(mails), "emails found.")
    count = 1
    for i in range(0, len(mails), batch_size):
      batch = mails[i:i+batch_size]
      print(batch)
      emails = ml.getEmails(batch)
      count = processEmails(emails, count)
    else:
      print("No more emails.")

if __name__ == "__main__":
  main()