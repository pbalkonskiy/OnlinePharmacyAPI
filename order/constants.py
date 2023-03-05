
# Delivery methods
SELF_DELIVERY = "Self-delivery"
DOOR_DELIVERY = "Door delivery"

DELIVERY_METHODS = [
    (SELF_DELIVERY, "Self-delivery"),
    (DOOR_DELIVERY, "Door delivery"),
]

# Payment methods
PREPAYMENT = "Prepayment"
UPON_RECEIPT = "Upon receipt"

PAYMENT_METHODS = [
    (PREPAYMENT, "Prepayment"),
    (UPON_RECEIPT, "Upon receipt"),
]

# Payment status
PENDING_PAYMENT = "Pending payment"
SUCCESSFULLY_PAID = "Successfully paid"
UPON_RECEIPT = "Payment upon receipt"

PAYMENT_STATUS = [
    (PENDING_PAYMENT, "Pending payment"),
    (SUCCESSFULLY_PAID, "Successfully paid"),
    (UPON_RECEIPT, "Payment upon receipt"),
]


WITHOUT_ACTION = "Without action"
PACKED_IN_STOCK = "Packed in stock"
ON_THE_ROAD = "On the road"
DELIVERED = "Delivered"

DELIVERY_STATUS = [
    (WITHOUT_ACTION, "Without action"),
    (PACKED_IN_STOCK, "Packed in stock"),
    (ON_THE_ROAD, "On the road"),
    (DELIVERED, "Delivered"),
]

# Here will be delivery statuses.
# Need to discuss it with BA team.
