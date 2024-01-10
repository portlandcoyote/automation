import pandas as pd
from datetime import datetime, timedelta

RECORDED_DATE_COLUMN = 'Recorded Date'
TWO_WEEKS_AGO = datetime.today() - timedelta(days=14)


def main():
    df = pd.read_csv('master.csv')

    df['Sort ID'] = 'M' + df['Sort ID'].astype(str)
    df = df.rename(columns={'Sort ID': 'MAP ID'})

    desired_order = [
        'MAP ID',
        'Date of observation',
        'Time of observation',
        'Time Code',
        'Latitude',
        'Longitude'
    ]

    columns_to_drop = [name for name in df.columns if name not in desired_order]

    # Create a mask to filter out the rows that fall within the last two weeks
    df[RECORDED_DATE_COLUMN] = pd.to_datetime(df[RECORDED_DATE_COLUMN], format='mixed', errors='coerce')
    df = df[df[RECORDED_DATE_COLUMN] < TWO_WEEKS_AGO]

    df = df.drop(columns=columns_to_drop)
    df = df.reindex(columns=desired_order)

    df.to_csv('arc_gis_online.csv', index=False)


if __name__ == "__main__":
    main()
