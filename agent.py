import os.path
import schedule
import time
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# UPDATED SCOPES: Added 'gmail.send' so the bot can email you!
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

def get_gmail_service():
    """Authenticates and returns the Gmail service."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def send_email_to_self(service, subject, body_text):
    """Sends an email to your own account."""
    try:
        # get user's email address
        profile = service.users().getProfile(userId='me').execute()
        my_email = profile['emailAddress']

        message = MIMEText(body_text)
        message['to'] = my_email
        message['from'] = my_email
        message['subject'] = subject

        # Encode the message (Base64url)
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        body = {'raw': raw_message}

        service.users().messages().send(userId="me", body=body).execute()
        print(f"✅ Email sent successfully to {my_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def job():
    print("\n⏰ Waking up to scan...")
    try:
        service = get_gmail_service()
        
        TARGET_LABEL_ID = "Label_5376955759611575572" 
        
        # Search Inbox + Label
        results = service.users().messages().list(
            userId="me", 
            labelIds=["INBOX", TARGET_LABEL_ID], 
            maxResults=40
        ).execute()
        messages = results.get("messages", [])

        # Start building the summary text
        daily_summary = "Here is your Daily AI Project Summary:\n\n"
        email_count = 0

        if messages:
            email_count = len(messages)
            daily_summary += f"🔥 Found {email_count} active items in Inbox:\n"
            daily_summary += "-"*40 + "\n"
            
            # Process emails and add to summary string
            for msg in messages:
                msg_detail = service.users().messages().get(userId="me", id=msg['id']).execute()
                headers = msg_detail['payload']['headers']
                
                subject = "No Subject"
                sender = "Unknown"
                for h in headers:
                    if h['name'] == 'Subject': subject = h['value']
                    if h['name'] == 'From': sender = h['value']
                
                snippet = msg_detail.get('snippet', '')
                
                # Append to our big text block
                daily_summary += f"📧 FROM: {sender}\n"
                daily_summary += f"📝 SUBJ: {subject}\n"
                daily_summary += f"📄 BODY: {snippet[:200]}...\n"
                daily_summary += "-"*40 + "\n"
        else:
            daily_summary += "✅ No active project emails found in Inbox today.\n"

        # ALWAYS print to screen (for debugging)
        print(daily_summary)

        # SEND THE EMAIL
        send_email_to_self(service, f"Daily Update: {email_count} Items Found", daily_summary)

    except Exception as e:
        print(f"Error: {e}")

# Run immediately to test the email sending
job()

# Schedule for 8:00 AM
print("...Scheduler is live. Waiting for 08:00 AM...")
schedule.every().day.at("08:00").do(job) 

while True:
    schedule.run_pending()
    time.sleep(60)