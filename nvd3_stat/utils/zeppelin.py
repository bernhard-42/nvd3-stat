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

import time
import os.path

def HTML(text):
    return "%%html\n%s" % text

def Javascript(script):
    return "%%html\n<script>%s</script>" % script

def display_html(html):
    print(html)

def display_javascript(js):
    print(js)

def loadNVD3(nvd3version="1.8.5", d3version="3.5.17"):
    display_html(HTML("""<div id="nvd3_loadStatus"><div>"""))
    time.sleep(0.2)
    
    folder = os.path.dirname(__file__)
    with open(os.path.join(folder, "../js", "loadLibraries.js"), "r") as fd:
        loadLibraries = fd.read()

    js = """
        (function() {
            var loadLibraries = %s
            var element = document.getElementById("nvd3_loadStatus");
            loadLibraries("%s", "%s", function(msg) { element.innerHTML += ("<div>" + msg + "</div>"); },
                                      function(msg) { element.innerHTML += ("<div style='color:red'>Error: " + msg + "</div>"); })
        })();
    """ %(loadLibraries, d3version, nvd3version)

    display_javascript(Javascript(js))
