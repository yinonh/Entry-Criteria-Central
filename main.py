import streamlit as st
from streamlit_option_menu import option_menu
# from streamlit_theme import set_theme
# from streamlit_pandas_profiling import st_profile_report

from Screens.HomeScreen import HomePage
from Screens.Search import Search
from Screens.Calculator import Calculator
from Screens.Graph import GraphScreen
# from Data.ReviewDB import Data
from Data.AddmissionDB import AdmissionDB


IMAGE_PATH = "Assets/image.png"
THEAM_COLOR = "#5777b3"


class Managment:

    def __init__(self, *args, **kwargs):
        super(Managment, self).__init__(*args, **kwargs)
        self.window = None
        self.data = AdmissionDB()

        # self.data.update_all()

        st.set_page_config(page_title="My Streamlit App", page_icon="Assets/icon.ico")#, layout="wide")

        with st.sidebar:
            st.image(IMAGE_PATH)
            st.title("Entry Criteria Central")
            choice = option_menu(menu_title=None,
                                 options=[HomePage.name, Search.name, Calculator.name, GraphScreen.name],# , 'Humanities', 'Engineering', 'Natural sciences',
                                         # 'Health Sciences'],
                                 icons=[HomePage.icon, Search.icon, Calculator.icon, GraphScreen.icon], default_index=0)
            st.info("Welcome to the website")

        if choice == HomePage.name:
            self.window = HomePage(self.data)
            self.window.build()

        elif choice == Search.name:
            self.window = Search(self.data)
            self.window.build()

        elif choice == Calculator.name:
            self.window = Calculator(self.data)
            self.window.build()

        elif choice == GraphScreen.name:
            self.window = GraphScreen(self.data)
            self.window.build()


if __name__ == "__main__":
    Managment()
