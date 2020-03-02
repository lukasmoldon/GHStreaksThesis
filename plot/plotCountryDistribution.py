import plotly.express as px
import country_converter as coco
import json
import pandas as pd

cc = coco.CountryConverter()

with open("C:/Users/Lukas/Desktop/countryDistribution.json", "r") as fp:
    countrydata = json.load(fp)

del countrydata["Jamaika"]
del countrydata["Unknown"]

plotdata = pd.DataFrame(columns=["iso_alpha", "value"])

cnt = 0
for name in countrydata:
    cnt += countrydata[name]

for name in countrydata:
    res = cc.convert(names=name, to="ISO3")
    if len(res) == 3:
        value = countrydata[name]/cnt
        plotdata = plotdata.append({"iso_alpha":res, "value":value}, ignore_index=True)


fig = px.choropleth(plotdata, locations="iso_alpha",
                    color="value", # lifeExp is a column of gapminder
                    color_continuous_scale=px.colors.sequential.Sunsetdark,
                    labels={"value":"share of users"})
fig.show()