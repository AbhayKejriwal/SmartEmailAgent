import GmailAPI as ml
import EmailAsst as astn
import json
import PySimpleGUI as sg


def createInitialLabels():
    ml.create_label("Priority", "#000000", "#cc3a21")
    ml.create_label("Not Important", "#000000", "#ffad47")
    ml.create_label("Useless", "#000000", "#4a86e8")


def processEmails(emails, window, count, total_emails):
    for email in emails:
        response = astn.generate(str(email))
        res = json.loads(response)  # Parse the JSON string into a dictionary

        email['Summary'] = res['Summary']
        email['Category'] = res['Category']

        if res['Category'] != 'Cannot Classify':
            ml.addLabels(email, [res['Category']])
            if res['Category'] != 'Priority':
                ml.removeLabels(email, ['INBOX'])
        
        # Update the progress in the GUI
        window['-PROGRESS-'].update(f'Processing: {count}/{total_emails} emails')
        count += 1

    return count



def main():
    layout = [
        [sg.Text('Email Assistant', font=('Helvetica', 16))],
        [sg.Button('Fetch and Filter Emails', key='-FETCH-', size=(20, 1))],
        [sg.Text('', size=(30, 1), key='-EMAIL_COUNT-')],
        [sg.Text('', size=(30, 1), key='-PROGRESS-')],
        [sg.Exit()]
    ]

    window = sg.Window('Email Assistant GUI', layout)

    while True:
        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Exit'):
            break
        
        if event == '-FETCH-':
            labels = ['INBOX']  # this line specifies the label of the emails to be read
            state = "is:unread"  # this line specifies the state of the emails to be read
            
            mails = ml.listEmails(labels, state)
            batch_size = 10

            if not mails:
                window['-EMAIL_COUNT-'].update("No emails found.")
            else:
                total_count= len(mails)
                window['-EMAIL_COUNT-'].update(f"{total_count} emails found.")
                
                count = 1
                for i in range(0, total_count, batch_size):
                    batch = mails[i:i+batch_size]
                    emails = ml.getEmails(batch)
                    count = processEmails(emails, window, count, total_count)
                else:
                    window['-EMAIL_COUNT-'].update(f"{total_count} emails processed.")
                    window['-PROGRESS-'].update('Processing Complete!')

    window.close()

if __name__ == "__main__":
    main()
