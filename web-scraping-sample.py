from splinter import Browser
from selenium import webdriver

url = 'https://directory.fsf.org/wiki/Main_Page'
browser_engine = "chrome"
search_str = "internet"
is_headless = True

chromedriver_path = {
    'executable_path':r'C:\Users\devwarlt\Desktop\Faculdade\UNB - Pesquisador (arqs)\Web Scraping\chromedriver'
}

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

browser = Browser(
    browser_engine,
    **chromedriver_path,
    headless = is_headless,
    options = options
)

print("Acessando a URL -> {}".format(url))

browser.visit(url)

print("\nProcurando elementos-chave...")

search_fsd_input = browser.find_by_id("searchInput").first
search_fsd_input.fill(search_str)

search_btn = browser.find_by_id("mw-searchButton").first
search_btn.click()

print("Carregando resultados...")

results = browser.find_by_css(".mw-search-result-heading")
size = len(results)
msg = "\nResposta -> {pattern}"

if size == 0:
    msg = msg.format(pattern = "nenhum resultado foi encontrado!")
else:
    msg = msg.format(pattern = "fo{0} encontrado{1} {2} resultado{1}")
    msg = msg.format(
        "ram" if size > 1 else "i",
        "s" if size > 1 else "",
        size
    )

print(msg)
print("\nSessão atual terminada.")

browser.quit()
