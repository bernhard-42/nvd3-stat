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


from .nvd3_functions import Nvd3Functions
from .nvd3_chart import Nvd3Chart

from .charts.boxPlotChart             import BoxPlotChart
from .charts.discreteBarChart         import DiscreteBarChart
from .charts.multiBarChart            import MultiBarChart
from .charts.multiBarHorizontalChart  import MultiBarHorizontalChart
from .charts.lineChart                import LineChart
from .charts.linePlusBarChart         import LinePlusBarChart
from .charts.scatterPlusLineChart     import ScatterPlusLineChart
from .charts.stackedAreaChart         import StackedAreaChart
from .charts.pieChart                 import PieChart
from .charts.sunBurstChart            import SunBurstChart
from .charts.parallelCoordinatesChart import ParallelCoordinatesChart
from .charts.historicalBarChart       import HistoricalBarChart
from .charts.candlestickBarChart      import CandlestickBarChart
from .charts.ohlcBarChart             import OhlcBarChart


class Nvd3(object):
    
    def __init__(self, downloadAsPng=True):
        self.nvd3Functions = Nvd3Functions()
        self.registeredCharts = {}

        css = """
        <style>
        div.output_area img, div.output_area svg {
            max-width: 100%;
            height: 100%;
        }
        </style>
        """
        self.nvd3Functions.display_html(css)
        

    def reloadNVD3(self, nvd3version="1.8.5", d3version="3.5.17"):
        self.nvd3Functions.reloadNVD3(nvd3version, d3version)
        
    def register(self, funcName, funcBody, force=False):
        if not self.registeredCharts.get(funcName) or force:
            self.nvd3Functions.register(funcName, funcBody)
            self.registeredCharts[funcName] = True


    def boxPlotChart(self):
        self.register(BoxPlotChart.funcName, BoxPlotChart.funcBody)
        return BoxPlotChart(self.nvd3Functions)

    def discreteBarChart(self):
        self.register(DiscreteBarChart.funcName, DiscreteBarChart.funcBody)
        return DiscreteBarChart(self.nvd3Functions)

    def multiBarChart(self):
        self.register(MultiBarChart.funcName, MultiBarChart.funcBody)
        return MultiBarChart(self.nvd3Functions)

    def multiBarHorizontalChart(self):
        self.register(MultiBarHorizontalChart.funcName, MultiBarHorizontalChart.funcBody)
        return MultiBarHorizontalChart(self.nvd3Functions)

    def lineChart(self):
        self.register(LineChart.funcName, LineChart.funcBody)
        return LineChart(self.nvd3Functions)

    def linePlusBarChart(self):
        self.register(LinePlusBarChart.funcName, LinePlusBarChart.funcBody)
        return LinePlusBarChart(self.nvd3Functions)

    def scatterPlusLineChart(self):
        self.register(ScatterPlusLineChart.funcName, ScatterPlusLineChart.funcBody)
        return ScatterPlusLineChart(self.nvd3Functions)

    def stackedAreaChart(self):
        self.register(StackedAreaChart.funcName, StackedAreaChart.funcBody)
        return StackedAreaChart(self.nvd3Functions)

    def pieChart(self):
        self.register(PieChart.funcName, PieChart.funcBody)
        return PieChart(self.nvd3Functions)

    def sunBurstChart(self):
        self.register(SunBurstChart.funcName, SunBurstChart.funcBody)
        return SunBurstChart(self.nvd3Functions)

    def parallelCoordinatesChart(self):
        self.register(ParallelCoordinatesChart.funcName, ParallelCoordinatesChart.funcBody)
        return ParallelCoordinatesChart(self.nvd3Functions)

    def ohlcBarChart(self):
        self.register(OhlcBarChart.funcName, OhlcBarChart.funcBody)
        return OhlcBarChart(self.nvd3Functions)

    def candlestickBarChart(self):
        self.register(CandlestickBarChart.funcName, CandlestickBarChart.funcBody)
        return CandlestickBarChart(self.nvd3Functions)

    def historicalBarChart(self):
        self.register(HistoricalBarChart.funcName, HistoricalBarChart.funcBody)
        return HistoricalBarChart(self.nvd3Functions)


    # Source: http://d3js.org
    def c10(self):
        return ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]

    # Source: http://d3js.org
    def c20(self):
        return ["#1f77b4", "#aec7e8", "#ff7f0e", "#ffbb78", "#2ca02c", "#98df8a", "#d62728", "#ff9896", "#9467bd", "#c5b0d5", 
                "#8c564b", "#c49c94", "#e377c2", "#f7b6d2", "#7f7f7f", "#c7c7c7", "#bcbd22", "#dbdb8d", "#17becf", "#9edae5"]

    # Source: http://d3js.org
    def c20b(self):
        return ["#393b79", "#5254a3", "#6b6ecf", "#9c9ede", "#637939", "#8ca252", "#b5cf6b", "#cedb9c", "#8c6d31", "#bd9e39", 
                "#e7ba52", "#e7cb94", "#843c39", "#ad494a", "#d6616b", "#e7969c", "#7b4173", "#a55194", "#ce6dbd", "#de9ed6"]

    # Source: http://d3js.org
    def c20c(self):
        return ["#3182bd", "#6baed6", "#9ecae1", "#c6dbef", "#e6550d", "#fd8d3c", "#fdae6b", "#fdd0a2", "#31a354", "#74c476", 
                "#a1d99b", "#c7e9c0", "#756bb1", "#9e9ac8", "#bcbddc", "#dadaeb", "#636363", "#969696", "#bdbdbd", "#d9d9d9"]

    def grey(self):
        digits = ["0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"]
        return ["#%s" % (d*3) for d in digits]
