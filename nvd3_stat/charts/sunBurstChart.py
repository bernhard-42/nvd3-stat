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


class SunBurstChart(Nvd3Chart):

    funcName = "sunBurstChart"
    funcBody = """
        function(session, object) {
            var chart = nv.models.sunburstChart()
                      .mode("count")

            session.makeChart(session, object, chart);
        }        
    """
    
    def __init__(self, nvd3Functions):
        super(self.__class__, self).__init__(nvd3Functions)

    def plot(self, data):
        """
        Directly use data in the form:
            
            data = [{
                "name": "flare",
                "children": [
                    {
                        "name": "analytics",
                        "children": [
                            {
                                "name": "cluster",
                                "children": [
                                    {"name": "AgglomerativeCluster", "size": 3938},
                                    {"name": "CommunityStructure", "size": 3812},
                                    {"name": "HierarchicalCluster", "size": 6714},
                                    {"name": "MergeEdge", "size": 743}
                                ]
                            }, ....
        """
        self._plot(data)