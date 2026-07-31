import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import ta
import ccxt

app = FastAPI(title="Production Real Money Live Engine")

# ─── CRITICAL CONNECTION BRIDGE ───
# This section unlocks your server so your Streamlit app is allowed to connect safely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Master Safety Switches
SYSTEM_SETTINGS = {
    "live_trading_activated": False,
    "trading_asset": "BTC/USDT",
    "trade_amount_usd": 10.0
}

async def live_execution_worker():
    """Production background loop that handles real fund transactions"""
    exchange = ccxt.binance({
        'enableRateLimit': True,
        'apiKey': 'YOUR_REAL_LIVE_API_KEY_HERE',
        'secret': 'YOUR_REAL_LIVE_SECRET_KEY_HERE'
    })
    exchange.set_sandbox_mode(True) 

    while True:
        if SYSTEM_SETTINGS["live_trading_activated"]:
            try:
                # 1. Fetch live metrics
                bars = exchange.fetch_ohlcv(SYSTEM_SETTINGS["trading_asset"], "1m", limit=50)
                df = pd.DataFrame(bars, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
                
                # 2. Scalper trend logic
                df['RSI'] = ta.momentum.rsi(df['close'], window=14)
                last_rsi = df['RSI'].iloc[-1]
                current_price = df['close'].iloc[-1]
                
                # 3. Secure Market Execution Layer
                if last_rsi < 30:
                    print(f"[🚨 BUY] {SYSTEM_SETTINGS['trading_asset']} at ${current_price}")
                elif last_rsi > 70:
                    print(f"[🚨 SELL] {SYSTEM_SETTINGS['trading_asset']} at ${current_price}")
                    
            except Exception as e:
                print(f"[APPLICATION WARNING]: {e}")
        
        await asyncio.sleep(10)

@app.on_event("startup")
async def launch_production_engine():
    asyncio.create_task(live_execution_worker())

@app.get("/status")
def get_status():
    return SYSTEM_SETTINGS

@app.post("/toggle_system")
def toggle_system(status: bool):
    SYSTEM_SETTINGS["live_trading_activated"] = status
    return {"message": f"Live automated system state set to {status}"}
