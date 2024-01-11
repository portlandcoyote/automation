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
        'Observation Month',
        'Observation Year',
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

    unique_years = df['Observation Year'].unique()

    # Create a CSV file for each unique year
    for year in unique_years:
        # Filter the DataFrame for the current year
        year_df = df[df['Observation Year'] == year]

        # Save the filtered DataFrame as a CSV file
        year_csv_filename = f'{year}.csv'
        year_df.to_csv(year_csv_filename, index=False)


if __name__ == "__main__":
    main()
