from Tela.menu_flow import menu_flow
import os
try:
    os.mkdir('Arquivos')
except OSError:
    print('Diretório --Arquivos-- já existente')

raia = {'tabs': ["https://www.drogaraia.com.br/medicamentos.html?limit=48",
                 "https://www.drogaraia.com.br/bem-estar.html?limit=48",
                 "https://www.drogaraia.com.br/mamae-e-bebe.html?limit=48",
                 "https://www.drogaraia.com.br/beleza.html?limit=48",
                 "https://www.drogaraia.com.br/cabelo.html?limit=48",
                 "https://www.drogaraia.com.br/higiene-pessoal.html?limit=48"],
        'titles': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
        'urls': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
        'brand': "//div[@class='product-attributes']//li[@class='marca show-hover']/text()",
        'old': "//div[@class='price-info']//div[@class='price-box']/span//p[@class='old-price']/span["
               "2]/text()[2]",
        'wholesale': "//div[@class='product_label raia-arrasa']//span[@class='price']/text()",
        'price': "//div[@class='price-info']//div[@class='price-box']//p[@class='special-price']/"
                 "span/span[2]/text()",
        'price2': "//div[@class='price-info']//div[@class='price-box']//span[@class='regular-price ']/"
                  "span[2]/text()",
        'ean': "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()",
        'next': '//div[@class="pages inline"]/ol//a[text()="{}"]',
        'filename': 'Arquivos/droga_raia {}.csv'}

qualidoc = {'tabs': ["https://www.drogaraia.com.br/medicamentos.html?limit=48",
                     "https://www.drogaraia.com.br/bem-estar.html?limit=48",
                     "https://www.drogaraia.com.br/mamae-e-bebe.html?limit=48",
                     "https://www.drogaraia.com.br/beleza.html?limit=48",
                     "https://www.drogaraia.com.br/cabelo.html?limit=48",
                     "https://www.drogaraia.com.br/higiene-pessoal.html?limit=48"],
            'titles': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
            'urls': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
            'brand': "//div[@class='product-attributes']//li[@class='marca show-hover']/text()",
            'old': "//div[@class='price-info']//div[@class='price-box']/span//p[@class='old-price']/span["
                   "2]/text()[2]",
            'wholesale': "//div[@class='product_label raia-arrasa']//span[@class='price']/text()",
            'price': "//div[@class='price-info']//div[@class='price-box']//p[@class='special-price']/"
                     "span/span[2]/text()",
            'price2': "//div[@class='price-info']//div[@class='price-box']//span[@class='regular-price ']/"
                      "span[2]/text()",
            'ean': "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()",
            'next': '//a[@title="Próximo"]',
            'filename': 'Arquivos/qualidoc {}.csv'}

farma_delivery = {'tabs': ["https://www.drogaraia.com.br/medicamentos.html?limit=48",
                           "https://www.drogaraia.com.br/bem-estar.html?limit=48",
                           "https://www.drogaraia.com.br/mamae-e-bebe.html?limit=48",
                           "https://www.drogaraia.com.br/beleza.html?limit=48",
                           "https://www.drogaraia.com.br/cabelo.html?limit=48",
                           "https://www.drogaraia.com.br/higiene-pessoal.html?limit=48"],
                  'titles': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
                  'urls': "//div[@class='product-info']/div[@class='product-name']/a[@class='show-hover']",
                  'brand': "//div[@class='product-attributes']//li[@class='marca show-hover']/text()",
                  'old': "//div[@class='price-info']//div[@class='price-box']/span//p[@class='old-price']/span["
                         "2]/text()[2]",
                  'wholesale': "//div[@class='product_label raia-arrasa']//span[@class='price']/text()",
                  'price': "//div[@class='price-info']//div[@class='price-box']//p[@class='special-price']/"
                           "span/span[2]/text()",
                  'price2': "//div[@class='price-info']//div[@class='price-box']//span[@class='regular-price ']/"
                            "span[2]/text()",
                  'ean': "//*[@id='product-attribute-specs-table']/tbody/tr[2]/td/text()",
                  'next': '//a[@title="Próximo"]',
                  'filename': 'Arquivos/farma_delivery {}.csv'}

ultra_farma = {'tabs': ["https://www.ultrafarma.com.br/categoria/medicamentos?resultsperpage=90&sortby=relevance",
                        "https://www.ultrafarma.com.br/categoria/genericos?resultsperpage=90&sortby=relevance",
                        "https://www.ultrafarma.com.br/categoria/saude-e-bem-estar?resultsperpage=90&sortby=relevance",
                        "https://www.ultrafarma.com.br/categoria/beleza?resultsperpage=90&sortby=relevance",
                        "https://www.ultrafarma.com.br/categoria/dermocosmeticos?resultsperpage=90&sortby=relevance",
                        "https://www.ultrafarma.com.br/categoria/cuidados-diarios?resultsperpage=90&sortby=relevance",
                        "https://www.ultrafarma.com.br/categoria/infantil?resultsperpage=90&sortby=relevance"],
               'titles': "//*[@id='produtos-placeholder']/div/div/div/div/div/div/a[2]/h3",
               'urls': '//*[@id="produtos-placeholder"]/div/div/div/div/div/div/a[2]',
               'brand': "//*[@id='container']/section[1]/div[1]/div/div[2]/div/div[2]//span[@class='brandName']/a/text()",
               'old': "//*[@id='container']/section[1]//div[@class='product-price']/p[@class='product-price-old']/del/text()",
               'wholesale': "//*[@id='container']/section[1]/div[1]/div/div[2]/div/div[2]/ul/li[1]/img/@title",
               'price': "//*[@id='container']/section[1]//div[@class='product-price']/p[@class='product-price-new']/span[2]/text()",
               'price2': "//*[@id='container']/section[1]/div[1]/div/div[2]/div/div[2]/div[2]/p[2]/span[2]/text()",
               'ean': "//*[@id='pdp-section-outras-informacoes']/div/ul/li[2]/span/@data-attr-value",
               'next': '//ul[@class="pagination pagination-vitrine"]/li/a[text()="{}"]',
               'filename': 'Arquivos/ultrafarma {}.csv'}

company_list = [raia, qualidoc, farma_delivery, ultra_farma]

if __name__ == '__main__':
    menu_flow(company_list)
