import streamlit as st
import requests
from services.api import get_news_sentiment

def sentiment_page():
    st.title("📰 News Sentiment Analysis")

    token = st.session_state.token
    sentiment_data = get_news_sentiment(token)

    if not sentiment_data:
        st.write("No sentiment data available.")
        return

    # Display Overall Sentiment Summary
    st.subheader("📊 Overall Portfolio Sentiment Summary")
    overall_summary = sentiment_data["overall_sentiment_summary"]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("😊 Positive", overall_summary["positive"])
    with col2:
        st.metric("😐 Neutral", overall_summary["neutral"])
    with col3:
        st.metric("😞 Negative", overall_summary["negative"])

    # Display Holdings Sentiment
    st.subheader("📈 Holdings Sentiment")
    for stock in sentiment_data["holdings_sentiment"]:
        st.markdown(
            f"""
            ### {stock['stock_symbol']} - {stock['stock_name']}
            **Sentiment Summary:** {stock['sentiment_summary']}
            """
        )

        # Display related articles
        st.markdown("**📰 Related Articles:**")
        for article in stock["related_articles"]:

            # Display article details
            st.markdown(
                f"""
                - [{article['title']}]({article['link']})  
                  <medium>Publisher: {article['publisher']}</medium>  
                  <medium>Sentiment: **{article['sentiment']}**</medium>
                """,
                unsafe_allow_html=True
            )
