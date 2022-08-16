import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import csv

def main():
    load_dotenv()

    # env variables for login info
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    # initialize both lists.. draftOrder will be column 1 of CSV 
    # email list is column 2
    draftOrder = []
    email_list = []

    # open the CSV file (currently hardcoded as data.csv in current directory)
    with open('data.csv', newline='') as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        reader = csv.reader(csvfile, dialect)
        # skip headers (assumed to be present)
        next(reader)
        for row in reader:
            draftOrder.append(row[0])
            email_list.append(row[1])

    # currently not necessary
    #leagueManagerMap = {draftOrder[i]: email_list[i] for i in range (len(draftOrder))}

    # randomize player names
    random.shuffle(draftOrder)

    orderString = buildDraftOrderString(draftOrder)
    content = buildEmailBody(orderString)   
    sendEmail(content, email_list, EMAIL_ADDRESS, EMAIL_PASSWORD)


def buildDraftOrderString(draftOrder):
    count = 1
    orderString = ''
    for name in draftOrder:
        orderString = orderString + f'{count}: {name}<br>'
        count+=1
    
    return orderString

def buildEmailBody(orderString):
    return f'''
    <!DOCTYPE html>
    <html>
        <head>
            <header>
                
            </header>
        </head>
        <body>
            <div style="width: fit-content; margin: auto; background-color: aliceblue; padding: 30px">
            
            <h1 style="text-align: center;  ">Insert your title here</h1> 
            <p>
                {orderString}  
            </p>
        </div>
        </body>
    </html>
    ''' 
def sendEmail(content, email_list, email_address, password):
    msg = EmailMessage()
    # custom subject
    msg['Subject'] = ''
    msg['From'] = email_address
    # 'To' takes a list or single string.. in this case its a list
    msg['To'] = email_list
    msg.set_content(content, subtype='html')

    # currently set for yahoo.. change smtp server to match what you use
    with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as smtp:
        smtp.login(email_address, password)
        #uncomment this to actually send the emails
        #smtp.send_message(msg)
        smtp.close()


if __name__ == '__main__':
    main()
