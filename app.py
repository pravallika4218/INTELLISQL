import streamlit as st
import sqlite3
import os
from google import genai

# ==============================
# CONFIGURE GEMINI (NEW SDK)
# ==============================

client = genai.Client(api_key="")

# ==============================
# FUNCTION: Convert Question → SQL
# ==============================

def get_sql_from_gemini(question):
    prompt = f"""
    Convert the following question into SQLite SQL query.

    Table: STUDENT(NAME, CLASS, SECTION, MARKS)

    Only return SQL query.
    No explanation.
    No markdown.

    Question: {question}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )

    return response.text.strip()


# ==============================
# FUNCTION: Execute SQL
# ==============================

def execute_query(sql, db="data.db"):
    try:
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return f"Database Error: {e}"


# ==============================
# STREAMLIT UI
# ==============================

st.set_page_config(page_title="IntelliSQL - Gemini", layout="centered")

st.title("📊 IntelliSQL")
st.subheader("Powered by Gemini 2.5 Flash")

st.sidebar.success("🟢 Gemini API Connected")
st.sidebar.write("Schema: STUDENT(NAME, CLASS, SECTION, MARKS)")

question = st.text_input("Ask a question about students:")

if st.button("Generate & Execute Query"):

    if question:

        with st.spinner("Gemini is generating SQL..."):
            sql_query = get_sql_from_gemini(question)

        st.subheader("Generated SQL Query:")
        st.code(sql_query, language="sql")

        if os.path.exists("data.db"):
            result = execute_query(sql_query)

            st.subheader("Query Result:")

            if isinstance(result, list):
                if result:
                    st.table(result)
                else:
                    st.info("No data found.")
            else:
                st.error(result)
        else:
            st.error("data.db not found. Please create the database first.")

    else:

        st.warning("Please enter a question.")
