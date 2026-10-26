def validate_price(price_cents):
    if price_cents <= 0:
        raise ValueError("price must be greater than zero")
    return price_cents
