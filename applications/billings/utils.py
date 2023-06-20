from decimal import Decimal


def calculate_balances(transactions):
    balances = {}

    for transaction in transactions:
        user = transaction['user']
        amount = transaction['amount']
        paid_by = transaction['paid_by']

        # Update the balances for the users
        if user not in balances:
            balances[user] = Decimal('0.00')
        if paid_by not in balances:
            balances[paid_by] = Decimal('0.00')

        balances[user] -= amount
        balances[paid_by] += amount

    # Construct the final list of transactions
    final_transactions = []
    for transaction in transactions:
        user = transaction['user']
        amount = transaction['amount']
        paid_by = transaction['paid_by']

        if user in balances and balances[user] < 0:
            # The user owes money
            diff = min(amount, abs(balances[user]))
            transaction['amount'] -= diff
            balances[user] += diff
            balances[paid_by] -= diff

            if transaction['amount'] > 0:
                final_transactions.append(transaction)

    return final_transactions