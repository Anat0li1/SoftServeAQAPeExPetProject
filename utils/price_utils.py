class PriceUtils:
    def __init__(self, price_style = "american"):
        self.price_style = price_style

    def retrieve_price(self, price):
        price = price.replace("−", "-").replace("–", "-")
        match self.price_style.lower():
            case "american":
                if price.startswith("-"):
                    return -float(price.strip(" -$"))
                return float(price.strip(" $"))
            case _:
                return float(price)