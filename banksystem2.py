import json
import os
from datetime import datetime

FILENAME = "bank_data.json"


if os.path.exists(FILENAME):
    with open(FILENAME, "r") as f:
        data = json.load(f)
        bank = data.get("bank", {})
        account_number = data.get("account_number", 1001)
        transfers = data.get("transfers", [])
else:
    bank = {}
    account_number = 1001
    transfers = []



def save_data():
    with open(FILENAME, "w") as f:
        json.dump({
            "bank": bank,
            "account_number": account_number,
            "transfers": transfers
        }, f, indent=4)


def open_account():
    global account_number
    name = input("Enter Name: ")
    amount = float(input("Enter Opening Balance: "))

    bank[str(account_number)] = {
        "name": name,
        "balance": amount
    }

    print("\n✅ Account Created Successfully!")
    print("Account Number:", account_number)

    account_number += 1
    save_data()



def deposit():
    acc = input("Enter Account Number: ")
    if acc in bank:
        amt = float(input("Enter Deposit Amount: "))
        bank[acc]["balance"] += amt
        print("💰 Deposit Successful!")
        save_data()
    else:
        print("❌ Account Not Found!")



def withdraw():
    acc = input("Enter Account Number: ")
    if acc in bank:
        amt = float(input("Enter Withdraw Amount: "))
        if bank[acc]["balance"] >= amt:
            bank[acc]["balance"] -= amt
            print("💸 Withdrawal Successful!")
            save_data()
        else:
            print("❌ Insufficient Balance!")
    else:
        print("❌ Account Not Found!")



def check_balance():
    acc = input("Enter Account Number: ")
    if acc in bank:
        print(f"💳 Current Balance: ₹{bank[acc]['balance']}")
    else:
        print("❌ Account Not Found!")



def transfer_money():
    sender = input("Sender Account Number: ")
    receiver = input("Receiver Account Number: ")

    if sender in bank and receiver in bank:
        amt = float(input("Enter Amount to Transfer: "))

        if bank[sender]["balance"] >= amt:
            bank[sender]["balance"] -= amt
            bank[receiver]["balance"] += amt

            transfers.append({
                "from": sender,
                "to": receiver,
                "amount": amt,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            })

            print("🔁 Transfer Successful!")
            save_data()
        else:
            print("❌ Insufficient Balance!")
    else:
        print("❌ One or both accounts not found!")



def transfer_history():
    acc = input("Enter Account Number: ")
    found = False

    print("\n--- Transfer History ---")
    for t in transfers:
        if t["from"] == acc or t["to"] == acc:
            print(f"{t['time']} | {t['from']} → {t['to']} | ₹{t['amount']}")
            found = True

    if not found:
        print("No transfer history found!")



def delete_account():
    acc = input("Enter Account Number: ")
    if acc in bank:
        del bank[acc]
        print("🗑 Account Deleted Successfully!")
        save_data()
    else:
        print("❌ Account Not Found!")



while True:
    print("\n========== BANK MENU ==========")
    print("1. Open Account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Check Balance")
    print("5. Transfer Money")
    print("6. Transfer History")
    print("7. Delete Account")
    print("8. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        open_account()
    elif choice == "2":
        deposit()
    elif choice == "3":
        withdraw()
    elif choice == "4":
        check_balance()
    elif choice == "5":
        transfer_money()
    elif choice == "6":
        transfer_history()
    elif choice == "7":
        delete_account()
    elif choice == "8":
        print("👋 Thank You for Using Bank System")
        break
    else:
        print("❌ Invalid Choice!")
