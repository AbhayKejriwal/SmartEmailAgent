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

def listEmails(labels=['INBOX'], state='is:unread'):
  creds = getCredentials() # this line gets the credentials of the user to access the gmail account
  service = build('gmail', 'v1', credentials=creds)
  
  if not labels and not state:
    results = service.users().messages().list(userId='me').execute
  elif not state:
    results = service.users().messages().list(userId='me', labelIds=labels).execute()
  elif not labels:
    results = service.users().messages().list(userId='me', q=state).execute()
  else:
    results = service.users().messages().list(userId='me', labelIds=labels, q=state).execute()

  messages = results.get('messages', [])
  return messages

def getEmails(messages):
  # Call the Gmail API
  creds = getCredentials() # this line gets the credentials of the user to access the gmail account
  service = build('gmail', 'v1', credentials=creds) # this line creates a service object that interacts with the Gmail API
  emails = []
  for message in messages:
    email = getEmail(service, message)
    emails.append(email)
  return emails

def deleteEmail(email):
  creds = getCredentials()
  service = build('gmail', 'v1', credentials=creds)
  msg = service.users().messages().delete(userId='me', id=email['MessageID']).execute()
  return msg

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
      label_id = get_label_id(label)
      if not label_id:
        label = create_label(label)
        label_id = label['id']
      label_ids.append(label_id)
    service.users().messages().modify(userId='me', id=email['MessageID'], body={'addLabelIds': label_ids}).execute()
    print(f"Label {labels} added to email {email['Subject']}.")
  except Exception as e:
    print(f"An error occurred while adding label to email: {e}")

def create_label(label_name, text_color="#000000", background_color="#ffffff"):
  """Creates a new label in the user's Gmail account."""
  label_body = {
  "labelListVisibility": "labelShow",
  "messageListVisibility": "show",
  "name": label_name,
  "color": {
          "textColor": text_color,
          "backgroundColor": background_color
      }
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
  state = "is:read"
  emails = getEmails(labels, state)
  if not emails:
    print("No emails found.")
  else:
    for email in emails:
      print(email)#['Subject'], email['From'])#, email['Message'])
  #     removeLabels(email, ['Not Important'])
  #     addLabels(email, ['Priority'])
  # create_label("Priority", "#000000", "#cc3a21")


# Run the main function
if __name__ == '__main__':
  main()