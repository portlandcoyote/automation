# How to run

## Installing dependencies 
If using a MacOS or Linux I recommend using a package manager to install the following dependencies.
A popular package manager for MacOS is Homebrew, which you can download here:
https://brew.sh/

If you would rather not use a package manager, make sure you download the following dependencies directly:

Make sure you have Git installed on your computer.
https://git-scm.com/downloads

After completing the git download, you should be able to open your terminal and verify by typing:
```bash
git --version
>>> 2.42.0 (any version number means it was successful)
```

Make sure you have Python3 installed on your computer.
After completing the python download, you should be able to open your terminal and verify by typing:
https://www.python.org/downloads/
```bash
python3 --version
```

Using homebrew to download Git and Python:
Open your terminal and type the following commands one at a time, hitting enter after each one.
```bash
brew install git
brew install python
```

Once you have git and python installed. In your home directory in your terminal type the following commands one at a 
time again:
```bash
echo 'export PATH="$(brew --prefix python)/bin:$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

You are now ready to run the shell script to format coyote observation data.

## Pulling the repository

Open your terminal and navigate to where you would like to store these files locally.
You use the command `cd` to change to a directory (folder) that you want to be the parent of these files.
E.g.,
```bash
cd Documents/coyotes
```

You'll then clone the repository like so:
```bash
git clone [the link to the git repository -- copied from GitHub]
```

You should now see a folder with the repository name with all the files in it.

## First time running

Ensure that the main python script and the bash script in the repository are executable.
You can do so by typing the following in the project directory terminal:

```bash
chmod +x main.py
chmod +x get_coyote_data.sh 
```

## Running

Open your terminal and navigate to the project directory, may look something like this:
```bash
cd Documents/coyotes/automation
```

Download the observation form results from qualtrics as a csv. 
Save the csv in whatever way you want, as long as it is in the current directory.
An example could be:
>>> automation/data_pulls/2023/fall/raw.csv

Each name following the slashes (/) is a folder inside the automation directory.
The csv file can also be named whatever you like. 
For example:
>>> automation/data_pulls/2023/fall/november_24.csv

Now without leaving the automation directory, type in the terminal this command:
```bash
./get_coyote_data.sh [path_to_file]
```

Note:
Do not literally type path_to_file, type in the relative file path to the newly saved csv. 
So if it was saved like the example above the command would be:
```bash
./get_coyote_data.sh ./data_pulls/2023/fall/november_24.csv
```

You should now have in the current directory a:
master.csv
rejected.csv
ago.csv
qualtrics_ref.csv

Done!

### Project must-haves

* Place the lat / lng coordinates into separate columns
* Determine time code (DAY / NIGHT / UNSPECIFIED)
    * sunrise and sunset for each lat/long 
    * pull from NOAA 
    * ensure that NOAA incorporated daylight savings 
* Leave off the last two weeks (for ArcGISOnline csv)

### Downloading qualtrics survey instructions

When downloading from qualtrics, these are the options to select:

-> Download all fields
Numeric responses or choice text:
-> Use choice text
-> Split multi-value fields into columns

### Reasons to reject observations

- No lat/long
- No consent
- Survey Preview
