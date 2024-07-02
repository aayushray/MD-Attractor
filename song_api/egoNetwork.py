from song_api import spotifyAPI
import networkx as nx
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt

class ConstructGraph():
    def __init__(self, collaboratedArtists: Dict[str, List[str]]) -> None:
        self.data = collaboratedArtists
        self.G = nx.Graph()

        self.constructGraph()
        self.similarityComparison(0.5)

    def constructGraph(self) -> None:
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

    def calculateSimilarity(self, genres1: List[str], genres2: List[str]) -> float:
        commonGenres = list(set(genres1) & set(genres2))
        similarity = len(commonGenres) / max(len(genres1), len(genres2))
        return similarity
    
    def similarityComparison(self, threshold: float) -> List[Tuple[str, str, Dict[str, float]]]:
        filteredEdges = []
        for edge in self.G.edges(data=True):
            if edge[2]['weight'] >= threshold:
                filteredEdges.append(edge)

        return filteredEdges
    
    def extractArtists(self) -> List[str]:
        artists = []
        for edge in self.filteredEdges:
            artists.append(edge[1])
        
        return artists