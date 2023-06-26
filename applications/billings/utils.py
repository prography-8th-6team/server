from decimal import Decimal


def calculate_balances(transactions):
    for i, t1 in enumerate(transactions):
        for j, t2 in enumerate(transactions[i + 1:], i + 1):
            if t1["user"] == t2["paid_by"] and t1["paid_by"] == t2["user"]:
                t1["amount"] -= t2["amount"]
                t2["amount"] = 0

    reduced_transactions = []

    for t in transactions:
        if t['amount'] == 0:
            continue
        if t["amount"] < 0:
            t["user"], t["paid_by"] = t["paid_by"], t["user"]
            t["amount"] *= -1
        if t["amount"] > 0:
            reduced_transactions.append(t)
    return reduced_transactions


def calculate_user_amounts(transactions):
    user_amounts = {}

    for t in transactions:
        user = t["user"]
        amount = t["amount"]
        paid_by = t["paid_by"]

        if user not in user_amounts:
            user_amounts[user] = 0
        if paid_by not in user_amounts:
            user_amounts[paid_by] = 0

        user_amounts[user] -= amount
        user_amounts[paid_by] += amount

    result = [{"user": str(k), "amount": v} for k, v in user_amounts.items()]
    return result
