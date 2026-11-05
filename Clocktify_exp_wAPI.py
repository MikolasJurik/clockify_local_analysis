import requests
import pandas as pd
import os

API_KEY = os.getenv("CLOCKIFY_API_KEY")
headers = {"X-Api-Key": API_KEY}

# Kontrola API klíče
if not API_KEY:
    raise ValueError("API key nebyl nalezen!")

# API endpoint
url = "https://api.clockify.me/api/v1/user"

# Odeslání GET požadavku
response = requests.get(url, headers=headers)

# Kontrola odpovědi
response.raise_for_status()

# Převod JSON na Python slovník
user_data = response.json()

print(user_data)

# Get workspaces
url = "https://api.clockify.me/api/v1/workspaces"

response = requests.get(url, headers=headers)
response.raise_for_status()

workspaces = response.json()
print(workspaces)
for workspace in workspaces:
    print(workspace["name"], workspace["id"])

workspace_id = "67d93bed1d5f4925b9ad989d"
user_id = user_data["id"]

# Get time entries

url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/user/{user_id}/time-entries"

all_entries = []
page = 1

while True:

    params = {
        "page": page,
        "page-size": 200
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    data = response.json()

    all_entries.extend(data)

    print(f"Page {page}: {len(data)} records")

    # Last-Page header tells us whether this is the final page
    if response.headers.get("Last-Page", "").lower() == "true":
        break

    page += 1

time_entries = all_entries
print("Total records:", len(time_entries))

# Get projects
url = f"https://api.clockify.me/api/v1/workspaces/{workspace_id}/projects"

params = {
    "page": 1,
    "page-size": 5000
}

response = requests.get(url, headers=headers, params=params)
response.raise_for_status()

projects = response.json()

print("Number of projects:", len(projects))

for project in projects:
    print(project["id"], project["name"])

project_lookup = {
    project["id"]: project["name"]
    for project in projects
}








# Convert JSON to pandas DataFrame
df = pd.json_normalize(time_entries, sep="_")

# Select relevant columns
df = df[[
    "id",
    "description",
    "projectId",
    "timeInterval_start",
    "timeInterval_end",
    "timeInterval_duration",
    "timeInterval_timeZone"
]]
# Rename columns
df = df.rename(columns={
    "projectId": "project_id",
    "timeInterval_start": "start",
    "timeInterval_end": "end",
    "timeInterval_duration": "duration",
    "timeInterval_timeZone": "timezone"
})
df["project_name"] = df["project_id"].map(project_lookup)


# Convert ISO 8601 duration to timedelta
df["duration_td"] = pd.to_timedelta(df["duration"], errors="coerce")

# Convert duration to hours
df["duration_hours"] = (
    df["duration_td"].dt.total_seconds() / 3600
)




print(df.head())

df["start"] = pd.to_datetime(df["start"], utc=True).dt.tz_convert("Europe/Prague")

df["end"] = pd.to_datetime(df["end"], utc=True).dt.tz_convert("Europe/Prague")

df.to_csv("clockify_export.csv", index=False, encoding="utf-8-sig")

