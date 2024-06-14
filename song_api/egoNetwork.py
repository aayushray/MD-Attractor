from song_api import spotifyAPI
import networkx as nx
import matplotlib.pyplot as plt

class ConstructGraph():
    def __init__(self, collaboratedArtists):
        self.data = collaboratedArtists
        self.G = nx.Graph()

        self.constructGraph()
        # print("Nodes:", self.G.nodes())
        # print("Edges:", self.G.edges())

        # nx.draw(self.G, with_labels=True, font_weight='bold')
        # pos = nx.spring_layout(self.G)
        # edge_labels = nx.get_edge_attributes(self.G, 'weight')
        # nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels)
        # plt.show()



    def constructGraph(self):
        rootArtist = next(iter(self.data))
        self.G.add_node(rootArtist)

        for artist in self.data:
            if artist == rootArtist:
                continue
            self.G.add_node(artist)
            genres1 = self.data[rootArtist]
            genres2 = self.data[artist]

            similarity = self.calculateSimilarity(genres1, genres2)
            self.G.add_edge(rootArtist, artist, weight = similarity)

    def calculateSimilarity(self, genres1, genres2):
        commonGenres = list(set(genres1) & set(genres2))
        similarity = len(commonGenres) / max(len(genres1), len(genres2))
        return similarity