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


class ParallelCoordinatesChart(Nvd3Chart):

    funcName = "parallelCoordinatesChart"
    funcBody = """
        function(session, object) {
            for(var i in object.data.dim) {
                object.data.dim[i].format = d3.format(object.data.dim[i].format)
            }

            var chart = nv.models.parallelCoordinatesChart()
                    .dimensionData(object.data.dim)
                    .displayBrush(true)
                    .lineTension(0.85);

            session.__functions.makeChart(session, object, chart);
        }
    """
    
    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)
        self.key = []
        self.values = []
        self.dimAttributes = []
        self.lineAttributes = []

    
    def plot(self, data, key, values, dimAttributes, lineAttributes={}, config={}):
        """
        Create a ParallelCoordinatesChart

        Example:
            >>> iris.loc[iris.Name=="Iris-setosa",     "color"] = nv.c10()[0]
            >>> iris.loc[iris.Name=="Iris-versicolor", "color"] = nv.c10()[1]
            >>> iris.loc[iris.Name=="Iris-virginica",  "color"] = nv.c10()[2]
            >>> iris["strokeWidth"] = 0.5
            >>> iris.head()
 
                    SepalLength  SepalWidth  PetalLength  PetalWidth         Name    color  strokeWidth
                0          5.1         3.5          1.4         0.2  Iris-setosa  #1f77b4          0.5           

            >>> pc = nv.parallelCoordinatesChart()

            >>> config = {"height": 600}
            
            >>> pc.plot(iris, 'Name', ['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'],
                        lineAttributes=["color", "strokeWidth"], 
                        dimAttributes= {"format": [",.1f", ",.1f", ",.1f", ",.1f"]}
                        config=config)
            
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
        key : string
            Column name or dict key for values to be used to name the lines
        values : list of strings
            Column names or dict keys for values to be used as dimensions (vertical lines)
        lineAttributes : list of strings
            Column names or dict keys for values to be used as "color" and "strokeWidth" attributes for lines
        dimAttributes: dict
            Dict with a list for the format of each dimension
        config : dict
            dict of nvd3 options 
            (use as keywork argument in the form config=myconfig)

        Returns
        -------
            None
        """
 
        dataConfig = self.chart(data, key=key, values=values, dimAttributes=dimAttributes, lineAttributes=lineAttributes, config=config)    
        self._plot(dataConfig)

       
    def convert(self, data, key, values, dimAttributes, lineAttributes={}):
        self.key.append(key)
        self.values.append(values)
        self.dimAttributes.append(dimAttributes)
        self.lineAttributes.append(lineAttributes)

        df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
         
        values2 = df.loc[:, values].to_dict("records")
        nvd3Data = df[[key] + lineAttributes].rename(str, {key:"name"}).to_dict("records")

        for v, n in zip (values2, nvd3Data):
            n["values"] = v
                
        attributes = {"key":values}
        attributes.update(dimAttributes)
        dim = pd.DataFrame(attributes).to_dict("records")

        return {"data": nvd3Data, "dim":dim}

