from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

CSV_FILE = "data/btc_1d_data_2018_to_2025.csv"

def load_data():
    df = pd.read_csv(CSV_FILE)
    # Ubah kolom waktu dari string ke datetime
    df["Open time"] = pd.to_datetime(df["Open time"])
    return df

def build_chart(df):
    #  baris: atas = candlestick, bawah = volume
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,          # sumbu X dipakai bersama
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25],   # candlestick 75%, volume 25%
    )

    # Grafik candlestick (baris 1)
    fig.add_trace(
        go.Candlestick(
            x=df["Open time"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="BTC/USDT",
        ),
        row=1, col=1,
    )

    # Grafik volume (baris 2)
    fig.add_trace(
        go.Bar(x=df["Open time"], y=df["Volume"], name="Volume"),
        row=2, col=1,
    )

    fig.update_layout(
        title="Bitcoin (BTC) Harian 2018 - 2025",
        height=750,
        xaxis_rangeslider_visible=False,  # sembunyikan slider bawah
        showlegend=False,
    )
    fig.update_yaxes(title_text="Harga (USDT)", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)

    # Kembalikan grafik sebagai HTML (plotly.js dari CDN, perlu internet)
    return fig.to_html(full_html=False, include_plotlyjs="cdn")

@app.route("/")
def index():
    df = load_data()
    chart_html = build_chart(df)
    return render_template("index.html", chart=chart_html)

if __name__ == "__main__":
    app.run(debug=True)
