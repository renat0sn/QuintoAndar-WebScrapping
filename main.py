import pandas as pd
from model.driver import Driver
from bs4 import BeautifulSoup
import time

URL = 'https://www.quintoandar.com.br/alugar/imovel/sao-paulo-sp-brasil'
PATH_WEBDRIVER = 'WebDriver/msedgedriver.exe'

def main():
    driver = Driver(PATH_WEBDRIVER)
    driver.start()
    driver.enter_page(URL)

    df_casas = pd.DataFrame()
    # Scroll navigate configuration
    element_scroll = driver.get_elements('div', 'class', 'sc-18lu2ht-0 bvIvXr')[0]
    driver.driver.execute_script("arguments[0].style.overflow = 'visible';", element_scroll)
    scroll_repeat_in_pixels = 250

    success = 0
    error = 0
    while True:
        try:
            time.sleep(1)
            house_list_temp = [card.text.split('\n')[-5:] for card in driver.get_elements('div', 'data-testid', 'house-card-container')]

            df_temp = pd.DataFrame()
            df_temp['address'] = [house[0] for house in house_list_temp]
            df_temp['district'] = [house[1].split(', ')[0] for house in house_list_temp]
            df_temp['area'] = [house[2].split(' • ')[0] for house in house_list_temp]
            df_temp['bedrooms'] = [house[2].split(' • ')[1] for house in house_list_temp]
            df_temp['garage'] = [house[2].split(' • ')[2] for house in house_list_temp]
            df_temp['type'] = [house[2].split(' • ')[3] for house in house_list_temp]
            df_temp['rent'] = [house[3].split('R$ ')[1] for house in house_list_temp]
            df_temp['total'] = [house[4].split('R$ ')[1] for house in house_list_temp]

            df_casas = pd.concat([df_casas, df_temp]).reset_index(drop=True).drop_duplicates().reset_index(drop=True)

            driver.driver.execute_script('arguments[0].scrollIntoView();', driver.get_elements('div', 'data-testid', 'house-card-container')[-3])
            ver_mais_btn = driver.get_elements('button', 'aria-label', 'Ver mais')[0]
            time.sleep(1)
            driver.click_element(ver_mais_btn)
            # Scroll until find "Ver mais" button
            while True:
                driver.driver.execute_script(f"arguments[0].scrollTop += {scroll_repeat_in_pixels}", element_scroll)
                try:
                    ver_mais_btn = driver.get_elements('button', 'aria-label', 'Ver mais')[0]
                    time.sleep(1)
                    driver.click_element(ver_mais_btn)
                    break
                except (StaleElementReferenceException, IndexError):
                    continue

            success += 1
            print('Sucesso: ' + str(success) + ' | Casas encontradas: ' + str(df_temp.shape[0]) + ' | Total de casas: ' + str(df_casas.shape[0]))
            
        except:
            error += 1
            print('Erro: ' + str(error) + ' - ' + str(e))



if __name__ == '__main__':
    main()


    