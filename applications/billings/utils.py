def calculate_balances(transactions):
    for i, t1 in enumerate(transactions):
        for j, t2 in enumerate(transactions[i + 1:], i + 1):
            if t1["user"]["id"] == t2["paid_by"]["id"] and t1["paid_by"]["id"] == t2["user"]["id"]:
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

        user_id = user["id"]
        user_nickname = user["nickname"]
        paid_by_id = paid_by["id"]
        paid_by_nickname = paid_by["nickname"]

        if user_id not in user_amounts:
            user_amounts[user_id] = {"id": user_id, "nickname": user_nickname, "amount": 0}
        if paid_by_id not in user_amounts:
            user_amounts[paid_by_id] = {"id": paid_by_id, "nickname": paid_by_nickname, "amount": 0}

        user_amounts[user_id]["amount"] -= amount
        user_amounts[paid_by_id]["amount"] += amount

    result = list(user_amounts.values())

    positive_total_amount = sum([i['amount'] for i in result if i['amount'] > 0])

    for t in user_amounts.values():
        t["amount"] = (t["amount"] / positive_total_amount) * 100 if t['amount'] != 0 else 0
    return result
