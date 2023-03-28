import streamlit as st

from Screens.Screen import Screen


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

