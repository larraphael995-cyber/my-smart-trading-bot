import streamlit as st
import requests

API_URL = "https://corsproxy.io?" + "https://onrender.com"

st.set_page_config(page_title="Live Production Console", page_icon="💰")
st.title("💰 AI Live Capital Management Console")

try:
    status = requests.get(API_URL).json()
    is_live = status["live_trading_activated"]
except Exception as e:
    st.error("Live Execution Core is offline. Please launch main.py first.")
    st.stop()

st.warning("⚠️ SECURITY WARNING: Turning this system ON connects directly to your live API broker funds.")

st.metric(label="Current Capital Safety Status", value="LIVE AND ACTIVE" if is_live else "SECURE / DISCONNECTED")

if is_live:
    if st.button("🔴 EMERGENCY KILL SWITCH (STOP TRADING)", type="primary", use_container_width=True):
        requests.post(API_URL.replace("/status", "/toggle_system?status=false"))
        st.rerun()
else:
    if st.button("⚡ ACTIVATE LIVE BOT EXECUTION", use_container_width=True):
        requests.post(API_URL.replace("/status", "/toggle_system?status=true"))
        st.rerun()

st.info(f"Targeting Market Asset: `{status['trading_asset']}` \n\nMax Allocation Size: `${status['trade_amount_usd']}` USD per trade.")
