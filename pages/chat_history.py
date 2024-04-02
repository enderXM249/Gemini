import streamlit as st 
import mysql.connector
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv() 

config = {
  'host': 'localhost',
  'port': 3306,
  'user': 'root',
  'password': 'maity@123',
  'database': 'llm'
}

def connect_to_db():
    try:
        connection = mysql.connector.connect(**config)
        print(f"Connected successfully")
        return connection
    
    except mysql.connector.Error as err:
        st.error(f"Error connecting MYSQL database: {err}")
        print(f"Not connected {err}")
        return None

def store_message(sender, content):
    connection = connect_to_db()
    if connection:
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO chat_history (sender, timestamp, content) VALUES (%s, NOW(), %s)"
            cursor.execute(sql, (sender, content))
            connection.commit()
        except mysql.connector.Error as err:
            st.error(f"Error storing message: {err}")
        finally:
            cursor.close()
            connection.close()

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
def get_gemini_response(question):
    
    response =chat.send_message(question,stream=True)
    return response

st.title("Chat App with MySQL History")
input=st.text_input("Input: ",key="input")
submit=st.button("Ask the question")


if submit:
    
    response=get_gemini_response(input)
    st.subheader("The Response is")
    
    for chunk in response:
        print(st.write(chunk.text))
        print("_"*80)
    
    chat_history = chat.history
    # print(type(chat_history))
    result_chat = chat_history
    result_list = [result_chat]
    result_list = [str(item) for item in result_list]

    list_as_string = ', '.join(result_list)

    # print(type(list_as_string))

    
    store_message(sender="User", content=list_as_string)
    st.success("Message sent to DB!")
    # text_value = chat_history[1]['parts']['text']
    # st.write(list_as_string)
    

    
