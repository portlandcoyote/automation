from datetime import datetime, timedelta

LAT_LONG_COLUMN = 'Q26'
OBSERVATION_TIME_COLUMN = 'Q19.1'
RECORDED_DATE_COLUMN = 'RecordedDate'
DATE_COLUMN = 'Q19'
RESPONSE_TYPE_COLUMN = 'Status'
CONSENT_COLUMN = 'Q21'
SORT_ID_COLUMN = 'Sort ID'
LAT_LONG_REGEX = r'lat":(\d+\.\d+),"lng":(-?\d+\.\d+)'
RESPONSE_REJECT = 'Survey Preview'
TWO_WEEKS_AGO = datetime.today() - timedelta(days=14)
JSON_ROW_INDEX = 1
UNSPECIFIED = 'Unspecified'
MASTER_FILE_PATH = 'master.csv'
QR_FILE_PATH = 'qualtrics_ref.csv'
AGO_FILE_PATH = 'arc_gis_online.csv'
REJECTED_FILE_PATH = 'rejected.csv'

# Qualtrics Reference Desired layout
QR_ORDER = [
    'Sort ID',
    'ResponseId'
]

# Master Desired layout
MASTER_ORDER = [
    'Sort ID',
    'RecordedDate',
    'Q19',
    'Q19.1',
    'time_code',
    'latitude',
    'longitude',
    'sunrise',
    'sunset',
    'Q7_1',
    'Q7_2',
    'Q7_3',
    'Q7_4',
    'Q7_5',
    'Q7_6',
    'Q7_6_TEXT',
    'Q8',
    'Q9',
    'Q23_1',
    'Q23_4',
    'Q23_5',
    'Q23_6',
    'Q23_6_TEXT',
    'Q22_4',
    'Q22_5',
    'Q22_6',
    'Q22_7',
    'Q22_7_TEXT',
    'Q24_1',
    'Q24_4',
    'Q24_5',
    'Q24_6',
    'Q24_7',
    'Q24_8',
    'Q24_9',
    'Q24_10',
    'Q24_11',
    'Q24_11_TEXT',
    'Q25',
    'Q25_6_TEXT',
    'Q11',
    'Q12',
    'Q13',
    'Q13_7_TEXT',
]

MASTER_COLUMNS = {
    'RecordedDate': 'Recorded Date', 'Q19': 'Date of observation', 'Q19.1': 'Time of observation',
    'time_code': 'Time Code', 'latitude': 'Latitude', 'longitude': 'Longitude',
    'Q7_1': 'What was the coyote doing? - Moving slowly', 'Q7_2': 'What was the coyote doing? - Moving quickly',
    'Q7_3': 'What was the coyote doing? - Mostly stationary', 'Q7_4': 'What was the coyote doing? - Vocalizing',
    'Q7_5': 'What was the coyote doing? - Hunting', 'Q7_6': 'What was the coyote doing? - Other',
    'Q7_6_TEXT': 'What was the coyote doing? Other text', 'Q8': 'How many coyotes did you observe',
    'Q9': 'Please select the statement you agree with most',
    'Q23_1': 'Why did you enjoy seeing the coyote - I like wildlife/coyotes',
    'Q23_4': 'Why did you enjoy seeing the coyote - It was a cool experience',
    'Q23_5': 'Why did you enjoy seeing the coyote - Minding its own business',
    'Q23_6': 'Why did you enjoy seeing the coyote - Other',
    'Q23_6_TEXT': 'Why did you enjoy seeing the coyote - Other text',
    'Q22_4': 'Why didnt you enjoy seeing the coyote - Coyote',
    'Q22_5': 'Why didnt you enjoy seeing the coyote - Neighborhood',
    'Q22_6': 'Why didnt you enjoy seeing the coyote - Too bold or aggressive',
    'Q22_7': 'Why didnt you enjoy seeing the coyote - Other',
    'Q22_7_TEXT': 'Why didnt you enjoy seeing the coyote - Other text',
    'Q24_1': 'Why did you have mixed feelings about seeing the coyote? - Coyote',
    'Q24_4': 'Why did you have mixed feelings about seeing the coyote? - Neighborhood',
    'Q24_5': 'Why did you have mixed feelings about seeing the coyote? - Too bold or aggressive',
    'Q24_6': 'Why did you have mixed feelings about seeing the coyote? - I like wildlife/coyotes',
    'Q24_7': 'Why did you have mixed feelings about seeing the coyote? - It was a cool experience',
    'Q24_8': 'Why did you have mixed feelings about seeing the coyote? - Minding its own business',
    'Q24_9': 'Why did you have mixed feelings about seeing the coyote? - I see coyotes all the time',
    'Q24_10': 'Why did you have mixed feelings about seeing the coyote? - I dont care',
    'Q24_11': 'Why did you have mixed feelings about seeing the coyote? - Other',
    'Q24_11_TEXT': 'Why did you have mixed feelings about seeing the coyote? - Other text',
    'Q25': 'Why were you neutral about seeing this coyote - Selected choice',
    'Q25_6_TEXT': 'Why were you neutral about seeing this coyote - Other text',
    'Q11': 'Is there anything else you would like to share about your observation?',
    'Q12': 'What is your home zip code',
    'Q13': 'How did you hear about the Portland Urban Coyote Project - Selected choice',
    'Q13_7_TEXT': 'How did you hear about the Portland Urban Coyote Project - Other text'
    }
