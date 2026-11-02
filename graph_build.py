
from collections import  defaultdict


class GraphBuild:
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

    def dfs(self, start_node):
        seen = set()
        frequency = defaultdict(int)
        top_nodes = 4
        def visit(node):
            seen.add(node)
            for neighbor in self.graph.adjacency[node]:
                frequency[neighbor] +=1
                if neighbor not in seen:
                    visit(neighbor)

        visit(start_node)

        genres = {}    #<- created 2 dicts to store the top genres seperate from the top directors and actors for the recommendation logic in the tmdb_api class. i chose to do this to avoid unessisary if else, for the genre_id and people_id methods in the tmdb_api.py.
        people = {}

        for node, count in frequency.items():
            if count >= top_nodes:
                if node.startswith("Genre"):
                    genres[node] = count
                elif node.startswith(("Director:", "Actor:")):
                    people[node] = count

        return genres, people

