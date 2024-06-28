from song_api import spotifyAPI
import networkx as nx
import matplotlib.pyplot as plt

class ConstructGraph():
    def __init__(self, collaboratedArtists):
        self.data = collaboratedArtists
        self.G = nx.Graph()

        self.constructGraph()
        self.similarityComparison(0.5)

        # Another Approach: Sort the top tracks based on their popularity, and then compare the genres, with the root song genre.


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
    
    def similarityComparison(self, threshold):
        self.filteredEdges = []
        for edge in self.G.edges(data=True):
            if edge[2]['weight'] >= threshold:
                self.filteredEdges.append(edge)

        return self.filteredEdges
    
    def extractArtists(self):
        self.artists = []
        for edge in self.filteredEdges:
            self.artists.append(edge[1])
        
        return self.artists