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

    success = 0
    error = 0
    while True:
        try:
            time.sleep(1)
            df_temp = pd.DataFrame()
            df_temp['address'] = [rua.text for rua in driver.get_elements('span', 'data-testid', 'house-card-address')]
            df_temp['district'] = [bairro.text.split(',')[0] for bairro in driver.get_elements('span', 'data-testid', 'house-card-region')]
            df_temp['area'] = [info.text.split(' • ')[0] for info in driver.get_elements('span', 'class', 'sc-gsnTZi iEPiQX sc-crXcEl jddosl CozyTypography')]
            df_temp['bedrooms'] = [info.text.split(' • ')[1] for info in driver.get_elements('span', 'class', 'sc-gsnTZi iEPiQX sc-crXcEl jddosl CozyTypography')]
            df_temp['garage'] = [info.text.split(' • ')[2] for info in driver.get_elements('span', 'class', 'sc-gsnTZi iEPiQX sc-crXcEl jddosl CozyTypography')]
            df_temp['type'] = [info.text.split(' • ')[3] for info in driver.get_elements('span', 'class', 'sc-gsnTZi iEPiQX sc-crXcEl jddosl CozyTypography')]
            df_temp['rent'] = [aluguel.text.split('R$ ')[1] for aluguel in driver.get_elements('h3', 'data-testid', 'house-card-rent')]
            df_temp['total'] = [total.text.split('R$ ')[1] for total in driver.get_elements('small', 'class', 'sc-gsnTZi UCMwJ sc-crXcEl jddosl CozyTypography')]

            df_casas = pd.concat([df_casas, df_temp]).reset_index(drop=True).drop_duplicates().reset_index(drop=True)

            driver.driver.execute_script('arguments[0].scrollIntoView();', driver.get_elements('div', 'data-testid', 'house-card-container')[-1])

            success += 1
            print('Sucesso: ' + str(success) + ' | Casas encontradas: ' + str(df_temp.shape[0]) + ' | Total de casas: ' + str(df_casas.shape[0]))
            
        except:
            error += 1
            print('Erro: ' + str(error))
            continue



if __name__ == '__main__':
    main()


    