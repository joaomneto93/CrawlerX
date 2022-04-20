class Farmacia:

    def __init__(self, tab_list: list, brand: str, old_price: str, wholesale: str, price1: str, price2: str,
                 ean: str, titles: str, next_: str, filename: str):
        self.tab_list = tab_list
        self.brand_xpath = brand
        self.old_price_xpath = old_price
        self.wholesale_price_xpath = wholesale
        self.price_xpath = price1
        self.price_xpath2 = price2
        self.ean_xpath = ean
        self.titles_xpath = titles
        self.next_xpath = next_
        self.filename = filename
