import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sales AI Dashboard", layout="wide")

st.title("📊 Sales AI Dashboard")

question = st.text_input("Ask your sales question")

if st.button("Ask"):

    if question:
        try:
            res = requests.get(
                "http://127.0.0.1:8000/ask",
                params={"question": question}
            )

            data = res.json()

            if "error" in data:
                st.error(data["error"])

            else:
                # 💡 Insight
                if "insight" in data:
                    st.subheader("💡 Insight")
                    st.success(data["insight"])

                # SQL
                st.subheader("🧠 Generated SQL")
                st.code(data["sql"], language="sql")

                # Table
                df = pd.DataFrame(data["data"])

                st.subheader("📋 Result")
                st.dataframe(df)

                # Chart
                if len(df.columns) >= 2:
                    st.subheader("📈 Chart")

                    x = df.columns[0]
                    y = df.columns[1]

                    fig, ax = plt.subplots()
                    ax.bar(df[x], df[y])
                    plt.xticks(rotation=45)

                    st.pyplot(fig)

        except Exception as e:
            st.error(str(e))