
from collections import  defaultdict


class GraphBuild:
    def __init__(self, graph, db):
        self.graph = graph
        self.db = db
        self.start_node = None


    def build(self):

        sql_results = self.db.fetch_info_for_graph()

        #loop through the sql results and add each item as a node with its connections
        for row in sql_results:
            movie_node = "Movie:" + row["title"]

            if self.start_node is None:
                self.start_node = movie_node

            actors = row["actors"].split(", ")
            directors = row["directors"].split(", ")
            genres = row["genres"].split(", ")

            actor_nodes = ["Actor:" + name for name in actors]
            director_nodes = ["Director:" + name for name in directors]
            genre_nodes = ["Genre:" + name for name in genres]

            for actor_node in actor_nodes:
                self.graph.connections(movie_node, actor_node)

            for director_node in director_nodes:
                self.graph.connections(movie_node, director_node)

            for actor_node in actor_nodes:
                for director_node in director_nodes:
                    self.graph.connections(actor_node, director_node)

            for genre in genre_nodes:
                self.graph.connections(movie_node, genre)

        return self.graph

#recursively traversing the graph counting how many each node appears
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

        genres = {}    #<- created 2 dicts to store the top genres seperate from the top directors and actors for the recommendation logic in the tmdb_api class. Makes it easier to filter results in the get_recommendation method from tmdb_api class
        people = {}

        for node, count in frequency.items():
            if count >= top_nodes:
                if node.startswith("Genre"):
                    genres[node] = count
                elif node.startswith(("Director:", "Actor:")):
                    people[node] = count

        return genres, people

#returning movies nodes that apear in database
    def movie_titles(self):
        titles = set()
        for node in self.graph.adjacency:
            if node.startswith("Movie:"):
                titles.add(node.replace("Movie:", "", 1))
        return titles