import pandas as pd

data = pd.read_csv("clockify_export.csv")

vyrez = data[["project_name","description", "duration_hours"]]

celkove_dle_projektu = vyrez.groupby("project_name")[["duration_hours"]].sum().sort_values("duration_hours",ascending=False)

dle_popisu = vyrez.groupby(["project_name","description"])["duration_hours"].sum()

