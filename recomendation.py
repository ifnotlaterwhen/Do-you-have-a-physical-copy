from graph import Graph
from DButils import FilmDB

class Recommendation:
    def __init__(self, graph):
        self.graph = graph


    def build(self):
        db = FilmDB("cinefiles")
        sql_results = db.fetch_info_for_graph()

        #loop through the sql results and add each item as a node with its connections
        for title, row in sql_results.items():
            movie_node = "Movie:" + title
            actor_node = "Actor:" + row["actor_name"]
            director_node = "Director:" + row["directed_name"][0]

            self.graph.add_node(movie_node)
            self.graph.add_node(actor_node)
            self.graph.add_node(director_node)

            self.graph.connections(movie_node, actor_node)
            self.graph.connections(movie_node, director_node)
            self.graph.connections(actor_node, director_node)

            for genre in row["genre_name"].split(", "):
                genre_node = "Genre:" + genre
                self.graph.add_node(genre_node)
                self.graph.connections(movie_node, genre_node)

        return self.graph

recommend = Recommendation(Graph())
graph = recommend.build()
print(graph.adjacency)