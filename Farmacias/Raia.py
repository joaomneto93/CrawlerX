class DrogaRaia:

    def __init__(self):
        self.lista_abas = ["https://www.drogaraia.com.br/medicamentos.html?limit=48",
                      "https://www.drogaraia.com.br/bem-estar.html?limit=48",
                      "https://www.drogaraia.com.br/mamae-e-bebe.html?limit=48",
                      "https://www.drogaraia.com.br/beleza.html?limit=48",
                      "https://www.drogaraia.com.br/cabelo.html?limit=48",
                      "https://www.drogaraia.com.br/higiene-pessoal.html?limit=48"]
        self.brand_xpath = "//div[@class='product-attributes']//li[@class='marca show-hover']/text()"
        self.old_price_xpath = "//div[@class='price-info']//div[@class='price-box']/span//p[@class='old-price']/span[2]/text()[2]"
        self.wholesale_price_xpath = "//div[@class='product_label raia-arrasa']//span[@class='price']/text()"
        self.price_xpath = "//div[@class='price-info']//div[@class='price-box']//p[@class='special-price']/" \
                           "span/span[2]/text()"
        self.price_xpath2 = "//div[@class='price-info']//div[@class='price-box']//span[@class='regular-price ']/" \
                            "span[2]/text()"
        self.ean_xpath = "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()"
        self.titles_xpath = "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']"
        self.next_xpath = '//a[@title="Próximo"]'
        self.filename = 'droga_raia.csv'
