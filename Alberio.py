#Created by Menuka Wijayarathne 2023-09-21
import warnings
import paramiko
import time
import smtplib
from email.mime.text import MIMEText
import pymongo
from datetime import datetime

def execute_remote_command_with_delay(hostname, username, password, command, delay_seconds=4):
    try:
        # Create an SSH client instance
        client = paramiko.SSHClient()

        # Automatically add the server's host key (not recommended for production use)
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the remote server using the provided credentials
        client.connect(hostname, username=username, password=password)

        # Start an interactive shell session
        shell = client.invoke_shell()

        # Wait for the shell to start (you can adjust the delay)
        time.sleep(2)

        # Execute the 'pool list' command within the shell
        shell.send(command + '\n')

        # Wait for the command to complete (you can adjust the delay)
        time.sleep(delay_seconds)

        # Read the command output
        output = shell.recv(4096).decode('utf-8')

        # Close the SSH connection
        client.close()

        return output
    except Exception as e:
        return str(e)

def send_email(subject, body):
    # Email configuration
    smtp_server = '10.210.6.82'
    smtp_port = 25  # Port for plain SMTP without TLS/SSL
    sender_email = 'nexenta.alberio@dialog.lk'
    recipient_email = 'nfvcloudops@dialog.lk'

    # Create the email message
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Send the email without TLS/SSL
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(sender_email, [recipient_email], msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

if __name__ == "__main__":
    # Suppress paramiko.SSHException warnings
    warnings.filterwarnings("ignore", category=UserWarning)

    # Define the remote server details
    remote_hostname = '10.108.129.40'  # Update with your server's IP address or hostname
    remote_username = 'admin'         # Update with your SSH username
    remote_password = 'Nexenta1!'       # Update with your SSH password
    
    # Command to execute on the remote server
    
    command_to_execute='pool list -O units=G,basic'
    # Execute the remote command with a 4-second delay
    result = execute_remote_command_with_delay(remote_hostname, remote_username, remote_password, command_to_execute, delay_seconds=10)
    print(result)

    lines = result.split('\n')
    for i, line in enumerate(lines):
        if "hapool1" in line:
            # Extract the three columns (1st, 2nd, and 3rd) from the line
            columns = line.split()
            if len(columns) == 9: 

                extracted_columns = [columns[0], columns[3],columns[4]]
                X =' '.join(extracted_columns)
                Y = columns[3]
                Z = columns[4]
                print(Y)
                print(X)
                print(Z)
                #print(' '.join(extracted_columns))
#Nexenta
#alberio
                    # Connect to MongoDB (assuming MongoDB is running locally on default port 27017)
                client = pymongo.MongoClient("mongodb://localhost:27017/")

                # Specify the database and collection
                db = client["alberio"]  # Replace with your database name
                collection = db["alberio"]  # Replace with your collection name

                # Create a document with timestamp and free storage
                document = {
                    "time": datetime.now(),
                    "free storage": Y
                }

                collection.insert_one(document)


    # Send the extracted output via email
    email_subject = f'CEE | Alberio free space = {Y}|  precentage = {Z}'
    send_email(email_subject, X)
 
