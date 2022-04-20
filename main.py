from Tela.menu_flow import menu_flow

raia = {'tabs': ["https://www.drogaraia.com.br/medicamentos.html?limit=48",
                       "https://www.drogaraia.com.br/bem-estar.html?limit=48",
                       "https://www.drogaraia.com.br/mamae-e-bebe.html?limit=48",
                       "https://www.drogaraia.com.br/beleza.html?limit=48",
                       "https://www.drogaraia.com.br/cabelo.html?limit=48",
                       "https://www.drogaraia.com.br/higiene-pessoal.html?limit=48"],
        'brand': "//div[@class='product-attributes']//li[@class='marca show-hover']/text()",
        'old': "//div[@class='price-info']//div[@class='price-box']/span//p[@class='old-price']/span["
                           "2]/text()[2]",
        'wholesale': "//div[@class='product_label raia-arrasa']//span[@class='price']/text()",
        'price': "//div[@class='price-info']//div[@class='price-box']//p[@class='special-price']/"
                       "span/span[2]/text()",
        'price2': "//div[@class='price-info']//div[@class='price-box']//span[@class='regular-price ']/"
                        "span[2]/text()",
        'ean': "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()",
        'titles': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
        'next': '//a[@title="Próximo"]',
        'filename': 'droga_raia.csv'}

qualidoc = {'tabs': ["https://www.drogaraia.com.br/medicamentos.html?limit=48",
                       "https://www.drogaraia.com.br/bem-estar.html?limit=48",
                       "https://www.drogaraia.com.br/mamae-e-bebe.html?limit=48",
                       "https://www.drogaraia.com.br/beleza.html?limit=48",
                       "https://www.drogaraia.com.br/cabelo.html?limit=48",
                       "https://www.drogaraia.com.br/higiene-pessoal.html?limit=48"],
        'brand': "//div[@class='product-attributes']//li[@class='marca show-hover']/text()",
        'old': "//div[@class='price-info']//div[@class='price-box']/span//p[@class='old-price']/span["
                           "2]/text()[2]",
        'wholesale': "//div[@class='product_label raia-arrasa']//span[@class='price']/text()",
        'price': "//div[@class='price-info']//div[@class='price-box']//p[@class='special-price']/"
                       "span/span[2]/text()",
        'price2': "//div[@class='price-info']//div[@class='price-box']//span[@class='regular-price ']/"
                        "span[2]/text()",
        'ean': "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()",
        'titles': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
        'next': '//a[@title="Próximo"]',
        'filename': 'droga_raia.csv'}

farma_delivery = {'tabs': ["https://www.drogaraia.com.br/medicamentos.html?limit=48",
                       "https://www.drogaraia.com.br/bem-estar.html?limit=48",
                       "https://www.drogaraia.com.br/mamae-e-bebe.html?limit=48",
                       "https://www.drogaraia.com.br/beleza.html?limit=48",
                       "https://www.drogaraia.com.br/cabelo.html?limit=48",
                       "https://www.drogaraia.com.br/higiene-pessoal.html?limit=48"],
        'brand': "//div[@class='product-attributes']//li[@class='marca show-hover']/text()",
        'old': "//div[@class='price-info']//div[@class='price-box']/span//p[@class='old-price']/span["
                           "2]/text()[2]",
        'wholesale': "//div[@class='product_label raia-arrasa']//span[@class='price']/text()",
        'price': "//div[@class='price-info']//div[@class='price-box']//p[@class='special-price']/"
                       "span/span[2]/text()",
        'price2': "//div[@class='price-info']//div[@class='price-box']//span[@class='regular-price ']/"
                        "span[2]/text()",
        'ean': "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()",
        'titles': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
        'next': '//a[@title="Próximo"]',
        'filename': 'droga_raia.csv'}

ultra_farma = {'tabs': ["https://www.drogaraia.com.br/medicamentos.html?limit=48",
                       "https://www.drogaraia.com.br/bem-estar.html?limit=48",
                       "https://www.drogaraia.com.br/mamae-e-bebe.html?limit=48",
                       "https://www.drogaraia.com.br/beleza.html?limit=48",
                       "https://www.drogaraia.com.br/cabelo.html?limit=48",
                       "https://www.drogaraia.com.br/higiene-pessoal.html?limit=48"],
        'brand': "//div[@class='product-attributes']//li[@class='marca show-hover']/text()",
        'old': "//div[@class='price-info']//div[@class='price-box']/span//p[@class='old-price']/span["
                           "2]/text()[2]",
        'wholesale': "//div[@class='product_label raia-arrasa']//span[@class='price']/text()",
        'price': "//div[@class='price-info']//div[@class='price-box']//p[@class='special-price']/"
                       "span/span[2]/text()",
        'price2': "//div[@class='price-info']//div[@class='price-box']//span[@class='regular-price ']/"
                        "span[2]/text()",
        'ean': "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()",
        'titles': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
        'next': '//a[@title="Próximo"]',
        'filename': 'droga_raia.csv'}

company_list = [raia, qualidoc, farma_delivery, ultra_farma]

if __name__ == '__main__':
    menu_flow(company_list)
