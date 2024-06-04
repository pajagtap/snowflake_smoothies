# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

conn = st.connection("snowflake")
# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """You can choose the fruits you want in your smoothie."""
)

name_on_order = st.text_input("Name of Smoothie:")
st.write("Name on smoothie will be: ", name_on_order)

session = conn.session()
my_dataframe = session.table("smoothies.public.fruit_options")\
                .select(col("FRUIT_NAME"), col("SEARCH_ON"))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()
                                               
ingredients_list = st.multiselect(
    "Choose upto 5 ingredients"
    ,my_dataframe
    ,max_selections=5
)
if ingredients_list:
    ingredients_str = ''
    
    for i in ingredients_list:
        ingredients_str += i + ' '
        st.subheader(i + ' Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+i)
        fv_dt = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        
    st.write(ingredients_str)

    my_insert_stmt = """ insert into 
                smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredients_str + """','"""+name_on_order+"""')"""

    time_to_insrt = st.button("Submit Order")
    if time_to_insrt:
        # st.write(my_insert_stmt)
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")



