import streamlit as st
from Screens.Screen import Screen

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class HomePage(Screen):
    name = 'Home'
    icon = 'house'

    def build(self):

        st.title("Entry Criteria Central")# 🎓
        st.write("List of academic institutions:")
        st.markdown("""---""")

        institutions_images = ['Assets/BGU.png', 'Assets/EV.png', 'Assets/TECH.png', 'Assets/TLV.png']

        for index, col in enumerate(st.columns(len(institutions_images))):
            with col:
                st.image(institutions_images[index], width=100)

        st.markdown('<br><br><br>', unsafe_allow_html=True)


        # Group the DataFrame by 'institute' and count the unique values in 'field' column
        grouped = self.data.groupby('institute')['field'].nunique().sort_values(ascending=False)

        # Reverse the text in x-axis labels
        reversed_labels = [label[::-1] for label in grouped.index]

        # Set the style using Seaborn
        sns.set(style="whitegrid")

        # Create a bar plot
        plt.figure(figsize=(12, 6))
        sns.barplot(x=reversed_labels, y=grouped.values, palette="viridis")

        # Customize the plot
        plt.title("Number of Unique Fields per Institute", fontsize=16)
        plt.xlabel("Institute", fontsize=12)
        plt.ylabel("Number of Unique Fields", fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=10)

        # Add data labels to the bars
        for i, v in enumerate(grouped.values):
            plt.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=10)

        # Display the plot in Streamlit page
        st.pyplot(plt)


