import random
import string

# In-memory simulation store
STK_TRANSACTIONS = {}

def initiate_stk_push(phone, amount):
    transaction_ref = "STK-" + "".join(
        random.choices(string.ascii_uppercase + string.digits, k=6)
    )

    STK_TRANSACTIONS[transaction_ref] = {
        "phone": phone,
        "amount": amount,
        "status": "pending",
    }

    return {
        "message": "STK Push initiated",
        "transaction_ref": transaction_ref,
    }


def confirm_stk_payment(transaction_ref):
    transaction = STK_TRANSACTIONS.get(transaction_ref)

    if not transaction:
        return {"error": "Transaction not found"}

    transaction["status"] = "success"

    return {
        "status": "success",
        "transaction_ref": transaction_ref,
    }


def b2c_disbursement(phone, amount):
    return {
        "message": "Funds disbursed successfully",
        "phone": phone,
        "amount": amount,
    }
