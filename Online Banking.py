import random
import re

class Account:
    # Constructor
    def __init__(self, cardId, userName, passWord, quotaMoney):
        self.cardId = cardId
        self.userName = userName
        self.passWord = passWord
        self.quotaMoney = quotaMoney
        self.money = 0  # Initialize money to 0

    # Get methods
    def getCardId(self):
        return self.cardId

    def getUserName(self):
        return self.userName
    
    def getPassWord(self):
        return self.passWord
    
    def getQuotaMoney(self):
        return self.quotaMoney
    
    def getMoney(self):
        return self.money
    
    # Set methods
    def setCardId(self, cardId):
        self.cardId = cardId

    def setUserName(self, userName):
        self.userName = userName
    
    def setPassWord(self, passWord):
        self.passWord = passWord
    
    def setQuotaMoney(self, quotaMoney):
        self.quotaMoney = quotaMoney

    def setMoney(self, money):
        self.money = money


def main(Account_List):
    print("")
    print("==================Welcome to Home Page======================")
    while True:
        print("\nPlease enter the action you want to do:")
        print("1) Sign In")
        print("2) Open an Account")
        print("3) Quit")
        Input = int(input("Select Your Option: "))

        if Input == 1:
            Login(Account_List)
        elif Input == 2:
            Register(Account_List)
        elif Input == 3:
            print("See you Next Time")
            break
        else:
            print("The command that currently entered is not supported\n")


def Register(Account_List):
    passWord = " "
    print("")
    print("==================User Account Registration======================")
    
    while True:
        name = input("Enter Account Name: ")
        if any(account.getUserName() == name for account in Account_List):
            print("User Name already exists!")
            print(" ")
        else:
            break

    while True:
        passWord = input("Enter Account Password: ")
        confirmPassword = input("Enter Your Confirmation Password: ")

         # Check if the password meets the complexity requirements
        if (len(passWord) >= 8 and                    # Minimum length of 8 characters
            re.search(r'[a-z]', passWord) and          # At least one lowercase letter
            re.search(r'[A-Z]', passWord) and          # At least one uppercase letter
            re.search(r'[0-9]', passWord) and          # At least one number
            re.search(r'[@$!%*?&#]', passWord)):       # At least one special character
            if confirmPassword == passWord:
                print("Password has been created")
                print(" ")
                break  # Exit the loop if passwords match
            else:
                print("Passwords must be the same")
                print(" ")
        else:
            print("Password must be at least 8 characters long and include:")
            print(" - At least one lowercase letter")
            print(" - At least one uppercase letter")
            print(" - At least one number")
            print(" - At least one special character (@$!%*?&#)")
            print(" ")

    quotaMoney = float(input("Enter the current limit: ")) 

    # Generate the card number of 8 digits and ensure it's unique
    cardId = create_cardId(Account_List)

    account = Account(cardId, name, passWord, quotaMoney)
    Account_List.append(account)

    print(f"Account has been successfully created. The card number is: {account.getCardId()}")
    print(" ")


# Function to create a unique 8-digit card ID
def create_cardId(Account_List):
    while True:
        cardId = ''.join([str(random.randint(0, 9)) for _ in range(8)])  # Generate an 8-digit random number
        if all(account.getCardId() != cardId for account in Account_List):
            return cardId

# Function to get an account by its card ID
def getAccountByCardId(cardId, Account_List):
    for account in Account_List:
        if account.getCardId() == cardId:
            return account
    return None


# Function to handle user login
def Login(Account_List):
    print("\n==================User login function======================")

    if not Account_List:
        print("There is no account in the current system. You need to register first!\n")
        return

    while True:
        cardId = input("Enter login card number: ")
        account = getAccountByCardId(cardId, Account_List)

        if account:
            while True:
                passWord = input("Enter login password: ")
                if account.getPassWord() == passWord:
                    print(f"{account.getUserName()} has successfully entered the system. Your card number is: {account.getCardId()}")
                    print_all(account, Account_List)
                    return
                else:
                    print("Password is incorrect")
        else:
            print("Sorry, there is no account with this card number!")


# Function to display the user interface after login
def print_all(account, Account_List):
    while True:
        print("\n==================User interface======================")
        print("1) Query")
        print("2) Deposit")
        print("3) Withdraw money")
        print("4) Transfer accounts")
        print("5) Change Password")
        print("6) Show Total Balance") 
        print("7) Sign out")
        choice = int(input("Please enter the operation command: "))

        if choice == 1:
            show_account(account)
        elif choice == 2:
            deposit_money(account)
        elif choice == 3:
            draw_money(account)
        elif choice == 4:
            transfer_money(account, Account_List)
        elif choice == 5:
            update_password(account)
        elif choice == 6:
            show_total_balance(Account_List)  # Call the total balance function
        elif choice == 7:
            print("Thank you, come again!")
            break
        else:
            print("Invalid command")

# Function to display account details
def show_account(account):
    print("\n==================Current account details======================")
    print(f"Card Number: {account.getCardId()}")
    print(f"Full Name: {account.getUserName()}")
    print(f"Balance: {account.getMoney()}")
    print(f"Current cash withdrawal limit: {account.getQuotaMoney()}")


# Function to deposit money
def deposit_money(account):
    print("\n==================Saving operation======================")
    amount = float(input("Enter the deposit amount: "))
    account.setMoney(account.getMoney() + amount)
    print("Deposit completed!")


# Function to withdraw money
def draw_money(account):
    print("\n==================Withdrawal operation======================")

    if account.getMoney() >= 100:
        while True:
            amount = float(input("Enter the withdrawal amount: "))
            if amount > account.getQuotaMoney():
                print(f"Withdrawal amount exceeds the limit of {account.getQuotaMoney()}")
            elif account.getMoney() >= amount:
                account.setMoney(account.getMoney() - amount)
                print(f"Successfully withdrew {amount}. Current balance remaining: {account.getMoney()}")
                return
            else:
                print("Insufficient balance!")
    else:
        print("Balance must exceed 100 units to withdraw")


# Function to transfer money between accounts
def transfer_money(account, Account_List):
    print("\n==================Transfer operation======================")

    if len(Account_List) < 2:
        print("There are no other accounts in the system to transfer!")
        return

    if account.getMoney() == 0:
        print("Sorry, you don't have any money to transfer")
        return

    while True:
        cardId = input("Enter the card number of the other party: ")
        target_account = getAccountByCardId(cardId, Account_List)

        if target_account and target_account.getCardId() != account.getCardId():
            confirm_name = input(f"Please confirm the name starts with [{target_account.getUserName()[1]}]: ")
            if target_account.getUserName().startswith(confirm_name):
                amount = float(input("Enter the transfer amount: "))
                if amount > account.getMoney():
                    print(f"Transfer amount exceeds your balance of {account.getMoney()}")
                else:
                    account.setMoney(account.getMoney() - amount)
                    target_account.setMoney(target_account.getMoney() + amount)
                    print(f"Transfer of {amount} to {target_account.getUserName()} successful!")
                    return
            else:
                print("Authentication information error")
        else:
            print("Error with the transfer card number entered!")

# Function to update account password
def update_password(account):
    print("\n==================Change Password======================")

    while True:
        current_password = input("Enter current password: ")
        if account.getPassWord() == current_password:
            while True:
                new_password = input("Enter a new password: ")
                confirm_password = input("Enter confirmation password: ")

                if new_password == confirm_password:
                    account.setPassWord(new_password)
                    print("Password successfully updated!")
                    return
                else:
                    print("The passwords entered are inconsistent")
        else:
            print("The current password entered is incorrect")

# Function to show total balance of all accounts
def show_total_balance(Account_List):
    total_balance = sum(account.getMoney() for account in Account_List)
    print(f"\n==================Total Balance======================")
    print(f"Total balance across all accounts: {total_balance}")


# Main program entry point
if __name__ == "__main__":
    Account_List = []
    main(Account_List)
