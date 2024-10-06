import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


def getCredentials():
  """
  The `getCredentials` function in Python retrieves and manages user credentials for accessing Gmail
  using OAuth 2.0 authentication.
  :return: The `getCredentials` function returns the credentials needed for accessing and managing
  Gmail using the specified scopes.
  """
  creds = None

  SCOPES = ['https://mail.google.com/', # this scope allows us to read, write, send, and delete emails
            'https://www.googleapis.com/auth/gmail.labels'] # this scope allows us to manage labels

  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first time.
  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request()) 
    else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open('token.json', 'w') as token:
      token.write(creds.to_json())

  return creds

def getEmail(service, message):
  """
  The function `getEmail` retrieves and processes email information from a specified message using the
  Gmail API in Python.
  
  :param service: The `service` parameter in the `getEmail` function is typically an instance of a
  Gmail service object that allows interaction with the Gmail API. This object is used to retrieve
  information about a specific email message identified by its ID
  
  :param message: The function `getEmail` takes two parameters: `service` and `message`. The `service`
  parameter is expected to be a Gmail service object, and the `message` parameter is expected to be a
  dictionary representing a message retrieved from Gmail
  
  :return: The `getEmail` function is returning a dictionary containing the MessageID, Subject, From,
  and Message content of the email.
  """
  msg = service.users().messages().get(userId='me', id=message['id']).execute()
  
  payload = msg.get('payload')
  headers = payload.get('headers')

  for header in headers:
    if header['name'] == 'Subject': 
      subject = header['value'] 
    if header['name'] == 'From': 
      sender = header['value']
  text = ""

  parts = payload.get('parts')
  for part in parts:
    data = part['body'].get('data', '')  # Safely retrieve the value of 'data' key with a default value of an empty string
    byte_code = base64.urlsafe_b64decode(data)
    text = text + byte_code.decode("utf-8")
  email = { 'MessageID': message['id'], 'Subject': subject, 'From': sender, 'Message': text }

  return email
  # msg  = service.users().messages().modify(userId='me', id=message['id'], body={'removeLabelIds': ['UNREAD']}).execute()

def getEmails(labels=[], state=None):
  """
  The function `getEmails` uses the Gmail API to retrieve emails based on specified labels and state
  parameters.
  
  :param labels: The `labels` parameter in the `getEmails` function is used to specify the labels of
  the emails you want to retrieve. Labels are like folders in Gmail that help you organize your
  emails. By providing label IDs in the `labels` parameter, you can filter the emails based on those
  labels
  
  :param state: The `state` parameter in the `getEmails` function is used to filter the emails based
  on a specific query string. If provided, it will search for emails that match the specified query
  string in the Gmail account
  
  :return: The `getEmails` function returns a list of email messages based on the specified labels and
  state parameters. It interacts with the Gmail API to retrieve messages from the user's Gmail
  account.
  """
  # Call the Gmail API
  creds = getCredentials() # this line gets the credentials of the user to access the gmail account
  service = build('gmail', 'v1', credentials=creds) # this line creates a service object that interacts with the Gmail API
  if not labels and not state:
    results = service.users().messages().list(userId='me').execute
  elif not state:
    results = service.users().messages().list(userId='me', labelIds=labels).execute()
  elif not labels:
    results = service.users().messages().list(userId='me', q=state).execute()
  else:
    results = service.users().messages().list(userId='me', labelIds=labels, q=state).execute()

  messages = results.get('messages', [])

  emails = []
  for message in messages:
    email = getEmail(service, message)
    emails.append(email)

  return emails

def getLabels():
  creds = getCredentials() # this line gets the credentials of the user to access the gmail account
  service = build('gmail', 'v1', credentials=creds) # this line creates a service object that interacts with the Gmail API
  results = service.users().labels().list(userId="me").execute()
  labels = results.get("labels", [])

  if not labels:
    print("No labels found.")
    return
  print("Labels:")
  for label in labels:
    print(label["name"])
  return labels

def get_label_id(label_name):
  """Fetch the label ID of a custom label by its name."""
  try:
    creds = getCredentials() # this line gets the credentials of the user to access the gmail account
    service = build('gmail', 'v1', credentials=creds)
    labels = service.users().labels().list(userId='me').execute()
    for label in labels['labels']:
        if label['name'] == label_name:
            return label['id']
    print(f"Label '{label_name}' not found.")
  except Exception as e:
    print(f"An error occurred while fetching labels: {e}")
    return None

def removeLabels(email, labels):
  try:
    creds = getCredentials()
    service = build('gmail', 'v1', credentials=creds)
    label_ids = []
    for label in labels:
      label_ids.append(get_label_id(label))
    service.users().messages().modify(userId='me', id=email['MessageID'], body={'removeLabelIds': label_ids}).execute()
    print(f"Label {labels} removed from email {email['Subject']}.")
  except Exception as e:
    print(f"An error occurred while removing label from email: {e}")

def addLabels(email, labels):
  try:
    creds = getCredentials()
    service = build('gmail', 'v1', credentials=creds)
    label_ids = []
    for label in labels:
      label_ids.append(get_label_id(label))
    service.users().messages().modify(userId='me', id=email['MessageID'], body={'addLabelIds': label_ids}).execute()
    print(f"Label {labels} added to email {email['Subject']}.")
  except Exception as e:
    print(f"An error occurred while adding label to email: {e}")

def create_label(label_name):
  """Creates a new label in the user's Gmail account."""
  label_body = {
  "labelListVisibility": "labelShow",
  "messageListVisibility": "show",
  "name": label_name,
  }
  creds = getCredentials()
  service = build('gmail', 'v1', credentials=creds)
  try:
    label = service.users().labels().create(userId='me', body=label_body).execute()
    print(f"Label created: {label['id']}, {label['name']}")
    return label
  except Exception as e:
    print(f"An error occurred: {e}")
    return None

def modify_label_color(label_id, text_color, background_color):
  """Modify the color of an existing label given its ID."""
  label_body = {
      "color": {
          "textColor": text_color,
          "backgroundColor": background_color
      }
  }
  creds = getCredentials()
  service = build('gmail', 'v1', credentials=creds)
  try:
    
    label = service.users().labels().update(userId='me', id=label_id, body=label_body).execute()
    print(f"Label updated")
    return label
  except Exception as e:
    print(f"An error occurred while updating the label: {e}")
    return None

# Driver and Test code
def main():
  labels = ['INBOX']
  state = "is:unread"
  # modify_label_color('Label_5', '#ffffff', '#000000') - invalid colour codes
  # emails = getEmails(labels, state)

  # if not emails:
  #   print("No emails found.")
  # else:
  #   for email in emails:
  #     print(email['Subject'], email['From'])#, email['Message'])
  #     removeLabels(email, ['Not Important'])
      # # Store the email in a text file
      # with open('email.txt', 'w') as file:
      #   file.write(str(email))
  # create_label('Not Important')
  # print(getLabels())
  # print(get_label_id('Not Important'))



def fetchAllEmails():
  emails = getEmails()
  return emails

def fetchInbox():
  labels = ['INBOX']
  inbox = getEmails(labels)
  return inbox

def fetchStarred():
  labels = ['STARRED']
  starred = getEmails(labels)
  return starred

def fetchUnread():
  state = "is:unread"
  unread = getEmails(state)
  return unread

def fetchRead():
  state = "is:read"
  read = getEmails(state)
  return read

def markRead(email):
  removeLabels(email, ['UNREAD'])

def markUnread(email):
  addLabels(email, ['UNREAD'])

def markStarred(email):
  addLabels(email, ['STARRED'])

def markUnstarred(email):
  removeLabels(email, ['STARRED'])

def deleteEmail(email):
  creds = getCredentials()
  service = build('gmail', 'v1', credentials=creds)
  msg = service.users().messages().delete(userId='me', id=email['MessageID']).execute()
  return msg

def archiveEmail(email):
  creds = getCredentials()
  service = build('gmail', 'v1', credentials=creds)
  msg = service.users().messages().modify(userId='me', id=email['MessageID'], body={'removeLabelIds': ['INBOX']}).execute()
  return msg

# Run the main function
if __name__ == '__main__':
  main()