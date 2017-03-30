>**Note:**
>This Readme has been automatically created by [zepppelin2md.py](https://github.com/bernhard-42/zeppelin2md).

>Alternatively, load into your Zeppelin instance using the URL 
>    `https://raw.githubusercontent.com/bernhard-42/nvd3-stat/master/notebooks/Zeppelin-Nvd3-Demo.json`

# notebooks/Zeppelin-Nvd3-Demo.json

---

#### Check Versions

_Input:_

```python
%pyspark

def versionCheck():
    import sys
    print("Python: " + sys.version.replace("\n", " - "))
    print("Spark:  " + sc.version)

def display(html, style=None):
    print("%html")
    if isinstance(html, (tuple, list)):
        html = "".join(["""<div style="display:inline; margin-left:%dpx">%s</div>""" % (el[1], el[0]) for el in html])
    if style is not None:
        html = "<%s>%s</%s>" % (style, html, style)
    print(html)

def getNoteId():
    return z.z.getInterpreterContext().getNoteId()

def getParagraphId():
    return z.z.getInterpreterContext().getParagraphId()


# The variable z holds the zeppelinContext. It is essential for all Angular based interactions - so let's save it :-)
ZEPPELIN_CONTEXT = z.z

# In case one overwrites z, z = recoverZeppelinContext() gets the context back
def recoverZeppelinContext():
    return PyZeppelinContext(ZEPPELIN_CONTEXT)

versionCheck()
```


---

#### Some helpers to create data

_Input:_

```python
%pyspark

import numpy as np
import pandas as pd
import random
import time
from datetime import datetime

pd.options.display.width=200

def randomList(count, mean, dist):
    return [ mean + (1 if random.random() > 0.5 else -1) * random.random() * dist for i in range(count)]


def randomNormalList(count, mean, stdev):
    return np.random.normal(mean, stdev, count).tolist()


def randomWalk(count=20, factor=2, offset=10):
    return np.abs(np.cumsum(np.random.uniform(-factor, factor, (count, 1)) ) + offset)


def lastDays(days, epoch=True, ms=True):
    now = datetime.now()
    t = int(time.mktime(now.timetuple())) - 3600 * 24 * days
    if epoch:
        factor = 1000 if ms else 1
        return [int(t + i * 3600 * 24) * factor for i in range(days)]
    else:
        return [time.strftime('%Y-%m-%d', time.localtime(int(t + i*3600*24))) for i in range(days)]
        
```


---

#### Stock data loader

_Input:_

```python
%pyspark

#
# pip install yahoo-finance
#

from yahoo_finance import Share     

def downloadHistoricalStockData(symbol, begin, end, fillMissing=True):
    data = Share(symbol).get_historical("%04d-%02d-%02d" % begin, "%04d-%02d-%02d" % end)
    df = pd.DataFrame(data)

    for col in "Adj_Close", "Close", "High", "Low", "Open":
        df[col] = df[col].astype(float)
    df["Volume"] = df["Volume"].astype(int)
    df["Date"] = pd.to_datetime(df["Date"], infer_datetime_format=True)
    
    if fillMissing:
        return fillMissingValues(df, symbol, begin, end)
    else: 
        return df

def fillMissingValues(df, symbol, begin, end):
    allDates = pd.DataFrame({"Date": pd.date_range(pd.datetime(*begin), pd.datetime(*end), freq='D')})
    df2 = allDates.merge(df, how="outer")
    df2["Symbol"] = symbol
    # for volume fill bank holidays with 0 (no trade)
    df2["Volume"] = df2["Volume"].fillna(0)
    # and all indicators with value of day before (no price change)
    df2 = df2.fillna(axis=0, method="ffill")
    df2["Timestamp"] = (df2["Date"].astype("int64") / 1000000).astype('int64')
    return df2.sort_values(by=["Timestamp"])
    
```


---

#### Iris data download ...

_Input:_

```bash
%sh
cd /tmp
wget  https://raw.github.com/pydata/pandas/master/pandas/tests/data/iris.csv
```


---

#### ... and as pandas  DataFrame

_Input:_

```python
%pyspark

import pandas as pd
iris = pd.read_csv('/tmp/iris.csv')

def getSpecies(name):
    return iris[iris.Name==name].loc[:,iris.columns != 'Name']

print(iris.head())
```


---

## 1 Preparation


---

#### Initialize ZeppelinSession ...

_Input:_

```python
%pyspark

from zeppelin_session import ZeppelinSession, resetZeppelinSession, LogLevel, Logger

resetZeppelinSession(z.z)

zs = ZeppelinSession(z.z)
```


---

#### ... and start it in the next paragraph

_Input:_

```python
%pyspark

zs.start()
```


---

#### Initialize NVD3

_Input:_

```python
%pyspark

from nvd3_stat import Nvd3

nv = Nvd3()
nv.reloadNVD3("1.8.5")
```


---


## Limitations

- ZeppelinSession is a pure frontend integration, hence a **shared notebook will not see the charts**
- ZeppelinSession depends on the Angular scope of the notebook, after leaving and re-entering the notebook, the scope is gone and the **charts are gone**


---

## 1 Box Plot Chart
### a) Single IQR Box Plot


---


_Input:_

```python
%pyspark
df = pd.DataFrame({"X1":randomNormalList(50, 5, 1), "X2":randomNormalList(50, 3, 0.5)})

bp1 = nv.boxPlotChart()

config={"height": 400, "width":450, "color":nv.c10(), "yDomain": [0, 10], "maxBoxWidth":False }

bp1.plot(data=df, boxStyle="iqr", config=config)
```


---

### b) Append values


---


_Input:_

```python
%pyspark
bp1.append({"X1":[1,5,7,8,9,8,7], "X2":[0.5, 3,4,5,6,3,2]})
```


---

### c) Horizontal Plots


---

#### Compare the three species (IQR box plot)

_Input:_

```python
%pyspark

display(html=[("Iris-setosa", 40),("Iris-versicolor", 330),("Iris-virginica", 300)], style="h3")

bp2 = nv.boxPlotChart()

config = {"height": 400, "width":450, "color":nv.c10(), "yDomain": [-0.5, 8.5], "maxBoxWidth":False}

bp2.hplot([bp2.chart(getSpecies("Iris-setosa"),     boxStyle="iqr", config=config),
           bp2.chart(getSpecies("Iris-versicolor"), boxStyle="iqr", config=config),
           bp2.chart(getSpecies("Iris-virginica"),  boxStyle="iqr", config=config)])
```


---

#### Compare IQR and Min-Max box plot

_Input:_

```python
%pyspark

bp3 = nv.boxPlotChart()

config = {"height": 400, "width":450, "color":nv.c10(), "yDomain": [-0.5, 6], "maxBoxWidth":False }

bp3.hplot([bp3.chart(data=getSpecies("Iris-setosa"), boxStyle="iqr",     config=config),
           bp3.chart(data=getSpecies("Iris-setosa"), boxStyle="min-max", config=config)])
```


---


## 2 Line Chart

### a) Plot


---


_Input:_

```python
%pyspark
x = np.linspace(0, 4*np.pi, 100)

l_df = pd.DataFrame({"X":x,
                     "Sin":np.sin(x), 
                     "Cos":np.cos(x), 
                     "ArcTan":np.arctan(x-2*np.pi)/3})

print(l_df.head())
```


---

#### Single line

_Input:_

```python
%pyspark
l1 = nv.lineChart()

config={"height":350, "width": 800, "color":nv.c10(), 
        "yAxis":{"axisLabel":"f(x)", "tickFormat":",.2f"}, 
        "xAxis":{"axisLabel":"x",    "tickFormat":",.2f"}}
        
lineAttributes={"area":True, "fillOpacity":0.2, "style":"dashed"}

l1.plot(l_df, "X", "Sin", lineAttributes, config)
```


---


_Input:_

```python
%pyspark
l2 = nv.lineChart()

def config(i):
    return {"height":300, "width": 400, "color":nv.c10()[i-1:], 
            "yAxis":{"axisLabel":"f(x)", "tickFormat":",.2f"}, 
            "xAxis":{"axisLabel":"x",    "tickFormat":",.2f"},
            "yDomain":[-1.2,1.2]}

lineAttributes1={"area":True,  "fillOpacity":0.2, "style":"dashed"}
lineAttributes2={"area":False,                    "style":"dotted"}
lineAttributes3={"area":True,  "fillOpacity":1.0                  }

l2.hplot([l2.chart(l_df, "X", "Sin",    lineAttributes1, config=config(1)),
          l2.chart(l_df, "X", "Cos",    lineAttributes2, config=config(2)),
          l2.chart(l_df, "X", "ArcTan", lineAttributes3, config=config(3))])
```


---

#### Multiple lines

_Input:_

```python
%pyspark
l3 = nv.lineChart()

config={"height":500, "width": 1024, "color":nv.c20b()[10:13], 
        "yAxis":{"axisLabel":"f(x)", "tickFormat":",.2f"}, 
        "xAxis":{"axisLabel":"x",    "tickFormat":",.2f"},
        "focusEnable": False, "duration":0}
        
lineAttributes={"area":[True, False, True], "fillOpacity":[0.2, 0, 0.2], "style":["dashed", "dotted", None]}

l3.plot(l_df[:70], "X", ["Sin", "Cos", "ArcTan"], lineAttributes, config)
```


---

### b) Append values


---


_Input:_

```python
%pyspark
for i in range(71,100):
    time.sleep(0.05)
    l3.append(l_df[i:i+1])
    
```


---


### c) Save it as PNG


---


_Input:_

```python
%pyspark
l3.saveAsPng("line.png", backgroundColor="white")
```


---


### d) Multiplie independent lines


---


_Input:_

```python
%pyspark
# data taken from scikit-learn http://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html

data = {'FPR': [0.0000,0.0000,0.0196,0.0196,0.0784,0.0784,0.0980,0.0980,0.1176,0.1176,0.1373,
                0.1373,0.1569,0.1569,0.1765,0.1765,0.3137,0.3137,0.3333,0.3333,0.3529,0.3529,
                0.4118,0.4118,0.4510,0.4510,0.4706,0.4706,0.5098,0.5098,0.5686,0.5686,1.0000],
        'TPR': [0.0417,0.1250,0.1250,0.2500,0.2500,0.2917,0.2917,0.3333,0.3333,0.4167,0.4167,
                0.5000,0.5000,0.5417,0.5417,0.5833,0.5833,0.6667,0.6667,0.7500,0.7500,0.7917,
                0.7917,0.8333,0.8333,0.8750,0.8750,0.9167,0.9167,0.9583,0.9583,1.0000,1.0000]}

config = {"width":600, "height":500, "color":nv.c20(2,1), "useInteractiveGuideline":True,
          "xDomain":[0,1], "yDomain":[0,1.05],
          "xAxis":{"axisLabel":"False Positive Rate"},
          "yAxis":{"axisLabel":"True Positive Rate"}
         }

display(html=[("ROC", 300)], style="h3")

roc = nv.lineChart()
roc.addLine(data, "FPR", "TPR")
roc.addLine({"X":[0,1], "Threshold":[0,1]}, "X", "Threshold", lineAttributes={"style":"dotted"})
roc.plot(config=config)
```


---


### e) Add a focus selector


---


_Input:_

```python
%pyspark
l2 = nv.lineChart()

config={"height":500, "width": 1024,
        "focusEnable": True, "color":nv.c10(), 
        "yAxis": {"axisLabel":"f(x)", "tickFormat":",.2f"}, 
        "xAxis":{"axisLabel":"x", "tickFormat":"%d-%m-%Y"}}

lineAttributes={"area":[True, False, True], "fillOpacity":[0.2, 0, 0.2], "style":["dashed", "dotted", None]}

l2.plot(l_df, "X", ["Sin", "Cos", "ArcTan"], lineAttributes, config)
```


---


## 3 Discrete Bar Chart

### a) Plot


---


_Input:_

```python
%pyspark
db_df = pd.DataFrame(iris.loc[:, ["SepalLength", "SepalWidth", "PetalLength", "PetalWidth"]].mean()).reset_index()
db_df.columns = ["Series", "Mean"]

db = nv.discreteBarChart()

config={"height": 350, "width": 500, "color": nv.c20(), "staggerLabels": False}

db.plot(db_df[:2], key="Series", value="Mean", config=config)
```


---


### b) Append values


---


_Input:_

```python
%pyspark
db.append(db_df[2:])
```


---


## 4 Multi Bar Chart

### a) Plot


---


_Input:_

```python
%pyspark
x = np.linspace(0, 4*np.pi, 10)
mb_df = pd.DataFrame({"X":x, "Sin":np.sin(x), "Cos":np.cos(x), "ArcTan":np.arctan(x-2*np.pi)/3})

mb1 = nv.multiBarChart()

config = {"height":500, "width": 800, 
          "color": nv.c20(),
          "xAxis":{"axisLabel":"x", "tickFormat":",.2f"},
          "yAxis":{"axisLabel":"f(x)", "tickFormat":",.2f"}}

mb1.plot(mb_df[:6], "X", ["Sin", "Cos", "ArcTan"], config)
```


---

### b) Append values


---


_Input:_

```python
%pyspark
for i in range(6,10):
    time.sleep(0.5)
    mb1.append(mb_df[i:i+1])
    
```


---

## 5 Multi Bar Horizontal Chart

### a) Plot


---


_Input:_

```python
%pyspark
mbh = nv.multiBarHorizontalChart()

config = {"height":500, "width": 800, "color":nv.c20()[10:], "stacked":False}

mbh.plot(mb_df[:6], "X", ["Sin", "Cos", "ArcTan"], config)
```


---


### b) Append values


---


_Input:_

```python
%pyspark
mbh.append(mb_df[6:])
```


---


## 6 Line Plus Bar Chart
### a) Plot


---

#### Load HDP historical Stock data

_Input:_

```python
%pyspark

ohlcDf = downloadHistoricalStockData('AAPL', (2016,3,28), (2017,3,27))
ohlcDf["VolumeMio"] = ohlcDf["Volume"] / 10000000
ohlcDf.head(10)
```


---


_Input:_

```python
%pyspark
lpb = nv.linePlusBarChart()

config={"color":[nv.c20()[0], nv.c20()[3]], 
        "height":600, "width":1200,
        "xAxis":{"tickFormat":"%d.%m.%y"},
        "x2Axis":{"tickFormat":"%d.%m.%y"},
        "yDomain":[80, 145],
        "duration":0, "focusEnable":True
}

lpb.plot(ohlcDf[0:300], "Timestamp", lineValue="Close", barValue="Volume", config=config)
```


---


### b) Append values


---


_Input:_

```python
%pyspark
for i in range(301,len(ohlcDf), 5):
    time.sleep(0.5)
    lpb.append(ohlcDf[i:i+5])
    
```


---


## 7 Pie Chart

### a) Plot


---


_Input:_

```python
%pyspark
p1 = nv.pieChart()
p1.plot(db_df, "Series", "Mean", config={"height":300, "width":260})
```


---


_Input:_

```python
%pyspark
p2 = nv.pieChart()

config1={"donut": False,                  "color": nv.c10(),  "width": 300, "height":400}
config2={"donut": True,                   "color": nv.c20(),  "width": 300, "height":400}
config3={"donut": True,  "halfPie": True, "color": nv.c20b(), "width": 300, "height":400}

p2.hplot([p2.chart(db_df[:2], "Series", "Mean", config=config1), 
          p2.chart(db_df[:2], "Series", "Mean", config=config2), 
          p2.chart(db_df[:2], "Series", "Mean", config=config3)])
```


---

### b) Append values


---


_Input:_

```python
%pyspark
for chart in range(3):
    p2.append(db_df[2:], chart=chart)
    
```


---


## 8 Stacked Area Chart

### a) Plot


---


_Input:_

```python
%pyspark
count = 100
groups = 5

series = []
for i in range(groups):
    factor = np.random.randint(5,10)
    offset = np.random.randint(20,100)
    series.append(randomWalk(count, 20, offset).tolist())

sa_df = pd.DataFrame([lastDays(count, epoch=True)] + series).T
sa_df.columns = ["Date"] + ["Series %d" % i  for i in range(groups)]
sa_df.head(2)
```


---


_Input:_

```python
%pyspark
sa = nv.stackedAreaChart()

config={"color": nv.c20(), "height":500, "xAxis":{"tickFormat":"%d.%m.%Y"}, "duration":0}

sa.plot(sa_df[:80], "Date", ["Series %d" % i for i in range(groups)], config=config)
```


---

### b) Append values


---


_Input:_

```python
%pyspark
for i in range(80, 100, 2):
    time.sleep(0.1)
    sa.append(sa_df[i:i+2])
```


---


## 9 Scatter Plus Line Chart

### a) Plot


---


_Input:_

```python
%pyspark
spl_df = pd.DataFrame({chr(65+i): randomNormalList(40, 4, 1) for i in range(4)})
spl_df["S1"] = "diamond"
spl_df["S2"] = "square"
spl_df.head(2)
```


---


_Input:_

```python
%pyspark
# ScatterPlusLineChart has an issue with lines in Jupyter and Zeppelin from 1.8.3 onwards, so switch to 1.8.2
nv.reloadNVD3("1.8.2")
```


---


_Input:_

```python
%pyspark
spl1 = nv.scatterPlusLineChart()

config = {"color":nv.c10(), 
          "xDomain":[0, 8], "xAxis":{"axisLabel":"A: squares,  C: diamonds"},
          "yDomain":[0, 8]}

data = spl1.plot(spl_df[:30], keys=["A", "C"], values=["B", "D"], pointAttributes={"shapes":["S1", "S2"]},
                 lines=[{"slope":1.0, "intercept":-1.0}, {"slope":-0.6, "intercept":6.0}], config=config)
                 
```


---

### b) Append values


---


_Input:_

```python
%pyspark
for i in range(30,40):
    time.sleep(0.5)
    spl1.append(spl_df[i:i+1], 
                lines=[{"slope":30.0/i, "intercept":-1.0}, {"slope":-20.0/i, "intercept":6.0}])
                
```


---

### c) Example


---


_Input:_

```python
%pyspark
from sklearn import linear_model

setosa     = iris[iris.Name == "Iris-setosa"]
versicolor = iris[iris.Name == "Iris-versicolor"]
virginica  = iris[iris.Name == "Iris-virginica"]

def linReg(x,y):
    regr = linear_model.LinearRegression()
    regr.fit(x,y)
    return (regr.coef_.item(0), regr.intercept_.item(0))
    
def prepare(df, name):
    sepal = df.loc[:,["SepalLength", "SepalWidth"]]
    sepal.columns = ["X", name]
    sepal["Shape"] = "diamond"
    petal = df.loc[:,["PetalLength", "PetalWidth"]]
    petal.columns = ["X", name]
    petal["Shape"] = "square"
    
    df = pd.concat([sepal, petal])
    x = df["X"].values.reshape(df.shape[0], 1)
    y = df[name].values.reshape(df.shape[0], 1)
    slope, intercept = linReg(x,y)

    df["Size"] = 2
    df = df.groupby(["Shape", "X", name]).sum().reset_index()
    return (df, slope, intercept)

setosaDf,     setosaSlope,     setosaIntercept     = prepare(setosa,     "Setosa")
virginicaDf,  virginicaSlope,  virginicaIntercept  = prepare(virginica,  "Virginica")
versicolorDf, versicolorSlope, versicolorIntercept = prepare(versicolor, "Versicolor")
```


---


_Input:_

```python
%pyspark
spl2 = nv.scatterPlusLineChart()

config = {"height":700, #"xDomain":[0,8], "yDomain":[0,4.5],
          "xAxis":{"axisLabel":"Length (sepal=diamond, petal=square)"}, "yAxis":{"axisLabel":"Width (sepal=diamond, petal=square)"}
}

spl2.addScatter(setosaDf,     "X", "Setosa",     lines={"slope":setosaSlope, "intercept":setosaIntercept}, 
                                                 pointAttributes={"shapes":"Shape", "sizes":"Size"})
spl2.addScatter(virginicaDf,  "X", "Virginica",  lines={"slope":virginicaSlope, "intercept":virginicaIntercept}, 
                                                 pointAttributes={"shapes":"Shape", "sizes":"Size"})
spl2.addScatter(versicolorDf, "X", "Versicolor", lines={"slope":versicolorSlope, "intercept":versicolorIntercept}, 
                                                 pointAttributes={"shapes":"Shape", "sizes":"Size"})

spl2.plot(config=config)
```


---


_Input:_

```python
%pyspark
# Switch back to 1.8.5
nv.reloadNVD3("1.8.5")
```


---


## 10 Parallel Coordinates Plot


---


_Input:_

```python
%pyspark
iris.loc[iris.Name=="Iris-setosa",     "color"] = nv.c10()[0]
iris.loc[iris.Name=="Iris-versicolor", "color"] = nv.c10()[1]
iris.loc[iris.Name=="Iris-virginica",  "color"] = nv.c10()[2]
iris["strokeWidth"] = 0.5
iris.head()
```


---


_Input:_

```python
%pyspark
pc = nv.parallelCoordinatesChart()

config = {"height": 600}

pc.plot(iris, 'Name', ['SepalWidth', 'SepalLength', 'PetalWidth', 'PetalLength'],
        lineAttributes=["color", "strokeWidth"], 
        dimAttributes= {"format": [",.1f", ",.1f", ",.1f", ",.1f"]},
        config=config)
        
```


---

## 11 Historical Bar Chart


---


_Input:_

```python
%pyspark
hb = nv.historicalBarChart()

config = {"color":nv.c20()[4:],
          "xAxis":{"axisLabel":"Date (d.m.y)"},
          "yAxis":{"axisLabel":"Volume (Mio)", "tickFormat":",.2f"}}

hb.plot(ohlcDf, "Timestamp", "VolumeMio",config=config)
```


---

## 12 Candlestick Chart


---


_Input:_

```python
%pyspark
cs = nv.candlestickBarChart()

config = {"color":nv.c10(), "yDomain":[114,145], "width":1400, "height":800,
          "xAxis":{"tickFormat":"%d/%m/%Y", "axisLabel":"Date (d/m/y)"},
          "yAxis":{"axisLabel":"Close (USD)"}}

ohlcAttribs = {"open":"Open" ,"high":"High" ,"low":"Low" ,"volume":"Volume" ,"adjusted":"Adj_Close"}

cs.plot(ohlcDf[-80:], "Timestamp", "Close", ohlcAttribs, config=config)
```


---

## 13 OHLC Chart


---


_Input:_

```python
%pyspark
ohlc = nv.ohlcBarChart()

config = {"color":nv.c10(), "yDomain":[114,145], "width":1400, "height":800,
          "xAxis":{"tickFormat":"%d/%m/%Y", "axisLabel":"Date (d/m/y)"},
          "yAxis":{"axisLabel":"Close (USD)"}}

ohlcAttribs = {"open":"Open" ,"high":"High" ,"low":"Low" ,"volume":"Volume" ,"adjusted":"Adj_Close"}

ohlc.plot(ohlcDf[-90:], "Timestamp", "Close", ohlcAttribs, config=config)
```


---

## 14 Bullet Chart


---


_Input:_

```python
%pyspark
def getData(title, actual, previous):
    return {"title":title, "subtitle":"out of 5",
            "ranges":{'Bad':3.5, 'OK':4.25, 'Good':5},
            "measure":{'Current':actual},
            "markers":{'Previous':previous},
            "markerLines":{'Threshold':3.0, 'Target':4.4}}
                
b1 = nv.bulletChart()

config = {"height":60, "width":600}

b1.vplot([b1.chart(config=config, **getData("Satisfaction", 3.9, 3.8)),
          b1.chart(config=config, **getData("Satisfaction", 4.3, 3.8))])
          
```

