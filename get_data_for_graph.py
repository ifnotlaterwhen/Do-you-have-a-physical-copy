from DButils import FilmDB
from tabulate import tabulate
from pprint import pprint

def get_data():
    data_for_graph = FilmDB("cinefiles").fetch_info_for_graph()
    table = tabulate(data_for_graph, headers=['film_id','title', 'genre_id', 'director_id', 'actor_id'], tablefmt='markdown')
    pprint(data_for_graph)
    print(table)


if __name__ == "__main__":
    get_data()