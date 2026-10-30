from graph import Graph
from DButils import FilmDB

class Recommendation:
    def __init__(self, graph,db):
        self.graph = graph
        self.db = db


    def build(self):

        sql_results = self.db.fetch_info_for_graph()

        #loop through the sql results and add each item as a node with its connections
        for row in sql_results:
            movie_node = "Movie:" + row["title"]

            actor_node = "Actor:" + row["actors"]
            director_node = "Director:" + row["directors"]

            self.graph.add_node(movie_node)
            self.graph.add_node(actor_node)
            self.graph.add_node(director_node)

            self.graph.connections(movie_node, actor_node)
            self.graph.connections(movie_node, director_node)
            self.graph.connections(actor_node, director_node)

            for genre in row["genre"].split(", "):
                genre_node = "Genre:" + genre
                self.graph.add_node(genre_node)
                self.graph.connections(movie_node, genre_node)

        return self.graph

if __name__ == "__main__":
    recommend = Recommendation(Graph(), FilmDB("cinefiles"))
    graph = recommend.build()
    print(graph.adjacency)