import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from Screens.Screen import Screen


class Graph(Screen):
    name = 'graph'
    icon = ''

    def build(self):
        st.title('Hello Networkx')
        st.markdown('Zachary´s Karate Club Graph')


        G = nx.karate_club_graph()


        fig, ax = plt.subplots()
        pos = nx.kamada_kawai_layout(G)
        nx.draw(G,pos, with_labels=True)
        st.pyplot(fig)
        st.balloons()