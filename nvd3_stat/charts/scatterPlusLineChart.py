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


class ScatterPlusLineChart(Nvd3Chart):

    funcName = "scatterPlusLineChart"
    funcBody = """
        function(session, object) {

            var chart = nv.models.scatterChart()
                          .showDistX(true)
                          .showDistY(true)

            chart.xAxis.showMaxMin(false)
                       .tickFormat(d3.format('.1f'));
                       
            chart.yAxis.showMaxMin(false)
                       .tickFormat(d3.format('.1f'));
          
            chart.scatter.onlyCircles = false;

            session.makeChart(session, object, chart);
        }        
    """
    
    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.keys = []
        self.values = []
        self.lines = []
        self.pointAttributes = []
        self.nvd3Data = []


    def plot(self, data=None, keys=None, values=None, lines=None, pointAttributes={}, config={}):
        """
        Create a ScatterPlusLineChart

        Example:
            >>> data0.head(2)  
                   Shape1       Shape3     Size1     Size3        X1        X2         Y1         Y2
                0   cross  triangle-up  0.227967  1.503784  2.657808  2.488658  21.163933  15.300586
                1  circle        cross  0.673804  1.305641  2.461894  1.852206  18.582600  21.406439
            
            >>> data1.head(2)
                   Shape1     Size1        X1         Y1
                0   cross  0.227967  2.124565  28.654155
                1  circle  0.673804  1.182773  26.394414
            
            >>> data3.head(2)
                          Shape2     Size2        X2         Y2
                0  triangle-down  2.049830  1.940713  27.293514
                1         square  2.015426  2.694447  25.333132
            
            
            >>> config = {"height":700, "color":nv.c10()}

            Option 1:
            >>> spl.plot(data=data0, keys=["X1", "X2"], values=["Y1", "Y2"], 
                         lines=[{"slope":1.5, "intercept":20}, {"slope":1.2, "intercept":12}],
                         pointAttributes={"shapes":["Shape1", "Shape3"],  "sizes":["Size1", "Size3"]},
                         config=config)
            
            Option 2:
            >>> spl.plot(data=data0, keys="X1", values="Y1", 
                         lines={"slope":1.5, "intercept":20}, 
                         pointAttributes={"shapes":"Shape1", "sizes":"Size1"},
                         config=config)

            Option 3:
            >>> spl.addScatter(data1, "X1", "Y1", lines={"slope":1.5, "intercept":20}, 
                                                  pointAttributes={"shapes":"Shape1",  "sizes":"Size1"})
            >>> spl.addScatter(data1, "X2", "Y2", lines={"slope":1.2, "intercept":18}, 
                                                  pointAttributes={"shapes":"Shape2", "sizes":"Size2"})
            >>> sqpl.plot(config=config)           
            
        Parameters
        ----------
        data : dict of lists / Pandas DataFrame or a list of dict of lists / Pandas DataFrame
            If the parameter is a dict, each keys represent the name of the dataset in the list
              { 'A': ( 1,   2,   3),
                'B': ('C', 'T', 'D' }
            or a pandas DataFrame, each column representing a dataset
                 A  B
              0  1  C
              1  2  T
              2  3  D
        keys : string or list of strings
            Column name(s) or dict key(s) for values to be used for the x axis
        values : string or list of strings
            Column name(s) or dict key(s) for values to be used for the lines
        lines : list of dict 
            One dict per key of the form {"intercept": ..., "slope": ...}
        pointAttributes : dict or dict of lists 
            Format {"shapes": [...], "sizes": [...]} where the list [...] contains
            the column names / dict keys to be used for shape or size of the point
        config : dict
            dict of nvd3 options 
            (use as keywork argument in the form config=myconfig)

        Returns
        -------
            None
        """

        if data is None:
            dataConfig = {"data":self.nvd3Data, "config": config}
            self.data.append(self.nvd3Data) # save the collection of single lines 
        else:
            dataConfig = self.chart(data, keys=keys, values=values, lines=lines, pointAttributes=pointAttributes, config=config)    
        self._plot(dataConfig)


    def addScatter(self, data, key=None, values=None, lines=None, pointAttributes={}):
        convData = self.convert(data, key, values, lines, pointAttributes)
        self.nvd3Data.append(convData["data"][0]) # collect single lines


    def convert(self, data, keys=None, values=None, lines=None, pointAttributes={}):
        self.keys.append(keys)
        self.values.append(values)
        self.lines.append(lines)
        self.pointAttributes.append(pointAttributes)

        nvd3Data = []

        shapes = pointAttributes.get("shapes")
        sizes = pointAttributes.get("sizes")

        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
        if (isinstance(values, (list, tuple))):
            if shapes is None:
                shapes = [None]*len(values)
            if sizes is None:
                sizes = [None]*len(values)
            if lines is None:
                lines = [None]*len(values)
        else:
            keys = [keys]
            values = [values]
            sizes = [sizes]
            shapes = [shapes]
            lines = [lines]

        nvd3Data = []
        for i in range(len(values)):
            columns = [keys[i], values[i]] 
            renameDict = {keys[i]:"x", values[i]:"y"}

            if shapes[i] is not None:
                columns.append(shapes[i])
                renameDict[shapes[i]] = "shape"
            if sizes[i] is not None:
                columns.append(sizes[i])
                renameDict[sizes[i]] = "size"

            points = df.loc[:,columns].rename(str, renameDict)
            points = {"key":values[i], "values":points.to_dict("records")}
            
            if lines[i] is not None:
                points["intercept"] = lines[i]["intercept"]
                points["slope"] = lines[i]["slope"]
                
            nvd3Data.append(points)

        return {"data":nvd3Data}


    def append(self, data, pointAttributes=None, lines=None, chart=0):
        if pointAttributes is not None:
            self.pointAttributes[chart] = pointAttributes
        if lines is not  None:
            self.lines[chart] = lines

        dataConfig = self.chart(data, keys=self.keys[chart], values=self.values[chart], lines=self.lines[chart], 
                                pointAttributes=self.pointAttributes[chart], config=self.config[chart], chart=chart) 
        self._append(dataConfig, chart=chart)

