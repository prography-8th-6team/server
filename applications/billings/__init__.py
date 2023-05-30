class BillingLineCategory:
    FOOD = 'food'
    TRANSPORTATION = 'transportation'
    HOTEL = 'hotel'
    MARKET = 'market'
    SHOPPING = 'shopping'
    OTHER = 'other'

    CHOICES = (
        (FOOD, 'food'),
        (TRANSPORTATION, 'transportation'),
        (HOTEL, 'hotel'),
        (MARKET, 'market'),
        (SHOPPING, 'shopping'),
        (OTHER, 'other')
    )


class SettlementStatus:
    CHARGED = 'charged'
    PARTIALLY_CHARGED = 'partially_charged'
    NOT_CHARGED = 'not_charged'

    CHOICES = (
        (CHARGED, 'charged'),
        (PARTIALLY_CHARGED, 'partially_charged'),
        (NOT_CHARGED, 'not_charged')
    )


class Color:
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'

    CHOICES = (
        (RED, 'red'),
        (BLUE, 'blue'),
        (GREEN, 'green'),
    )


class CurrencyType:
    USD = 'USD'
    EUR = 'EUR'
    KRW = 'KRW'

    CHOICES = (
        (USD, 'USD'),
        (EUR, 'EUR'),
        (KRW, 'KRW')
    )
