import streamlit as st
from streamlit_pills_multiselect import pills

from Screens.Screen import Screen
# import networkx as nx
# import matplotlib.pyplot as plt

THEAM_COLOR = "#5777b3"

institutions_dict = {'BGU': ("בן גוריון", 'orange'), 'EVR': ("האוניברסיטה העברית", 'pale-green'),
                     'TECH': ("הטכניון", 'pale-blue'), 'TLV': ("אוניברסיטת תל אביב", 'khaki')}


class Search(Screen):
    name = 'Search'
    icon = 'search'

    def card(self, name=None, institutions=None, sum=None, additional=None, psychometric=None,
             min_final_grade_average=None, without=None, notes=None):
        if min_final_grade_average is None:
            min_final_grade_average = ' - '
        if without is None:
            without = ''
        else:
            without = 'ללא פסיכומטרי: ' + without
        if psychometric is None:
            psychometric = ''
        if sum is None:
            sum = ''
        return st.write(f"""
       <!DOCTYPE html>
<html>
  <head>
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
  </head>
  <body>
    <div class="w3-container">
      <div class="w3-card-4" style="width:130%">
        <header class="w3-container w3-{institutions_dict[institutions][1]}">
          <div style='text-align: right'>
            <h3>{name}</h3>
            <p>{institutions_dict[institutions][0]}</p>
          </div>
        </header>
        <div class="w3-container">
          <div style='text-align: right'>
            <div style='text-align: right'>
              <p>{notes}</p>
              <p><strong>{min_final_grade_average} :ממוצע בגרות מינימאלי</strong></p>
            </div>
          </div>
          <hr>
          <div style='text-align: right'>
            <p>{without}</p><br>
          </div>
        </div>
        <div class="button-container">
          <button class="w3-button w3-light-grey"> {sum} :סכם</button>
          <button class="w3-button w3-sand">{'וגם' if additional else 'או' if not additional is None else ''}</button>
          <button class="w3-button w3-light-grey">{psychometric} :פסיכומטרי</button>
        </div>
      </div>
      <br><br>
    </div>
  </body>
</html>
""", unsafe_allow_html=True)


    def build(self):

        st.markdown("# <strong>Search</strong>", unsafe_allow_html=True)
        selected = pills("Chose:", [i[0] for i in institutions_dict.values()], index=None, multiselect=True,
                         clearable=True)
        result = st.multiselect(label='Enter what you want to learn:', options=set(self.data.get_all_professions()))
        sort_type = st.radio(label='chose sort type:', options=['don\'t sort', 'Sort by difficulty', 'Sort by sum', 'Sort by psychometric'], horizontal=True)
        high_to_low = st.checkbox(label='High to low', value=True)

        search_button = st.button('Search', on_click=self.press)
        st.write('\n')

        if search_button:
            selected_list = []
            if not selected is None:
                selected_list = list(
                    map(lambda x: next((k for k, v in institutions_dict.items() if x in v), None), selected))

            data = self.data.get_all_data(result, selected_list, sort_type, high_to_low)
            for row in data:
                self.card(name=row['name'], institutions=row['institutions'], sum=row['sum'], additional=row['additional'],
                          psychometric=row['psychometric'], notes=row['notes'],
                          min_final_grade_average=row['min_final_grade_average'], without=row['without'])

    def press(self):
        pass
