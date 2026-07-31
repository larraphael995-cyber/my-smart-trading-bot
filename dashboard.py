import streamlit as st
import json
import urllib.request

# ─── YOUR VERIFIED SECURE CORE ADDRESS ───
API_URL = "https://onrender.com"

st.set_page_config(page_title="Live Production Console", page_icon="💰")
st.title("💰 AI Live Capital Management Console")

# Secure bypass function utilizing native Python network calls instead of outside links
def secure_fetch_status(url):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'} # Mimics a safe browser request
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return None

# Attempt to connect to your background engine
status = secure_fetch_status(API_URL)

if status is None:
    st.error("Live Execution Core is offline. Please make sure your Render link is awake.")
    st.stop()

is_live = status.get("live_trading_activated", False)

st.warning("⚠️ SECURITY WARNING: Turning this system ON connects directly to your live API broker funds.")

st.metric(label="Current Capital Safety Status", value="LIVE AND ACTIVE" if is_live else "SECURE / DISCONNECTED")

# Control Switches
if is_live:
    if st.button("🔴 EMERGENCY KILL SWITCH (STOP TRADING)", type="primary", use_container_width=True):
        try:
            urllib.request.urlopen(API_URL.replace("/status", "/toggle_system?status=false"), timeout=5)
            st.rerun()
        except:
            st.error("Failed to transmit stop command.")
else:
    if st.button("⚡ ACTIVATE LIVE BOT EXECUTION", use_container_width=True):
        try:
            urllib.request.urlopen(API_URL.replace("/status", "/toggle_system?status=true"), timeout=5)
            st.rerun()
        except:
            st.error("Failed to transmit start command.")

st.info(f"Targeting Market Asset: `{status.get('trading_asset', 'BTC/USDT')}` \n\nMax Allocation Size: `${status.get('trade_amount_usd', 10.0)}` USD per trade.")
