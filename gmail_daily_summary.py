"""
Gmail Daily Summary Agent
Run via Windows Task Scheduler at 8:00 AM daily.

Setup instructions at bottom of file.
"""

import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send"
]

# Your label ID - update if needed
TARGET_LABEL_ID = "Label_5376955759611575572"


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
    profile = service.users().getProfile(userId='me').execute()
    my_email = profile['emailAddress']

    message = MIMEText(body_text)
    message['to'] = my_email
    message['from'] = my_email
    message['subject'] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
    print(f"✅ Email sent to {my_email}")


def run_daily_summary():
    """Main function - scans inbox and sends summary."""
    print("🔍 Scanning Gmail...")
    
    service = get_gmail_service()
    
    results = service.users().messages().list(
        userId="me", 
        labelIds=["INBOX", TARGET_LABEL_ID], 
        maxResults=40
    ).execute()
    messages = results.get("messages", [])

    daily_summary = "Here is your Daily AI Project Summary:\n\n"
    email_count = 0

    if messages:
        email_count = len(messages)
        daily_summary += f"🔥 Found {email_count} active items in Inbox:\n"
        daily_summary += "-" * 40 + "\n"
        
        for msg in messages:
            msg_detail = service.users().messages().get(userId="me", id=msg['id']).execute()
            headers = msg_detail['payload']['headers']
            
            subject = "No Subject"
            sender = "Unknown"
            for h in headers:
                if h['name'] == 'Subject':
                    subject = h['value']
                if h['name'] == 'From':
                    sender = h['value']
            
            snippet = msg_detail.get('snippet', '')
            
            daily_summary += f"📧 FROM: {sender}\n"
            daily_summary += f"📝 SUBJ: {subject}\n"
            daily_summary += f"📄 BODY: {snippet[:200]}...\n"
            daily_summary += "-" * 40 + "\n"
    else:
        daily_summary += "✅ No active project emails found in Inbox today.\n"

    print(daily_summary)
    send_email_to_self(service, f"Daily Update: {email_count} Items Found", daily_summary)
    print("✅ Done!")


if __name__ == "__main__":
    run_daily_summary()


# =============================================================================
# WINDOWS TASK SCHEDULER SETUP
# =============================================================================
#
# 1. Open Task Scheduler (search "Task Scheduler" in Windows)
#
# 2. Click "Create Basic Task" in the right panel
#
# 3. Name it: "Gmail Daily Summary"
#    Description: "Scans tagged emails and sends morning summary"
#    Click Next
#
# 4. Trigger: Select "Daily"
#    Click Next
#
# 5. Set start time: 8:00:00 AM
#    Recur every: 1 days
#    Click Next
#
# 6. Action: Select "Start a program"
#    Click Next
#
# 7. Program/script: Your python.exe path
#    (Find it by running: where python)
#
# 8. Add arguments:
#    gmail_daily_summary.py
#
# 9. Start in:
#    Your project folder (where credentials.json lives)
#
# 10. Click Finish
#
# 11. IMPORTANT: Right-click the task > Properties >
#     Check "Run whether user is logged on or not"
#     Check "Run with highest privileges"
#
# =============================================================================
# TO TEST IT NOW
# =============================================================================
#
# In PowerShell, navigate to your project folder and run:
#     python gmail_daily_summary.py
#
# If it works manually, Task Scheduler will work too.
# =============================================================================