from splinter import Browser
from selenium import webdriver
from timedprofiler import TimedProfiler
import multiprocessing, concurrent.futures

def test_proc(test):
    url = 'https://directory.fsf.org/wiki/Main_Page'
    browser_engine = "chrome"
    search_str = "asdbakfgueogmpew"
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
    
    tp = TimedProfiler(print)
    tp.enable_logging = True
    
    tp.log(f"Test#{test}")
    tp.log(f"Acessando a URL -> {url}")
    
    tp.target = "Acesso via URL"
    tp.start()

    browser.visit(url)

    tp.stop()
    tp.log("Verificando pop-ups...")

    # to-do make pop-up verifications
    # main div id -> fsf-modal-window-elem-container
    # close js -> fsfModalWindowElemDontShowForAWhile();
    main_popup = browser.find_by_id("fsf-modal-window-elem-container")

    if len(main_popup) == 1:
        tp.log("Removendo pop-up principal...")
        browser.execute_script("fsfModalWindowElemDontShowForAWhile();")
    else:
        tp.log("Nenhum pop-up encontrado.")

    tp.log("Procurando elementos-chave...")

    search_fsd_input = browser.find_by_id("searchInput").first
    search_fsd_input.fill(search_str)

    search_btn = browser.find_by_id("mw-searchButton").first

    tp.target = "Carregamento dos elementos"
    tp.start()

    search_btn.click()

    tp.log("Carregando resultados...")

    results = browser.find_by_css(".mw-search-result-heading")
    size = len(results)
    msg = "Resposta -> {pattern}"

    if size == 0:
        msg = msg.format(pattern = "nenhum resultado foi encontrado!")
    else:
        msg = msg.format(pattern = "fo{0} encontrado{1} {2} resultado{1}")
        msg = msg.format(
            "ram" if size > 1 else "i",
            "s" if size > 1 else "",
            size
        )

    tp.stop()
    tp.log(msg)
    tp.save_logs()
    
    browser.quit()

number_of_tests = 10
cores = multiprocessing.cpu_count()

print("Executando os testes...")

with concurrent.futures.ThreadPoolExecutor(cores) as executor:
    for running_test in range(number_of_tests + 1):
        executor.submit(test_proc, running_test)

print(f"Número de testes executados: {number_of_tests}")
print("Sessão atual terminada.")
