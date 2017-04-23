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

from IPython.display import Javascript, display_javascript, HTML, display_html
from ipykernel.comm import Comm
import json
import time
import os.path


class IPythonSession(object):

    def __init__(self):
        self.comm = None

        folder = os.path.dirname(__file__)
        with open(os.path.join(folder, "../js", "initIPython.js"), "r") as fd:
            initIPython = fd.read()

        display_javascript(Javascript(initIPython))

        css = """
            <style>
                div.output_area img, div.output_area svg {
                    max-width: 100%;
                    height: 100%;
                }
            </style>
        """
        display_html(HTML(css))
            
        time.sleep(0.5)
        self.comm = Comm(target_name='nvd3_stat', data={'event': 'open'})


    def registerFunction(self, funcName, funcBody):
        # Zeppelin only
        pass


    def call(self, funcName, args, delay):
        # Explicitely open comm channel in case notebook has been reloaded
        self.comm.open()
        self.comm.send({"funcName":funcName, "args":args, "delay": delay})


def loadNVD3(nvd3version="1.8.2", d3version="3.5.17"):

    folder = os.path.dirname(__file__)
    with open(os.path.join(folder, "../js", "loadLibraries.js"), "r") as fd:
        loadLibraries = fd.read()

    js = """
        (function() {
            var loadLibraries = %s
            loadLibraries("%s", "%s", function(msg) { element.append("<div>" + msg + "</div>"); },
                                      function(msg) { element.append("<div style='color:red'>Error: " + msg + "</div>"); })
        })();
    """ %(loadLibraries, d3version, nvd3version)

    display_javascript(Javascript(js))
