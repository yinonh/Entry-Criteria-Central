import streamlit as st
import plotly.express as px
from Screens.Screen import Screen
import pandas as pd
import base64


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

        st.write('\n\n')

        data = self.data.get_the_min_and_max()

        # Convert data to DataFrame for easier plotting
        df = pd.DataFrame.from_dict(data, orient="index")

        # Plot bar chart using Plotly
        fig = px.bar(
            df,
            x=df.index,
            y=["min_sum", "max_sum", "avg_sum", "max_psy", "min_psy", "avg_psy"],
            color_discrete_sequence=px.colors.qualitative.Dark2,
            title="Summary Statistics",
            labels={
                "variable": "Summary Statistic",
                "value": "Value",
            },
        )

        # Display chart in Streamlit app
        st.plotly_chart(fig)

