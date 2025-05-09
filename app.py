import streamlit as st
import pandas as pd
from scraper import scrape_enr
from datetime import datetime

st.set_page_config(page_title="US Infrastructure News Dashboard", page_icon="🏗️")
st.title("🏗️ US Infrastructure News Dashboard")

if st.button("📡 Scrape Latest News"):
    with st.spinner('Scraping ENR Infrastructure News…'):
        df = scrape_enr()
        if not df.empty:
            st.success(f"✅ Fetched {len(df)} articles.")
            st.dataframe(df)
            file_name = f'US_Infrastructure_News_{datetime.today().strftime("%Y%m%d")}.xlsx'
            df.to_excel(file_name, index=False)
            with open(file_name, "rb") as f:
                st.download_button(
                    label="📥 Download Excel Report",
                    data=f,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.error("No articles found.")
else:
    st.info("Click the button to fetch latest news.")
