var H=Object.defineProperty;var U=(n,e,t)=>e in n?H(n,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):n[e]=t;var v=(n,e,t)=>(U(n,typeof e!="symbol"?e+"":e,t),t);function W(n){return n&&n.__esModule&&Object.prototype.hasOwnProperty.call(n,"default")?n.default:n}function _(n){if(typeof n!="string")throw new TypeError("Path must be a string. Received "+JSON.stringify(n))}function k(n,e){for(var t="",a=0,i=-1,l=0,o,s=0;s<=n.length;++s){if(s<n.length)o=n.charCodeAt(s);else{if(o===47)break;o=47}if(o===47){if(!(i===s-1||l===1))if(i!==s-1&&l===2){if(t.length<2||a!==2||t.charCodeAt(t.length-1)!==46||t.charCodeAt(t.length-2)!==46){if(t.length>2){var r=t.lastIndexOf("/");if(r!==t.length-1){r===-1?(t="",a=0):(t=t.slice(0,r),a=t.length-1-t.lastIndexOf("/")),i=s,l=0;continue}}else if(t.length===2||t.length===1){t="",a=0,i=s,l=0;continue}}e&&(t.length>0?t+="/..":t="..",a=2)}else t.length>0?t+="/"+n.slice(i+1,s):t=n.slice(i+1,s),a=s-i-1;i=s,l=0}else o===46&&l!==-1?++l:l=-1}return t}function x(n,e){var t=e.dir||e.root,a=e.base||(e.name||"")+(e.ext||"");return t?t===e.root?t+a:t+n+a:a}var y={resolve:function(){for(var e="",t=!1,a,i=arguments.length-1;i>=-1&&!t;i--){var l;i>=0?l=arguments[i]:(a===void 0&&(a=process.cwd()),l=a),_(l),l.length!==0&&(e=l+"/"+e,t=l.charCodeAt(0)===47)}return e=k(e,!t),t?e.length>0?"/"+e:"/":e.length>0?e:"."},normalize:function(e){if(_(e),e.length===0)return".";var t=e.charCodeAt(0)===47,a=e.charCodeAt(e.length-1)===47;return e=k(e,!t),e.length===0&&!t&&(e="."),e.length>0&&a&&(e+="/"),t?"/"+e:e},isAbsolute:function(e){return _(e),e.length>0&&e.charCodeAt(0)===47},join:function(){if(arguments.length===0)return".";for(var e,t=0;t<arguments.length;++t){var a=arguments[t];_(a),a.length>0&&(e===void 0?e=a:e+="/"+a)}return e===void 0?".":y.normalize(e)},relative:function(e,t){if(_(e),_(t),e===t||(e=y.resolve(e),t=y.resolve(t),e===t))return"";for(var a=1;a<e.length&&e.charCodeAt(a)===47;++a);for(var i=e.length,l=i-a,o=1;o<t.length&&t.charCodeAt(o)===47;++o);for(var s=t.length,r=s-o,h=l<r?l:r,p=-1,d=0;d<=h;++d){if(d===h){if(r>h){if(t.charCodeAt(o+d)===47)return t.slice(o+d+1);if(d===0)return t.slice(o+d)}else l>h&&(e.charCodeAt(a+d)===47?p=d:d===0&&(p=0));break}var c=e.charCodeAt(a+d),f=t.charCodeAt(o+d);if(c!==f)break;c===47&&(p=d)}var m="";for(d=a+p+1;d<=i;++d)(d===i||e.charCodeAt(d)===47)&&(m.length===0?m+="..":m+="/..");return m.length>0?m+t.slice(o+p):(o+=p,t.charCodeAt(o)===47&&++o,t.slice(o))},_makeLong:function(e){return e},dirname:function(e){if(_(e),e.length===0)return".";for(var t=e.charCodeAt(0),a=t===47,i=-1,l=!0,o=e.length-1;o>=1;--o)if(t=e.charCodeAt(o),t===47){if(!l){i=o;break}}else l=!1;return i===-1?a?"/":".":a&&i===1?"//":e.slice(0,i)},basename:function(e,t){if(t!==void 0&&typeof t!="string")throw new TypeError('"ext" argument must be a string');_(e);var a=0,i=-1,l=!0,o;if(t!==void 0&&t.length>0&&t.length<=e.length){if(t.length===e.length&&t===e)return"";var s=t.length-1,r=-1;for(o=e.length-1;o>=0;--o){var h=e.charCodeAt(o);if(h===47){if(!l){a=o+1;break}}else r===-1&&(l=!1,r=o+1),s>=0&&(h===t.charCodeAt(s)?--s===-1&&(i=o):(s=-1,i=r))}return a===i?i=r:i===-1&&(i=e.length),e.slice(a,i)}else{for(o=e.length-1;o>=0;--o)if(e.charCodeAt(o)===47){if(!l){a=o+1;break}}else i===-1&&(l=!1,i=o+1);return i===-1?"":e.slice(a,i)}},extname:function(e){_(e);for(var t=-1,a=0,i=-1,l=!0,o=0,s=e.length-1;s>=0;--s){var r=e.charCodeAt(s);if(r===47){if(!l){a=s+1;break}continue}i===-1&&(l=!1,i=s+1),r===46?t===-1?t=s:o!==1&&(o=1):t!==-1&&(o=-1)}return t===-1||i===-1||o===0||o===1&&t===i-1&&t===a+1?"":e.slice(t,i)},format:function(e){if(e===null||typeof e!="object")throw new TypeError('The "pathObject" argument must be of type Object. Received type '+typeof e);return x("/",e)},parse:function(e){_(e);var t={root:"",dir:"",base:"",ext:"",name:""};if(e.length===0)return t;var a=e.charCodeAt(0),i=a===47,l;i?(t.root="/",l=1):l=0;for(var o=-1,s=0,r=-1,h=!0,p=e.length-1,d=0;p>=l;--p){if(a=e.charCodeAt(p),a===47){if(!h){s=p+1;break}continue}r===-1&&(h=!1,r=p+1),a===46?o===-1?o=p:d!==1&&(d=1):o!==-1&&(d=-1)}return o===-1||r===-1||d===0||d===1&&o===r-1&&o===s+1?r!==-1&&(s===0&&i?t.base=t.name=e.slice(1,r):t.base=t.name=e.slice(s,r)):(s===0&&i?(t.name=e.slice(1,o),t.base=e.slice(1,r)):(t.name=e.slice(s,o),t.base=e.slice(s,r)),t.ext=e.slice(o,r)),s>0?t.dir=e.slice(0,s-1):i&&(t.dir="/"),t},sep:"/",delimiter:":",win32:null,posix:null};y.posix=y;var z=y;const O=W(z),G="/home/pyodide",S=n=>`${G}/${n}`,w=(n,e)=>O.resolve(S(n),e);function L(n,e){const t=O.normalize(e),i=O.dirname(t).split("/"),l=[];for(const o of i){l.push(o);const s=l.join("/");if(n.FS.analyzePath(s).exists){if(n.FS.isDir(s))throw new Error(`"${s}" already exists and is not a directory.`);continue}try{n.FS.mkdir(s)}catch(r){throw console.error(`Failed to create a directory "${s}"`),r}}}function C(n,e,t,a){L(n,e),n.FS.writeFile(e,t,a)}function q(n,e,t){L(n,t),n.FS.rename(e,t)}function Y(n){n.forEach(e=>{let t;try{t=new URL(e)}catch{return}if(t.protocol==="emfs:"||t.protocol==="file:")throw new Error(`"emfs:" and "file:" protocols are not allowed for the requirement (${e})`)})}class B{constructor(){v(this,"_buffer",[]);v(this,"_promise");v(this,"_resolve");this._resolve=null,this._promise=null,this._notifyAll()}async _wait(){await this._promise}_notifyAll(){this._resolve&&this._resolve(),this._promise=new Promise(e=>this._resolve=e)}async dequeue(){for(;this._buffer.length===0;)await this._wait();return this._buffer.shift()}enqueue(e){this._buffer.push(e),this._notifyAll()}}function j(n,e,t){const a=new B;t.addEventListener("message",o=>{a.enqueue(o.data)}),t.start();async function i(){return await a.dequeue()}async function l(o){const s=Object.fromEntries(o.toJs());t.postMessage(s)}return n(e,i,l)}const R="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";function $(n){return Array.from(Array(n)).map(()=>R[Math.floor(Math.random()*R.length)]).join("")}const V=`import ast
import os
import sys
import tokenize
import types
from inspect import CO_COROUTINE

from gradio.wasm_utils import app_id_context

# BSD 3-Clause License
#
# - Copyright (c) 2008-Present, IPython Development Team
# - Copyright (c) 2001-2007, Fernando Perez <fernando.perez@colorado.edu>
# - Copyright (c) 2001, Janko Hauser <jhauser@zscout.de>
# - Copyright (c) 2001, Nathaniel Gray <n8gray@caltech.edu>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Code modified from IPython (BSD license)
# Source: https://github.com/ipython/ipython/blob/master/IPython/utils/syspathcontext.py#L42
class modified_sys_path:  # noqa: N801
    """A context for prepending a directory to sys.path for a second."""

    def __init__(self, script_path: str):
        self._script_path = script_path
        self._added_path = False

    def __enter__(self):
        if self._script_path not in sys.path:
            sys.path.insert(0, self._script_path)
            self._added_path = True

    def __exit__(self, type, value, traceback):
        if self._added_path:
            try:
                sys.path.remove(self._script_path)
            except ValueError:
                # It's already removed.
                pass

        # Returning False causes any exceptions to be re-raised.
        return False


# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
# Copyright (c) Yuichiro Tachibana (2023)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
def _new_module(name: str) -> types.ModuleType:
    """Create a new module with the given name."""
    return types.ModuleType(name)


def set_home_dir(home_dir: str) -> None:
    os.environ["HOME"] = home_dir
    os.chdir(home_dir)


async def _run_script(app_id: str, home_dir: str, script_path: str) -> None:
    # This function is based on the following code from Streamlit:
    # https://github.com/streamlit/streamlit/blob/1.24.0/lib/streamlit/runtime/scriptrunner/script_runner.py#L519-L554
    # with modifications to support top-level await.
    set_home_dir(home_dir)

    with tokenize.open(script_path) as f:
        filebody = f.read()

    await _run_code(app_id, home_dir, filebody, script_path)


async def _run_code(
        app_id: str,
        home_dir: str,
        filebody: str,
        script_path: str = '<string>'  # This default value follows the convention. Ref: https://docs.python.org/3/library/functions.html#compile
    ) -> None:
    set_home_dir(home_dir)

    # NOTE: In Streamlit, the bytecode caching mechanism has been introduced.
    # However, we skipped it here for simplicity and because Gradio doesn't need to rerun the script so frequently,
    # while we may do it in the future.
    bytecode = compile(  # type: ignore
        filebody,
        # Pass in the file path so it can show up in exceptions.
        script_path,
        # We're compiling entire blocks of Python, so we need "exec"
        # mode (as opposed to "eval" or "single").
        mode="exec",
        # Don't inherit any flags or "future" statements.
        flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT, # Allow top-level await. Ref: https://github.com/whitphx/streamlit/commit/277dc580efb315a3e9296c9a0078c602a0904384
        dont_inherit=1,
        # Use the default optimization options.
        optimize=-1,
    )

    module = _new_module("__main__")

    # Install the fake module as the __main__ module. This allows
    # the pickle module to work inside the user's code, since it now
    # can know the module where the pickled objects stem from.
    # IMPORTANT: This means we can't use "if __name__ == '__main__'" in
    # our code, as it will point to the wrong module!!!
    sys.modules["__main__"] = module

    # Add special variables to the module's globals dict.
    module.__dict__["__file__"] = script_path

    with modified_sys_path(script_path), modified_sys_path(home_dir), app_id_context(app_id):
        # Allow top-level await. Ref: https://github.com/whitphx/streamlit/commit/277dc580efb315a3e9296c9a0078c602a0904384
        if bytecode.co_flags & CO_COROUTINE:
            # The source code includes top-level awaits, so the compiled code object is a coroutine.
            await eval(bytecode, module.__dict__)
        else:
            exec(bytecode, module.__dict__)
`,J=`# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
# Copyright (c) Yuichiro Tachibana (2023)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import fnmatch
import logging
import os
import sys
import types
from typing import Optional, Set

LOGGER = logging.getLogger(__name__)

#
# Copied from https://github.com/streamlit/streamlit/blob/1.24.0/lib/streamlit/file_util.py
#

def file_is_in_folder_glob(filepath, folderpath_glob) -> bool:
    """Test whether a file is in some folder with globbing support.

    Parameters
    ----------
    filepath : str
        A file path.
    folderpath_glob: str
        A path to a folder that may include globbing.

    """
    # Make the glob always end with "/*" so we match files inside subfolders of
    # folderpath_glob.
    if not folderpath_glob.endswith("*"):
        if folderpath_glob.endswith("/"):
            folderpath_glob += "*"
        else:
            folderpath_glob += "/*"

    file_dir = os.path.dirname(filepath) + "/"
    return fnmatch.fnmatch(file_dir, folderpath_glob)


def get_directory_size(directory: str) -> int:
    """Return the size of a directory in bytes."""
    total_size = 0
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size


def file_in_pythonpath(filepath) -> bool:
    """Test whether a filepath is in the same folder of a path specified in the PYTHONPATH env variable.


    Parameters
    ----------
    filepath : str
        An absolute file path.

    Returns
    -------
    boolean
        True if contained in PYTHONPATH, False otherwise. False if PYTHONPATH is not defined or empty.

    """
    pythonpath = os.environ.get("PYTHONPATH", "")
    if len(pythonpath) == 0:
        return False

    absolute_paths = [os.path.abspath(path) for path in pythonpath.split(os.pathsep)]
    return any(
        file_is_in_folder_glob(os.path.normpath(filepath), path)
        for path in absolute_paths
    )

#
# Copied from https://github.com/streamlit/streamlit/blob/1.24.0/lib/streamlit/watcher/local_sources_watcher.py
#

def get_module_paths(module: types.ModuleType) -> Set[str]:
    paths_extractors = [
        # https://docs.python.org/3/reference/datamodel.html
        # __file__ is the pathname of the file from which the module was loaded
        # if it was loaded from a file.
        # The __file__ attribute may be missing for certain types of modules
        lambda m: [m.__file__],
        # https://docs.python.org/3/reference/import.html#__spec__
        # The __spec__ attribute is set to the module spec that was used
        # when importing the module. one exception is __main__,
        # where __spec__ is set to None in some cases.
        # https://www.python.org/dev/peps/pep-0451/#id16
        # "origin" in an import context means the system
        # (or resource within a system) from which a module originates
        # ... It is up to the loader to decide on how to interpret
        # and use a module's origin, if at all.
        lambda m: [m.__spec__.origin],
        # https://www.python.org/dev/peps/pep-0420/
        # Handling of "namespace packages" in which the __path__ attribute
        # is a _NamespacePath object with a _path attribute containing
        # the various paths of the package.
        lambda m: list(m.__path__._path),
    ]

    all_paths = set()
    for extract_paths in paths_extractors:
        potential_paths = []
        try:
            potential_paths = extract_paths(module)
        except AttributeError:
            # Some modules might not have __file__ or __spec__ attributes.
            pass
        except Exception as e:
            LOGGER.warning(f"Examining the path of {module.__name__} raised: {e}")

        all_paths.update(
            [os.path.abspath(str(p)) for p in potential_paths if _is_valid_path(p)]
        )
    return all_paths


def _is_valid_path(path: Optional[str]) -> bool:
    return isinstance(path, str) and (os.path.isfile(path) or os.path.isdir(path))


#
# Original code
#

def unload_local_modules(target_dir_path: str = "."):
    """ Unload all modules that are in the target directory or in a subdirectory of it.
    It is necessary to unload modules before re-executing a script that imports the modules,
    so that the new version of the modules is loaded.
    The module unloading feature is extracted from Streamlit's LocalSourcesWatcher (https://github.com/streamlit/streamlit/blob/1.24.0/lib/streamlit/watcher/local_sources_watcher.py)
    and packaged as a standalone function.
    """
    target_dir_path = os.path.abspath(target_dir_path)
    loaded_modules = {} # filepath -> module_name

    # Copied from \`LocalSourcesWatcher.update_watched_modules()\`
    module_paths = {
        name: get_module_paths(module)
        for name, module in dict(sys.modules).items()
    }

    # Copied from \`LocalSourcesWatcher._register_necessary_watchers()\`
    for name, paths in module_paths.items():
        for path in paths:
            if file_is_in_folder_glob(path, target_dir_path) or file_in_pythonpath(path):
                loaded_modules[path] = name

    # Copied from \`LocalSourcesWatcher.on_file_changed()\`
    for module_name in loaded_modules.values():
        if module_name is not None and module_name in sys.modules:
            del sys.modules[module_name]
`;importScripts("https://cdn.jsdelivr.net/pyodide/v0.26.1/full/pyodide.js");let u,A,M,D,F,P;async function K(n,e,t,a){console.debug("Loading Pyodide."),e("Loading Pyodide"),u=await loadPyodide({stdout:t,stderr:a}),console.debug("Pyodide is loaded."),console.debug("Loading micropip"),e("Loading micropip"),await u.loadPackage("micropip"),A=u.pyimport("micropip"),console.debug("micropip is loaded.");const i=[n.gradioWheelUrl,n.gradioClientWheelUrl];console.debug("Loading Gradio wheels.",i),e("Loading Gradio wheels"),await u.loadPackage(["ssl","setuptools"]),await A.add_mock_package("ffmpy","0.3.0"),await A.install.callKwargs(i,{keep_going:!0}),console.debug("Gradio wheels are loaded."),console.debug("Mocking os module methods."),e("Mock os module methods"),await u.runPythonAsync(`
import os

os.link = lambda src, dst: None
`),console.debug("os module methods are mocked."),console.debug("Importing gradio package."),e("Importing gradio package"),await u.runPythonAsync("import gradio"),console.debug("gradio package is imported."),console.debug("Defining a ASGI wrapper function."),e("Defining a ASGI wrapper function"),await u.runPythonAsync(`
# Based on Shiny's App.call_pyodide().
# https://github.com/rstudio/py-shiny/blob/v0.3.3/shiny/_app.py#L224-L258
async def _call_asgi_app_from_js(app_id, scope, receive, send):
	# TODO: Pretty sure there are objects that need to be destroy()'d here?
	scope = scope.to_py()

	# ASGI requires some values to be byte strings, not character strings. Those are
	# not that easy to create in JavaScript, so we let the JS side pass us strings
	# and we convert them to bytes here.
	if "headers" in scope:
			# JS doesn't have \`bytes\` so we pass as strings and convert here
			scope["headers"] = [
					[value.encode("latin-1") for value in header]
					for header in scope["headers"]
			]
	if "query_string" in scope and scope["query_string"]:
			scope["query_string"] = scope["query_string"].encode("latin-1")
	if "raw_path" in scope and scope["raw_path"]:
			scope["raw_path"] = scope["raw_path"].encode("latin-1")

	async def rcv():
			event = await receive()
			py_event = event.to_py()
			if "body" in py_event:
					if isinstance(py_event["body"], memoryview):
							py_event["body"] = py_event["body"].tobytes()
			return py_event

	async def snd(event):
			await send(event)

	app = gradio.wasm_utils.get_registered_app(app_id)
	if app is None:
		raise RuntimeError("Gradio app has not been launched.")

	await app(scope, rcv, snd)
`),M=u.globals.get("_call_asgi_app_from_js"),console.debug("The ASGI wrapper function is defined."),console.debug("Mocking async libraries."),e("Mocking async libraries"),await u.runPythonAsync(`
async def mocked_anyio_to_thread_run_sync(func, *args, cancellable=False, limiter=None):
	return func(*args)

import anyio.to_thread
anyio.to_thread.run_sync = mocked_anyio_to_thread_run_sync
	`),console.debug("Async libraries are mocked."),console.debug("Setting up Python utility functions."),e("Setting up Python utility functions"),await u.runPythonAsync(V),D=u.globals.get("_run_code"),F=u.globals.get("_run_script"),await u.runPythonAsync(J),P=u.globals.get("unload_local_modules"),console.debug("Python utility functions are set up."),e("Initialization completed")}async function Q(n,e,t,a){const i=S(n);console.debug("Creating a home directory for the app.",{appId:n,appHomeDir:i}),u.FS.mkdir(i),console.debug("Mounting files.",e.files),t("Mounting files");const l=[];await Promise.all(Object.keys(e.files).map(async p=>{const d=e.files[p];let c;"url"in d?(console.debug(`Fetch a file from ${d.url}`),c=await fetch(d.url).then(g=>g.arrayBuffer()).then(g=>new Uint8Array(g))):c=d.data;const{opts:f}=e.files[p],m=w(n,p);console.debug(`Write a file "${m}"`),C(u,m,c,f),typeof c=="string"&&p.endsWith(".py")&&l.push(c)})),console.debug("Files are mounted."),console.debug("Installing packages.",e.requirements),t("Installing packages"),await A.install.callKwargs(e.requirements,{keep_going:!0}),console.debug("Packages are installed."),console.debug("Auto-loading modules.");const o=await Promise.all(l.map(p=>u.loadPackagesFromImports(p))),s=new Set(o.flat()),r=Array.from(s);r.length>0&&a(r);const h=r.map(p=>p.name);console.debug("Modules are auto-loaded.",r),(e.requirements.includes("matplotlib")||h.includes("matplotlib"))&&(console.debug("Setting matplotlib backend."),t("Setting matplotlib backend"),await u.runPythonAsync(`
try:
	import matplotlib
	matplotlib.use("agg")
except ImportError:
	pass
`),console.debug("matplotlib backend is set.")),t("App is now loaded")}const E=self;"postMessage"in E?N(E):E.onconnect=n=>{const e=n.ports[0];N(e),e.start()};let b;function N(n){const e=$(8);console.debug("Set up a new app.",{appId:e});const t=r=>{n.postMessage({type:"progress-update",data:{log:r}})},a=r=>{console.log(r),n.postMessage({type:"stdout",data:{output:r}})},i=r=>{console.error(r),n.postMessage({type:"stderr",data:{output:r}})},l=r=>{console.error("Python error:",r),n.postMessage({type:"python-error",data:{traceback:r}})},o=r=>{const h={type:"modules-auto-loaded",data:{packages:r}};n.postMessage(h)};let s;n.onmessage=async function(r){const h=r.data;console.debug("worker.onmessage",h);const p=r.ports[0];try{if(h.type==="init-env"){b==null?b=K(h.data,t,a,i):t("Pyodide environment initialization is ongoing in another session"),b.then(()=>{const c={type:"reply:success",data:null};p.postMessage(c)}).catch(c=>{const f={type:"reply:error",error:c};p.postMessage(f)});return}if(b==null)throw new Error("Pyodide Initialization is not started.");if(await b,u.pyimport("gradio").wasm_utils.register_error_traceback_callback(e,l),h.type==="init-app"){s=Q(e,h.data,t,o);const c={type:"reply:success",data:null};p.postMessage(c);return}if(s==null)throw new Error("App initialization is not started.");switch(await s,h.type){case"echo":{const c={type:"reply:success",data:h.data};p.postMessage(c);break}case"run-python-code":{P(),console.debug("Auto install the requirements");const c=await u.loadPackagesFromImports(h.data.code);c.length>0&&o(c),console.debug("Modules are auto-loaded.",c),await D(e,S(e),h.data.code);const f={type:"reply:success",data:null};p.postMessage(f);break}case"run-python-file":{P(),await F(e,S(e),h.data.path);const c={type:"reply:success",data:null};p.postMessage(c);break}case"asgi-request":{console.debug("ASGI request",h.data),j(M.bind(null,e),h.data.scope,p);break}case"file:write":{const{path:c,data:f,opts:m}=h.data;if(typeof f=="string"&&c.endsWith(".py")){console.debug(`Auto install the requirements in ${c}`);const T=await u.loadPackagesFromImports(f);T.length>0&&o(T),console.debug("Modules are auto-loaded.",T)}const g=w(e,c);console.debug(`Write a file "${g}"`),C(u,g,f,m);const I={type:"reply:success",data:null};p.postMessage(I);break}case"file:rename":{const{oldPath:c,newPath:f}=h.data,m=w(e,c),g=w(e,f);console.debug(`Rename "${m}" to ${g}`),q(u,m,g);const I={type:"reply:success",data:null};p.postMessage(I);break}case"file:unlink":{const{path:c}=h.data,f=w(e,c);console.debug(`Remove "${f}`),u.FS.unlink(f);const m={type:"reply:success",data:null};p.postMessage(m);break}case"install":{const{requirements:c}=h.data,f=u.pyimport("micropip");console.debug("Install the requirements:",c),Y(c),await f.install.callKwargs(c,{keep_going:!0}).then(()=>{if(c.includes("matplotlib"))return u.runPythonAsync(`
try:
	import matplotlib
	matplotlib.use("agg")
except ImportError:
	pass
`)}).then(()=>{console.debug("Successfully installed");const m={type:"reply:success",data:null};p.postMessage(m)});break}}}catch(d){if(console.error(d),!(d instanceof Error))throw d;const c=new Error(d.message);c.name=d.name,c.stack=d.stack;const f={type:"reply:error",error:c};p.postMessage(f)}}}
