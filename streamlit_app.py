# Import python packages

import requests
from snowflake.snowpark import Session
import streamlit as st
#from secrets import account, user, password, warehouse, database, schema, role
from snowflake.snowpark.functions import col


#Write directly to the app
st.title("Custom Smoothies Order Form :cup_with_straw:")
st.write(
    """Customise your own smoothie!
    """
)
name_on_order = st.text_input('Name on smoothie')
st.write('The name on your smoothie will be ', name_on_order)

#connection_parameters = {
#    "account": "pszkbqy-zv52731",
#    "user": "JohnV54321",
#    "password": "&JT#e:'238~NR._",
#    "role": "sysadmin",  # optional
#    "warehouse": "COMPUTE_WH",  # optional
#    "database": "SMOOTHIES",  # optional
#    "schema": "PUBLIC",  # optional
#    }  

#session = Session.builder.configs(connection_parameters).create()

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect('Choose up to 5 ingredients:',
                                  my_dataframe,
                                  max_selections = 5
                                  )

if ingredients_list:
    
    ingredients_string = '';

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' ';
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
        fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
        
    st.write(ingredients_string)
#insert into smoothies.public.orders(ingredients, name_on_order) values ('Guava Elderberries ', 'John');
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    
    time_to_insert = st.button('Submit Order');

    if time_to_insert:
        if ingredients_string:
            session.sql(my_insert_stmt).collect()
            s_statement = 'Your Smoothie is ordered under ' + str(name_on_order)
            st.success(s_statement, icon="✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fv_df = st.dataframe(data=fruityvice_response.json(),use_container_width=True)

