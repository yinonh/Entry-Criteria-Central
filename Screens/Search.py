import streamlit as st
# import time
from streamlit_pills_multiselect import pills


from Screens.Screen import Screen

THEAM_COLOR = "#5777b3"

institutions_dict = {'BGU': "בן גוריון", 'EVR': "האוניברסיטה העברית", 'TECH': "הטכניון", 'TLV': "אוניברסיטת תל אביב"}
images_dict = {'BGU': 'Assets/BGU.png', 'EVR': 'Assets/EV.png', 'TECH': 'Assets/TECH.png', 'TLV': 'Assets/TLV.png'}


class Search(Screen):
    name = 'Search'
    icon = 'search'

    def card(self, name=None, institutions=None, sum=None, additional=None, psychometric=None, min_final_grade_average=None, without=None, notes=None):
        color = {'BGU': 'orange', 'EVR': 'pale-green', 'TECH': 'pale-blue', 'TLV': 'khaki'}
        return st.write(f"""
        <!DOCTYPE html>
        <html>
        <meta name="viewport" content="width=device-width, initial-scale=0.5">
        <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
        <style>
          .button-container {{
            display: flex;
          }}
        
          .w3-button {{
            pointer-events: none;
            flex-grow: 1;
          }}
        </style>
        <body>
          <div class="w3-container">
            <div class="w3-card-4" style="width:100%">
              <header class="w3-container w3-{color[institutions]}">
                <div style='text-align: right'>
                  <h3>{name}</h3>
                  <p>{institutions_dict[institutions]}</p>
                </div>
              </header>
              <div class="w3-container">
                <div style='text-align: right'>
                  <p>{without}</p>
                </div>
                <hr>
                <p>CEO at Mighty Schools. Marketing and Advertising. Seeking a new job and new opportunities.</p><br>
              </div>
              <div class="button-container">
                <button class="w3-button w3-light-grey"> {sum} :סכם</button>
                <button class="w3-button w3-sand">{psychometric} :פסיכומטרי</button>
                <button class="w3-button w3-dark-grey">hello</button>
              </div>
            </div>
          </div>
        </body>
        </html>
""", unsafe_allow_html=True)

    def build(self):

        st.title("Search")
        selected = pills("Chose:", list(institutions_dict.values()), index=None, multiselect=True, clearable=True)
        result = st.multiselect(label='Enter what you want to learn:', options=self.data.get_all_professions())

        search_button = st.button('Search', on_click=self.press)

        if search_button:
            data = self.data.get_all_data(result)
            for i in data:
                for j in data[i]:
                    self.card(j['name'], i, 3, 5)
                    # self.hebrow_text("<h2>" + j['name'] + "</h2>")
                    # self.hebrow_text("<h3>" + institutions_dict[i] + "</h3>")



        # results = self.data.get_all_data(result)
        # card = st.container()

        # progress_text = "Operation in progress. Please wait."
        # my_bar = st.progress(0)
        # for percent_complete in range(100):
        #     time.sleep(0.05)
        #     my_bar.progress(percent_complete + 1)

    def press(self):
        pass
