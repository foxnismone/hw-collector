
from pytrends.request import TrendReq
import time
try:
    pytrends = TrendReq(hl="es-419", tz=-180, timeout=(20, 35))
    pytrends.build_payload(["hot wheels"], cat=0, timeframe="today 3-m", geo="", gprop="")
    df = pytrends.interest_over_time()
    print("OK: filas=", len(df), "cols=", list(df.columns))
    if not df.empty:
        print("max=", df["hot wheels"].max(), "ultimo=", df["hot wheels"].iloc[-1])
except Exception as e:
    print("FALLO:", type(e).__name__, str(e)[:150])
