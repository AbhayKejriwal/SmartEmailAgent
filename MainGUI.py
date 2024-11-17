import GmailAPI as ml
import EmailAsst as astn
import json
import PySimpleGUI as sg
import threading

def createInitialLabels():
    ml.create_label("Priority", "#000000", "#cc3a21")
    ml.create_label("Not Important", "#000000", "#ffad47")
    ml.create_label("Useless", "#000000", "#4a86e8")

def extract_json(response_text):
    try:
        # Attempt to parse JSON from the response
        return json.loads(response_text)
    except json.JSONDecodeError as e:
        # print("Failed to parse JSON. Cleaning the response...")
        # Clean and retry parsing
        start_index = response_text.find("{")
        end_index = response_text.rfind("}") + 1
        if start_index != -1 and end_index != -1:
            clean_response = response_text[start_index:end_index]
            try:
                return json.loads(clean_response)
            except json.JSONDecodeError:
                print("Still unable to parse JSON.")
    return None

def processEmails(emails, total_count, count, window):
    for email in emails:
        try:
            response = astn.generate(str(email))
        except:
            try:
                response = astn.generate(str(email))
            except:
                print("An error occurred while generating response. Skipping mail.")
                window['-PROGRESS-'].update('Error occurred while generating response. Skipping mail.')
                continue
        
        try:
            res = extract_json(response)  # Parse the JSON string into a dictionary
        except:
            print("An error occurred while parsing the response. Skipping mail.")
            window['-PROGRESS-'].update('Error occurred while parsing the response. Skipping mail.')
            continue

        email['Summary'] = res['Summary']
        email['Category'] = res['Category']

        if res['Category'] != 'Cannot Classify':
            ml.addLabels(email, [res['Category']])
            if res['Category'] != 'Priority':
                ml.removeLabels(email, ['INBOX'])
        else:
            print("Cannot classify email. Label not added.")
            window['-PROGRESS-'].update('Cannot classify email. Label not added.')

        count += 1
        print("Emails Processed:", count, "/", total_count)
        window.write_event_value('-UPDATE-', (count, total_count))
    return count

def batchProcessEmails(mails, total_count, batch_size, window):
    for i in range(0, total_count, batch_size):
        # printing the batch number
        print("Batch", i//batch_size + 1)
        window['-EMAIL_COUNT-'].update(f'{total_count} emails found. Processing batch {i//batch_size + 1}')
        
        batch = mails[i:i+batch_size]
        print("Processing", len(batch), "emails.")  # printing the number of emails in the batch
                
        emails = ml.getEmails(batch)
        processEmails(emails, total_count, i+1, window)  
    return 

def fetch_and_filter_emails(window):
    labels = ['INBOX']
    state = "is:unread"    
    mails = ml.listEmails(labels, state)
    
    if not mails:
        print("No emails found.")
        window['-EMAIL_COUNT-'].update("No emails found.")
    else:
        total_count = len(mails)
        print(f"{total_count} emails found.")
        window['-EMAIL_COUNT-'].update(f"{total_count} emails found.")
        
        batch_size = 10
        batchProcessEmails(mails, total_count, batch_size, window)
        
        print(f"{total_count} emails processed.")
        print("Processing Complete!")
        window['-EMAIL_COUNT-'].update(f"{total_count} emails processed.")
        window['-PROGRESS-'].update('Processing Complete!')

def main():
    layout = [
        [sg.Text('Email Assistant', font=('Helvetica', 20))],
        [sg.Button('Fetch and Filter Emails', key='-FETCH-', size=(20, 2))],
        [sg.Text('', size=(30, 2), key='-EMAIL_COUNT-')],
        [sg.Text('', size=(30, 2), key='-PROGRESS-')],
        [sg.Exit()]
    ]

    window = sg.Window('Email Assistant GUI', layout, finalize=True)

    while True:
        event, values = window.read()
        
        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        
        if event == '-FETCH-':
            threading.Thread(target=fetch_and_filter_emails, args=(window,), daemon=True).start()
        
        if event == '-UPDATE-':
            count, total_emails = values[event]
            window['-PROGRESS-'].update(f'Processing: {count}/{total_emails} emails')

    window.close()

if __name__ == "__main__":
    main()
