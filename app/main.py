from fastapi import FastAPI

app = FastAPI(title="BookingApp",
    description="MDtext",
    summary="My first app",
    version="0.0.1",
)

@app.get('/hotels')
def get_hotels():
    return 'Отель Бридж резорт'
