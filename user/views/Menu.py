from datetime import datetime

from user.models.User import User
from user.models.UserAccounts import UserAccounts
from user.models.Transactions import Transactions


AMOUNT_DICT = {1: 500, 2: 1000, 3: 2000, 4: 5000, 5: 10000, 6: 15000, 7: 20000}
CUSTOMER_DICT = {1: "Withdraw Cash", 2: "Cash Transfer", 3: "Deposit Cash", 4: "Display Balance", 5: "Exit"}
ADMIN_DICT = {1: "Create New Account.", 2: "Delete Existing Account.", 3: "Update Account Information.",
              4: "Search for Account.", 5: "View Reports.", 6: "Exit"}


def goto_main_menu():
    aa = input("Please go to Main Menu")
    menu()


def login():
    login = input("Login: ")
    pincode = input("Pincode: ")

    user = User()
    return user.login(login, pincode)


def user_account(user):
    user_account = UserAccounts()
    return user_account.get(user.id)


def fast_withdraw():
    print("Fast Cash\n")
    options = ""
    for k, v in AMOUNT_DICT.items():
        options += "%d---%d\n" % (k, v)

    print("%s\n" % options)

    withdraw = int(input("Select one of the denominations of money: \n"))

    try:
        AMOUNT_DICT[withdraw]
    except KeyError as e:
        print(input("Invalid option please select again "))
        fast_withdraw()

    y = input("Are you sure you want to withdraw ------ (Y/N)? ")
    if y.lower() == 'n':
        customer_menu()

    return withdraw


def normal_withdraw():
    print("Normal Cash\n\n")

    withdraw = int(input("Enter the withdrawal amount: \n"))

    if withdraw < user_account.balance:
        print("You dont have sufficient balance")

    y = input("Are you sure you want to withdraw ------ (Y/N)? ")
    if y.lower() == 'n':
        customer_menu()

    return withdraw



def withdraw_cash():
    print("Withdraw Cash\n")

    print("1---Fast Cash.\n"
          "2---Normal Cash.\n\n")

    x = int(input("Please select a mode of withdrawal: "))

    if x not in [1, 2]:
        print(input("Invalid option please select again "))
        withdraw_cash()

    return x


def customer_menu():
    print("Customer Menu")

    options = ""
    for k, v in CUSTOMER_DICT.items():
        options += "%d---%s\n" %(k, v)

    print("%s\n" % options)
    x = int(input("Please select one of the above options: "))

    try:
        CUSTOMER_DICT[x]
    except KeyError as e:
        print(input("Invalid option please select again "))
        customer_menu()

    return x


def admin_menu():
    print("Administrator Menu\n\n")

    options = ""
    for k, v in ADMIN_DICT.items():
        options += "%d---%s\n" % (k, v)

    print("%s\n" % options)
    x = int(input("Please select one of the above options: "))

    try:
        ADMIN_DICT[x]
    except KeyError as e:
        print(input("Invalid option please select again "))
        admin_menu()
    return x


def create_user():
    print("Creating New Account...\n\n")
    user = User()
    user.id = str(input("user.id: "))
    user.name = str(input("Holders Name: "))
    user.login_id = str(input("Login ID: "))
    user.pincode = str(input("pincode: "))
    user.type = str(input("user type: "))
    user.save()


    user_acc = UserAccounts()
    user_acc.id = str(input("ID: "))
    user_acc.user_id = user.id
    user_acc.account_number = str(input("Account number: "))
    user_acc.balance = str(input("balance: "))
    user_acc.account_type = str(input("account type: "))
    user_acc.status = str(input("status: "))
    user_acc.save()


def delete_user(account_no):
    print("Deleting Existing account...\n\n")
    user_acc = UserAccounts()
    user_acc = user_acc.get_by_account(account_no)
    user_acc.delete()

    user = User()
    user = user.get(user_acc.user_id)
    user.delete()


def update_user(account_no):
    print("Updating account information...\n\n")

    user_acc = UserAccounts()
    user_acc = user_acc.get_by_account(account_no)

    user = User()
    user = user.get(user_acc.user_id)

    user_name = str(input("Holders Name: "))
    if user_name:
        user.name = user_name

    user_login_id = str(input("Login ID: "))
    if user_login_id:
        user.login_id = user_login_id

    user_pincode = str(input("pincode: "))
    if user_pincode:
        user.pincode = user_pincode

    user_type = str(input("user type: "))
    if user_type:
        user.type = user_type
    user.update()

    user_acc_type = str(input("account type: "))
    if user_acc_type:
        user_acc.account_type = user_acc_type

    user_acc_status = str(input("status: "))
    if user_acc_status:
        user_acc.status = user_acc_status
    user_acc.update()


def search_account_by_binarysearch(account_id):
    print("Searching for account...\n\n")
    user_acc = UserAccounts()
    user_acc = user_acc.get_all()
    account_id_found = binarySearch(user_acc, account_id)
    print(account_id_found)

    if account_id_found:
        print("User found.")
        user_account = UserAccounts()
        user_account = user_account.get_by_account(account_id)
        print(user_account)
    else:
        print("No user found")


def search_account_Amount(account_id):
    user_acc = UserAccounts()
    user_acc = user_acc.get_all_hashing()
    try:
        print(user_acc[account_id].balance)
    except KeyError as e:
        print("not found")


def search_account_by_hashing(account_id):
    user_acc = UserAccounts()
    user_acc = user_acc.get_all_hashing()
    try:
        print(user_acc[account_id].status)
    except KeyError as e:
        print("not found")

def binarySearch(alist, item):
    first = 0
    last = len(alist) - 1
    found = False

    while first <= last and not found:
        midpoint = (first + last) // 2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1

    return found


def transaction(user_account, amount, type):
    balance = int(user_account.balance)

    if type == 'withdraw':
        balance = balance - amount
    elif type == 'deposit':
        balance = balance + amount
    elif type == 'transfer':
        balance = balance - amount

    transaction = Transactions(2, user_account.id, amount, user_account.account_type, type, datetime.now(), balance)
    user_account.balance = balance
    user_account.update()
    return transaction.save()


def cash_transfer(user_account):
    print("Cash Transfer \n")

    amount = int(input("Enter amount in multiples of 500: \n"))

    account_number = int(input("Enter the account number to which you want to transfer: \n"))

    transfer_account = UserAccounts()
    transfer_account = transfer_account.get_by_account(account_number)

    transfer_user = User()
    transfer_user = transfer_user.get(transfer_account.user_id)

    print("You wish to deposit Rs ", amount, "in account held by Mr. "
          , transfer_user.name)
    x = int(input("if this information is correct please re-enter the account number: "))

    return (amount, transfer_account)


def deposit():
    print("Deposit Cash")

    amount = int(input("Enter the cash amount to deposit: "))

    return amount


def recipt(trans):
    print("Account # ", trans.account_number)
    print("Date: ", trans.date)
    print("Withdrawn: ", trans.amount )
    print("Balance: ", trans.balance)


def menu():
    print ("Welcome to Bank Mnagament System")

    user = login()
    if not user:
        print("Invalid user")
        goto_main_menu()

    if user.type == "customer":

        user_acc = user_account(user)
        if not user_acc:
            print("Invalid customer account")
            goto_main_menu()

        option = customer_menu()

        if option == 1:
            withdraw_opt = withdraw_cash()

            if withdraw_opt == 1:
                fast_opt = fast_withdraw()

                trans = transaction(user_acc, AMOUNT_DICT[fast_opt], "withdraw")
                print("Cash Successfully withdrawn!\n")

                z = input("Do you wish to print a receipt (Y/N)?")

                if z.lower() == 'y':
                    recipt(trans)

                print(input("Press enter to go back to Customer Menu "))
                customer_menu()

            elif withdraw_opt == 2:
                normal_opt = normal_withdraw()

                trans = transaction(user_acc,normal_opt,"withdraw")
                print("Cash Successfully Withdrawn! \n\n")

                z = input("Do you wish to print a receipt (Y/N)?")

                if z.lower() == 'y':
                    recipt(trans)

                print(input("Press enter to go back to Customer Menu "))
                customer_menu()

        elif option == 2:
            (transfer_opt, transfer_acc) = cash_transfer(user_acc)

            trans = transaction(user_acc, transfer_opt, 'transfer')
            print("Transaction confirmed.\n")

            transfer_acc.balance += transfer_opt
            transfer_acc.update()

            z = input("Do you wish to print a receipt (Y/N)?")

            if z.lower() == 'y':
                recipt(trans)

            print(input("Press enter to go back to Customer Menu "))
            customer_menu()

        elif option == 3:
            deposit_opt = deposit()

            trans = transaction(user_acc, deposit_opt, 'deposit')
            print("Cash deposited successfully!\n")

            z = input("Do you wish to print a receipt (Y/N)?")

            if z.lower() == 'y':
                recipt(trans)

            print(input("Press enter to go back to Customer Menu "))
            customer_menu()

        elif option == 4:
            print("Displaying Balance...\n")

            print("Account # ", user_acc.account_number)
            print("Date: ", datetime.now())
            print("Balance: ", user_acc.balance)

            print(input("Invalid option please select again "))
            customer_menu()

        elif option == 5:
            goto_main_menu()

        else:
            print("Pleas Enter the right choice. \n")

    elif user.type == "admin":
        admin_opt = admin_menu()

        if admin_opt == 1:
            create_user()

            print(input("Press enter to go back to Admin Menu "))
            admin_menu()
        elif admin_opt == 2:
            account_id = input("Enter account id to delete useraccount: ")
            delete_user(account_id)

            print(input("Press enter to go back to Admin Menu "))
            admin_menu()
        elif admin_opt == 3:
            account_id = input("Enter account id to update user information: ")
            update_user(account_id)

            print(input("Press enter to go back to Admin Menu "))
            admin_menu()
        elif admin_opt == 4:
            option = int(input("1---Binary Search\n"
                                     "2---By hashing\n"))
            if option == 1:
                user_account_id = input("Enter account id to search user information: ")
                search_account_by_binarysearch(user_account_id)
            else:
                user_account_id = input("Enter account id to search user information: ")
                search_account_by_hashing(user_account_id)
            print(input("Press enter to go back to Admin Menu "))
            admin_menu()
        elif admin_opt == 5:
            user_account_id = input("Enter account id to search user information: ")
            search_account_Amount(user_account_id)

            print(input("Press enter to go back to Admin Menu "))
            admin_menu()
        elif admin_opt == 6:
            goto_main_menu()
        else:
            print("Please enter the right choice.")
    else:
        print("please enter the right choice")




