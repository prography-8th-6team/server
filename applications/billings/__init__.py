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


class PaymentStatus:
    CHARGED = 'charged'
    PARTIALLY_CHARGED = 'partially_charged'
    NOT_CHARGED = 'not_charged'

    CHOICES = (
        (CHARGED, 'charged'),
        (PARTIALLY_CHARGED, 'partially_charged'),
        (NOT_CHARGED, 'not_charged')
    )
