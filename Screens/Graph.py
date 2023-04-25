import streamlit as st

from Screens.Screen import Screen
import networkx as nx
import matplotlib.pyplot as plt

THEAM_COLOR = "#5777b3"

institutions_dict = {'BGU': ("בן גוריון", 'orange'), 'EVR': ("האוניברסיטה העברית", 'pale-green'),
                     'TECH': ("הטכניון", 'pale-blue'), 'TLV': ("אוניברסיטת תל אביב", 'khaki')}


class GraphScreen(Screen):
    name = 'Graph'
    icon = 'asterisk'

    def create_graph(self, data):
        G = nx.DiGraph()

        # Create nodes for each institution
        institutions = set()
        for record in data:
            institutions.add(record['institutions'])

        for record in institutions:
            G.add_node(record)  # set the color attribute for each node

        # Create edges for each course
        for record in data:
            course_name = record['name'][::-1]
            institution_name = record['institutions']
            G.add_edge(institution_name, course_name, course=course_name)

        return G

    def build(self):

        st.markdown("# <strong>Create a Graph</strong>", unsafe_allow_html=True)
        result = st.multiselect(label='Enter what you want to learn:', options=set(self.data.get_all_professions()))

        search_button = st.button('Create Graph')
        st.write('\n')

        if search_button:
            data = self.data.get_all_data(result, [i[0] for i in institutions_dict.items()], None, False)
            G = self.create_graph(data)
            pos = nx.spring_layout(G)
            node_colors = self.color_for_node(G)
            nx.draw(G, pos, with_labels=True, node_color=node_colors)
            st.pyplot(plt)

    def color_for_node(self, G):
        colors = {'BGU': '#ff9800', 'EVR': '#ddffdd', 'TECH': '#ddffff', 'TLV': '#f0e68c'}
        node_colors = []

        for i in G.nodes():
            if i in colors.keys():
                node_colors.append(colors[i])
            else:
                node_colors.append('white')
        return node_colors
