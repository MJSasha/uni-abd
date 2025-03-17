from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time
import csv
from bs4 import BeautifulSoup  # Для последующего парсинга HTML
from webdriver_manager.microsoft import EdgeChromiumDriverManager

edge_options = Options()
# edge_options.add_argument("--headless")  # Запуск в фоновом режиме
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

url = "https://annailina.pythonanywhere.com/"
driver.get(url)

scroll_pause_time = 3

# Скроллим до конца страницы
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause_time)

    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Получаем весь HTML после полной загрузки страницы
html_source = driver.page_source
driver.quit()

# Парсим HTML с использованием BeautifulSoup
soup = BeautifulSoup(html_source, "html.parser")
table = soup.find("table")  # Найдем таблицу в HTML

# Извлекаем данные из таблицы
output_csv_file = "data.csv"
with open(output_csv_file, "w", newline="", encoding="utf-8") as output_file:
    writer = csv.writer(output_file)

    if table:
        rows = table.find_all("tr")
        for row in rows:
            cells = row.find_all("td")
            # Удаляем переносы строк из каждой ячейки
            row_data = [cell.text.strip().replace('\n', ' ') for cell in cells]
            if row_data:  # Пропускаем пустые строки
                writer.writerow(row_data)

print(f"Данные сохранены в {output_csv_file}")
