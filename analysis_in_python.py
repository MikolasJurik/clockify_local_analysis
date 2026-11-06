import pandas as pd
from plotnine import *
from datetime import datetime,date

data = pd.read_csv("clockify_export.csv")
data["datum"] = pd.to_datetime(data["start"],utc=True).dt.date

rozcestnik = input("Wish to:\n a) analyze all data \n b) specify time interval\n (a/b) ")
if rozcestnik not in ["a","b"]:
    print("bad input - answer only y or n")
    rozcestnik = input("Wish to:\n a) analyze all data \n b) specify time interval\n (a/b) ")

if rozcestnik == "b":
    datum_od = datetime.strptime(input("Date as start of the time interval you want to see in Y-m-d format (for example 2001-01-01): "),"%Y-%m-%d").date() or date(2000,1,1)
    datum_do = datetime.strptime(input("Date as end of time interval you want to see in Y-m-d format (for example 2001-01-01): "),"%Y-%m-%d").date() or date.today()
elif rozcestnik == "a":
    datum_od= date(2000,1,1)
    datum_do = date.today()


vyrez = data.loc[(data["datum"] >= datum_od) & (data["datum"]<=datum_do), ["project_name", "description", "duration_hours"]]

dle_projektu = vyrez.groupby("project_name")[["duration_hours"]].sum().reset_index().sort_values("duration_hours",ascending=False)
dle_popisku = vyrez.groupby(["project_name","description"],dropna=False).agg("sum").reset_index().sort_values("duration_hours",ascending=False)


#sloupec graf
(
ggplot(dle_projektu, aes(x="project_name", y="duration_hours"))
+ geom_col()
+ coord_flip()
+ scale_x_discrete(limits=dle_projektu["project_name"].tolist()[::-1])
 + labs(
        title=f"Logged hours form {datum_od} to {datum_do} ",
        x="Projext",
        y="Hours",
        caption=""
    )
+ theme_538()
)

dle_projektu.to_csv(f"Hours logged from {datum_od} to {datum_do}.csv",index=False)

