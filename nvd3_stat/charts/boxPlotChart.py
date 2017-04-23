# Copyright 2017 Bernhard Walter
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ..nvd3_chart import Nvd3Chart
import pandas as pd


class BoxPlotChart(Nvd3Chart):

    funcName = "boxPlotChart"
    funcBody = """
        function(session, object) {
            var chart = nv.models.boxPlotChart()
                        .x(function(d) { return d.key })

            session.__functions.makeChart(session, object, chart);
        }      
    """

    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.df = []
        self.keys = []
        self.boxStyle = []



    def plot(self, data, keys=None, boxStyle="iqr", config={}):
        """
        Create a BoxPlotChart
               
        Example:
            >>> df.head(3)
                    Series A  Series B  Series C  Series D   Series E
                0   7.629883  6.977595  3.323865  7.323412  14.111551
                1  14.067483  6.235542  3.285066  6.990191   7.673949
                2   6.843873  4.333124  4.258416  8.382573   9.060179

            >>> bp = nv.boxPlotChart()
            >>> config = {"height": 400, "width":400, "yDomain":[-5, 25], "maxBoxWidth":False, "color":nv.c10()}
            >>> bp.plot(bp_df, ["Series A", "Series B", "Series D"], boxStyle="iqr", config=config)

        Parameters
        ----------
        data : dict of lists or Pandas DataFrame 
            If the paramter is a dict, each keys represent the name of the dataset in the list
              { 'A': ( 1,   2,   3),
                'B': ('C', 'T', 'D' }
            or a pandas DataFrame, each column representing a dataset
                 A  B
              0  1  C
              1  2  T
              2  3  D
        keys : list of strings (optional)
            Column names to create boxplot for. If missing all columns are used.
        boxStyle : string
            'iqr':     low whisker = q1-1.5*iqr,  high whisker = q3+1.5*iqr (iq5 = q3-q1)
            'min-max': low whisker = min,         high whisker = max
        config : dict
            dict of nvd3 options 
            (use as keywork argument in the form config=myconfig)

        Returns
        -------
            None
            
        """

        dataConfig = self.chart(data, keys=keys, boxStyle=boxStyle, config=config)
        self._plot(dataConfig)


    def convert(self, data, keys=None, boxStyle="iqr"):
        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        
        self.df.append(df)
        self.keys.append(keys)
        self.boxStyle.append(boxStyle)

        if keys is not None:
            df = df[keys]

        q1 = df.quantile(0.25)
        q2 = df.quantile(0.5)
        q3 = df.quantile(0.75)

        if boxStyle == "iqr":          # iqr
            iqr = q3 - q1
            low = q1 - 1.5 * iqr
            high = q3 + 1.5 * iqr
        else:                          # "min-max"
            low  = df.min()
            high = df.max()
            
        nvd3Data =  [{"key":df.columns[i],
                      "values":{"whisker_low":low[i], "Q1":q1[i], "Q2":q2[i], "Q3": q3[i], "whisker_high":high[i]}}
                     for i in range(len(df.columns))] 
         
        # Add outliers
        if boxStyle == "iqr":
            for i in range(len(df.columns)):
                values = df.iloc[:,i]
                nvd3Data[i]["values"]["outliers"] = list(values[(values < q1[i]-1.5*iqr[i]) | (values > q3[i]+1.5*iqr[i])])

        return {"data": nvd3Data}
    

    def append(self, data, chart=0):
         df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
         self.df[chart] = pd.concat([self.df[chart], df])

         dataConfig = self.chart(self.df[chart], keys=self.keys[chart], boxStyle=self.boxStyle[chart], config=self.config[chart], chart=chart) 
        
         self._replace(dataConfig, chart=chart)

