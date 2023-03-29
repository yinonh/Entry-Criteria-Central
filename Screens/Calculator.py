import streamlit as st
from Screens.Screen import Screen


class Calculator(Screen):
    name = 'calculator'
    icon = 'calculator-fill'

    def build(self):
        st.markdown("""# Admission Chances Calculator for Various Universities

Welcome to our Admission Chances Calculator page! Here, you can calculate your chances of getting admitted to various universities across the world.

We currently offer admission chances calculators for the following universities:

- [Ben-Gurion University](https://in.bgu.ac.il/welcome/Pages/Rishum/JUNCTION-chances.aspx)
- [Hebrew University of Jerusalem](https://go.huji.ac.il/)
- [Technion](https://admissions.technion.ac.il/calculator/)
- [Tel-Aviv University](https://go.tau.ac.il/he/calculator)

To use a calculator, simply click on the link for the university you're interested in and fill out the required information, such as your GPA, test scores, and extracurricular activities. The calculator will then estimate your chances of getting admitted to that university based on its past admission data and other relevant factors.

Please note that the results from these calculators are estimates only and should not be taken as definitive. Admissions decisions are based on a wide range of factors beyond just your academic credentials, so we recommend using these calculators as a starting point for your research and not relying on them too heavily.

We hope you find our admission chances calculators useful, and we wish you the best of luck in your college applications!
""")