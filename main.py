import pandas as pd
from model.driver import Driver
from selenium.common.exceptions import StaleElementReferenceException
import time

URL = 'https://www.quintoandar.com.br/alugar/imovel/sao-paulo-sp-brasil'
PATH_WEBDRIVER = 'WebDriver/msedgedriver.exe'

def main():

    # Setup and start webdriver
    driver = Driver(PATH_WEBDRIVER)
    driver.start()
    driver.enter_page(URL)
    time.sleep(4)

    # Scroll navigate configuration
    element_scroll = driver.get_elements('div', 'class', 'sc-18lu2ht-0 bvIvXr')[0]
    driver.driver.execute_script("arguments[0].style.overflow = 'visible';", element_scroll)
    scroll_repeat_in_pixels = 250

    # Initialize variables
    df_properties = pd.DataFrame()
    success = 0
    error = 0
    hundred = 100

    # Loop to interact with page
    while True:
        try:
            time.sleep(1)
            house_list_temp = [card.text.split('\n')[-5:] for card in driver.get_elements('div', 'data-testid', 'house-card-container')]

            df_temp = pd.DataFrame()
            df_temp['address'] = [house[0] for house in house_list_temp]
            df_temp['district'] = [house[1].split(', ')[0] for house in house_list_temp]
            df_temp['area'] = [house[2].split(' • ')[0].split(' m')[0] for house in house_list_temp]
            df_temp['bedrooms'] = [house[2].split(' • ')[1].split(' q')[0] for house in house_list_temp]
            df_temp['garage'] = [house[2].split(' • ')[2].split(' v')[0] for house in house_list_temp]
            df_temp['type'] = [house[2].split(' • ')[3] for house in house_list_temp]
            df_temp['rent'] = [house[3].split('R$ ')[1].replace('.', '') for house in house_list_temp]
            df_temp['total'] = [house[4].split('R$ ')[1].replace('.', '') for house in house_list_temp]

            # Add the collected temporary dataframe to main dataframe
            df_properties = pd.concat([df_properties, df_temp]).reset_index(drop=True).drop_duplicates().reset_index(drop=True)
            total_properties = df_properties.shape[0]
            if total_properties > hundred:
                hundred += 100
                df_properties.to_csv('quintoandar.csv', index=False)
                print('File quintoandar.csv generated!')

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
            print('Success: ' + str(success) + ' | Properties found: ' + str(df_temp.shape[0]) + ' | Total properties: ' + str(df_properties.shape[0]))

        except Exception as e:
            error += 1
            print('Erro: ' + str(error) + ' - ' + str(e))



if __name__ == '__main__':
    main()


    