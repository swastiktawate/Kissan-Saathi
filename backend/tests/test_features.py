import datetime

from backend.app.services.features import get_features


def test_lookahead_mutation():
    # To test lookahead mutation, we use the features service.
    # It must not use data > origin_date.
    # If the DB is populated, we can verify the max date in returned DF is <= origin_date
    origin = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
    df = get_features('tomato', 'vashi', origin)
    
    if not df.empty:
        assert df['date'].max().strftime('%Y-%m-%d') <= origin
