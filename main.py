import streamlit as st
from streamlit_option_menu import option_menu
# from streamlit_theme import set_theme
# from streamlit_pandas_profiling import st_profile_report

from Screens.HomeScreen import HomePage
from Screens.Search import Search
from Screens.Calculator import Calculator
from Data.DB import Data

IMAGE_PATH = "Assets/image.png"
THEAM_COLOR = "#5777b3"


class Managment:

    def __init__(self, *args, **kwargs):
        super(Managment, self).__init__(*args, **kwargs)
        self.data = Data()
        #self.data.update_all()

        st.set_page_config(page_title="My Streamlit App", page_icon="Assets/icon.ico")#, layout="wide")

        with st.sidebar:
            st.image(IMAGE_PATH)
            st.title("Entry Criteria Central")
            choice = option_menu(menu_title=None,
                                 options=[HomePage.name, Search.name, Calculator.name],# , 'Humanities', 'Engineering', 'Natural sciences',
                                         # 'Health Sciences'],
                                 icons=[HomePage.icon, Search.icon, Calculator.icon], default_index=0)
            st.info("Welcome to the website")

        if choice == HomePage.name:
            window = HomePage(self.data)
            window.build()

        elif choice == Search.name:
            window = Search(self.data)
            window.build()

        elif choice == Calculator.name:
            window = Calculator(self.data)
            window.build()


if __name__ == "__main__":
    Managment()
