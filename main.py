#!/usr/bin/env python3

import sys
import os
import pandas as pd
import pytz
import numpy as np
import json
from astral.sun import sun
from astral import LocationInfo
from datetime import datetime

import constants


def main():

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.isfile(file_path):
            print("Executing program.")
        else:
            print("File does not exist or is not a regular file.")
            print("Aborting program.")
            return None
    else:
        print("No file path provided.")
        print("Aborting program.")
        return None

    # Open CSV file
    df = pd.read_csv(file_path)

    try:
        json.loads(df.iloc[constants.JSON_ROW_INDEX, 0])  # Parse the first column in this row as JSON
        is_json_metadata = True
    except json.JSONDecodeError:
        is_json_metadata = False

    if is_json_metadata:
        # Drop the row if it's the qualtrics json metadata
        df = df.drop(constants.JSON_ROW_INDEX)
        df = df.reset_index(drop=True)

    df = df.drop(0)  # Drop zuriel's headers preemptively.
    # Sort dataframe by recorded date
    df = df.sort_values(constants.RECORDED_DATE_COLUMN)

    # Rejected.csv ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # Create masks to use to filter rows that should be rejected:
    mask_lat_long_reject = pd.isna(df[constants.LAT_LONG_COLUMN]) | (df[constants.LAT_LONG_COLUMN] == '')  # No lat long.
    mask_response_type_reject = df[constants.RESPONSE_TYPE_COLUMN] == constants.RESPONSE_REJECT  # No survey previews.
    mask_consent_reject = df[constants.CONSENT_COLUMN].str.contains(r'\bnot\b', case=False)

    # Combine the masks using UNION (bitwise logical OR)
    combined_mask = mask_lat_long_reject | mask_response_type_reject | mask_consent_reject

    if os.path.isfile(constants.REJECTED_FILE_PATH):
        rejected = pd.concat([pd.read_csv(constants.REJECTED_FILE_PATH), df[combined_mask]], ignore_index=True)
    else:
        # Create a dataframe for the CSV for rejected rows
        rejected = df[combined_mask]

    # Export the rejected dataframe to a CSV file
    rejected.to_csv('rejected.csv', index=False)

    # Drop those rejected rows from the dataframe.
    df = df.dropna(subset=[constants.LAT_LONG_COLUMN])  # No lat long values.
    df = df[df[constants.RESPONSE_TYPE_COLUMN] != constants.RESPONSE_REJECT]  # No survey previews.
    df = df[~mask_consent_reject]  # '~' is the logical NOT bitwise operator in this context. Always need consent.

    # Check if master.csv exists ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    if os.path.isfile(constants.MASTER_FILE_PATH):  # Update to master.csv
        master_df = pd.read_csv(constants.MASTER_FILE_PATH)
        last_sort_id = master_df[constants.SORT_ID_COLUMN].iloc[-1]
        rows_to_drop = df.shape[0] - master_df.shape[0]

        df = df.iloc[rows_to_drop:]
        df.insert(0, constants.SORT_ID_COLUMN, np.arange(int(last_sort_id) + 1, int(last_sort_id) + 1 + len(df)),
                  allow_duplicates=False)
    else:  # Init master.csv
        # Create a 'sort ID' column for the df
        df.insert(0, constants.SORT_ID_COLUMN, np.arange(1, len(df) + 1), allow_duplicates=False)

    # Convert our date column that is currently strings to datetime objects for comparisons
    df[constants.DATE_COLUMN] = pd.to_datetime(df[constants.DATE_COLUMN], format='mixed', errors='coerce')
    df[constants.RECORDED_DATE_COLUMN] = pd.to_datetime(df[constants.RECORDED_DATE_COLUMN], format='mixed', errors='coerce')

    # Grab the lat/lng values from the column
    lat_and_long = df[constants.LAT_LONG_COLUMN]
    # Create two new columns, extracting the values from the regular expression result from the lat and long column
    df[['latitude', 'longitude']] = lat_and_long.str.extract(constants.LAT_LONG_REGEX, expand=True)
    # Create three new columns, sunrise, sunset, and time code.
    df = df.assign(sunrise='', sunset='', time_code='')

    # calc each sunrise and sunset and fill in each row
    for index, row in df.iterrows():
        latitude = row['latitude']
        longitude = row['longitude']
        observation_date = row[constants.DATE_COLUMN]
        observation_time = row[constants.OBSERVATION_TIME_COLUMN]
        observation = None
        time_zone = pytz.timezone('America/Los_Angeles')

        if pd.notna(observation_date) and pd.notna(observation_time):
            # Get our date back into a string to compare sunsets and sunrises
            observation_date = observation_date.strftime('%Y-%m-%d')
            # Split the observation_time to keep only hours and minutes
            observation_time = observation_time.split(':')[0] + ':' + observation_time.split(':')[1]
            # Combine the date and time to create the final datetime string
            date_time_str = f'{observation_date} {observation_time}'

            # Did I say a string? I meant right back into a datetime object
            try:
                combined_date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
                observation = time_zone.localize(combined_date_time)  # Localized to compare datetime objects
            except ValueError:
                # Handle the case where date_time_str is not in the expected format
                print(f"Error: Invalid date_time_str format for row with date: {date_time_str}")

        if not observation:
            df.loc[index, 'time_code'] = constants.UNSPECIFIED
        else:
            location = LocationInfo('Portland', 'USA', 'US/Western', latitude, longitude)
            s = sun(location.observer, date=observation)
            sunrise = s['sunrise']
            sunset = s['sunset']

            df.loc[index, 'sunrise'] = sunrise
            df.loc[index, 'sunset'] = sunset

            if sunrise <= observation < sunset:
                df.loc[index, 'time_code'] = 'Day'
            else:
                df.loc[index, 'time_code'] = 'Night'

    # Convert our date values back into the desired string format
    df[constants.DATE_COLUMN] = df[constants.DATE_COLUMN].dt.strftime('%m-%d-%Y')

    # Fill empty date and time blank values with 'Unspecified'
    df[constants.DATE_COLUMN].fillna(constants.UNSPECIFIED, inplace=True)
    df[constants.OBSERVATION_TIME_COLUMN].fillna(constants.UNSPECIFIED, inplace=True)

    # Make Qualtrics Reference csv ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    qr_columns_to_drop = [name for name in df.columns if name not in constants.QR_ORDER]
    qr_df = df.drop(columns=qr_columns_to_drop).reindex(columns=constants.QR_ORDER)

    if os.path.isfile(constants.QR_FILE_PATH):
        # Delete headers before adding with previous csv
        qr_df = pd.concat([pd.read_csv(constants.QR_FILE_PATH), qr_df], ignore_index=True)

    qr_df.to_csv('qualtrics_ref.csv', index=False)

    # Export Master.csv ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    master_columns_to_drop = [name for name in df.columns if name not in constants.MASTER_ORDER]

    df = df.drop(columns=master_columns_to_drop) \
        .reindex(columns=constants.MASTER_ORDER) \
        .rename(columns=constants.MASTER_COLUMNS)

    if os.path.isfile(constants.MASTER_FILE_PATH):
        master_df = pd.concat([pd.read_csv(constants.MASTER_FILE_PATH), df], ignore_index=True)
        master_df.to_csv('master.csv', index=False)
    else:
        # Export the updated dataframe to a new CSV file
        df.to_csv('master.csv', index=False)


if __name__ == "__main__":
    main()
