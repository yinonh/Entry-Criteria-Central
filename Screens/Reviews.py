import streamlit as st
import matplotlib.pyplot as plt
import random
from Screens.Screen import Screen


class Reviews(Screen):
    name = 'Reviews'
    icon = 'chat-right-text-fill'

    def filter_field_options(self, institute):
        filtered_data = self.data[self.data['institute'] == institute]
        field_options = filtered_data['field'].unique()
        return field_options

    def filter_data(self, institute, field):
        filtered_data = self.data[(self.data['institute'] == institute) & (self.data['field'] == field)]
        return filtered_data

    def build(self):

        st.title("Reviews")

        institute_options = self.data['institute'].unique()
        selected_institute = st.selectbox('Select an institute', institute_options)

        field_options = self.filter_field_options(selected_institute)
        selected_field = st.selectbox('Select a field', field_options)

        filtered_df = self.filter_data(selected_institute, selected_field)

        # Create pie charts for the selected data
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        columns = ['rating_value', 'expectations_grade', 'level_grade']

        for i, column in enumerate(columns):
            ax = axs[i]
            value_counts = filtered_df[column].value_counts()
            labels = value_counts.index.tolist()
            sizes = value_counts.values.tolist()
            ax.pie(sizes, labels=labels, autopct='%1d%%')
            ax.set_title(column)

        # Adjust spacing between subplots
        plt.tight_layout()

        # Display the pie charts in Streamlit
        st.pyplot(fig)

        col1, col2, col3 = st.columns(spec=3)

        with col1:
            st.markdown(filtered_df['rating_value'].mean())
        with col2:
            st.markdown(filtered_df['expectations_grade'].mean())
        with col3:
            st.markdown(filtered_df['level_grade'].mean())

        # Display random advice from previous students
        st.markdown('## Advice from Previous Students:')
        advice_samples = random.sample(list(filtered_df['advice']), k=4)
        for advice in advice_samples:
            st.markdown("""<div style="text-align: right;">""" + advice + """</div>""", unsafe_allow_html=True)
            st.markdown("---")