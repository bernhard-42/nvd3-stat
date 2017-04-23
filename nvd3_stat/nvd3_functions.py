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

import os.path
import time
from IPython import get_ipython

if get_ipython() is None:
    from zeppelin_session import ZeppelinSession as Session
    from .utils.zeppelin import  Javascript, display_javascript, HTML, display_html, loadNVD3
    isZeppelin = True
else:
    from IPython.display import Javascript, display_javascript, HTML, display_html
    from .utils.ipython import IPythonSession as Session, loadNVD3
    isZeppelin = False


class Nvd3Functions(object):

    def __init__(self):
        self.session = Session()

        folder = os.path.dirname(__file__)
        with open(os.path.join(folder, "js", "makeChart.js"), "r") as fd:
            makeChart = fd.read()

        js = """
        window.nvd3_stat = { 
            session: {
                charts: {}
            } 
        };
        window.nvd3_stat.session.makeChart = %s

        if(typeof(window.__nvd3_stat_debug) == "undefined") {
            window.__nvd3_stat_debug = 2;  // no debug output
        }
        console.info("nvd3_stat is initialized");
        """ % makeChart
        display_javascript(Javascript(js))

        time.sleep(0.5)
        self.register("makeChart", "window.nvd3_stat.session.makeChart")


    def register(self, funcName, funcBody):
        self.session.registerFunction(funcName, funcBody) 

 
    def call(self, event, data, divId, delay=200):
        self.session.call("makeChart", {"event":event, "data": data, "plotId":"%s" % divId}, delay)


    def reloadNVD3(self, nvd3version="1.8.5", d3version="3.5.17"):
        loadNVD3(nvd3version, d3version)

    def traceJs(self, on=True):
        if on:
            display_javascript(Javascript("__nvd3_stat_debug=2"))
        else:
            display_javascript(Javascript("__nvd3_stat_debug=0"))

    def display(self, html=None, js=None):
        if js is not None:
            display_javascript(Javascript(js))
        if html is not None:
            display_html(HTML(html))
