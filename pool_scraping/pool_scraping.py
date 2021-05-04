from bs4 import BeautifulSoup
import numpy as np


def get_pool_data(html_filename):
    """
    Takes the html corresponding to the <div class="ResultsPool-pool ResultsPool-pool"> and returns 
    (1) a list of fencer's names (in order), (2) a list of fencer's ID on FIE (in order)
    (3) an boolean array indicating winners for each bout and (4) array of scores for each bout
    """
    html_pool = open(html_filename)
    # caution: contains chlorine!
    pool_soup = BeautifulSoup(html_pool, 'html.parser')

    athlete_name_list = []
    athlete_ID_list = []

    for athlete in pool_soup.find_all('a'):
        link = athlete.get('href')
        link_pieces = link.split("/")
        athlete_name_list.append(athlete.get_text())
        athlete_ID_list.append(link_pieces[2])

    pool_size = len(athlete_name_list)
    winners_array = np.zeros((pool_size, pool_size), dtype=int)
    score_array = np.zeros((pool_size, pool_size), dtype=int)

    for idx, entry in enumerate(pool_soup.find_all('div', class_="ResultsPool-score")):
        score = entry.get_text().strip()
        if(score):
            # scores are stored in a 'V/5', 'D/2' format
            score_pieces = score.split("/")
            print(score_pieces)
            if score_pieces[0] == 'V':
                winners_array[idx // pool_size][idx % pool_size] = 1
            score_array[idx // pool_size][idx % pool_size] = score_pieces[1]
    
    return athlete_name_list, athlete_ID_list, winners_array, score_array