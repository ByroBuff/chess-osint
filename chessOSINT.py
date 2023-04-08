import requests
from bs4 import BeautifulSoup
import sys
import argparse



def getMember(username):
    memberURL = f"https://www.chess.com/member/{username}"
    mailURL = f"https://www.chess.com/callback/recover-password-data/{username}"

    try:
        memberPage = requests.get(memberURL)
        mailPage = requests.get(mailURL).json()
    except:
        print("Member does not exist or you do not have wifi")
        return
    
    memberContent = BeautifulSoup(memberPage.content, 'html.parser')

    country = memberContent.find("div", class_="country-flags-component")
    try:
        location = memberContent.find("div", class_="profile-card-location").findChild("div").text.strip("\n").strip(" ")
    except:
        location = "UNAVAILABLE\n"

    try:
        name = memberContent.find("div", class_="profile-card-name").text
    except:
        name = "UNAVAILABLE"

    print("---" + username + "---")

    print("Name      :  " + name)
    print("Country   :  " + country["v-tooltip"])
    print("Location  :  " + location, end="")
    print("Email     :  " + mailPage["email"])

def getEmail(email):
    emailURL = f"https://www.chess.com/callback/email/exist?email={email}"

    try:
        emailPage = requests.get(emailURL)

        if emailPage.status_code == 404:
            print("No user has this email address")
        else:
            print( "A user with this email exists")

    except:
        print("Connect to wifi and try again")


    



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process email or username')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--email', type=str, help='email to process')
    group.add_argument('--username', type=str, help='username to process')

    args = parser.parse_args()

    if args.username:
        getMember(args.username)
        
    elif args.email:
        getEmail(args.email)


