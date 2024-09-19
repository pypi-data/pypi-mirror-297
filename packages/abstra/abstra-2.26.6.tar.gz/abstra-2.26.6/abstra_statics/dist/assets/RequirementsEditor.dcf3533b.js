var N=Object.defineProperty;var V=(i,e,t)=>e in i?N(i,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):i[e]=t;var w=(i,e,t)=>(V(i,typeof e!="symbol"?e+"":e,t),t);import{C as D}from"./ContentLayout.124197f3.js";import{C as F}from"./CrudView.187e7b93.js";import{a as I}from"./asyncComputed.a9aefa60.js";import{d as R,W as S,ag as A,f as B,c as b,w as c,o as m,b as g,u as n,bP as k,aF as p,d9 as $,R as h,d7 as O,X as f,aR as L,ee as W,ec as v,er as J}from"./vue-router.daa9090b.js";import{u as U}from"./polling.1a044af4.js";import"./editor.40dccf2b.js";import{E as G}from"./record.7a59ec24.js";import{W as M}from"./workspaces.429f2733.js";import"./router.2e40d4d3.js";import"./gateway.143b9d5b.js";import"./popupNotifcation.6bc3253c.js";import"./DocsButton.vue_vue_type_script_setup_true_lang.ef44101d.js";import"./BookOutlined.37a8944e.js";import"./url.f89b68d7.js";import"./PhDotsThreeVertical.vue.00f8a21a.js";import"./index.91d5283b.js";import"./workspaceStore.74650beb.js";import"./colorHelpers.cbe2471c.js";(function(){try{var i=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(i._sentryDebugIds=i._sentryDebugIds||{},i._sentryDebugIds[e]="f4b9cc76-0de1-4d35-9c2d-89850a3930cb",i._sentryDebugIdIdentifier="sentry-dbid-f4b9cc76-0de1-4d35-9c2d-89850a3930cb")}catch{}})();class X{async list(){return(await fetch("/_editor/api/requirements")).json()}async recommendations(){return(await fetch("/_editor/api/requirements/recommendations")).json()}async update(e,t){if(!(await fetch(`/_editor/api/requirements/${e}`,{method:"PUT",headers:{"Content-Type":"application/json"},body:JSON.stringify(t)})).ok)throw new Error("Failed to update requirements")}async create(e){const t=await fetch("/_editor/api/requirements",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)});if(!t.ok)throw new Error("Failed to create requirements");return t.json()}async delete(e){if(!(await fetch(`/_editor/api/requirements/${e}`,{method:"DELETE"})).ok)throw new Error("Failed to delete requirements")}}const u=new X;class l{constructor(e){w(this,"record");this.record=G.from(e)}static async list(){return(await u.list()).map(t=>new l(t))}static async create(e,t){const o=await u.create({name:e,version:t||null});return new l(o)}get name(){return this.record.get("name")}set name(e){this.record.set("name",e)}get version(){var e;return(e=this.record.get("version"))!=null?e:"latest"}set version(e){this.record.set("version",e)}async delete(){await u.delete(this.name)}static async recommendations(){return u.recommendations()}}const H=i=>["__future__","__main__","_thread","abc","aifc","argparse","array","ast","asynchat","asyncio","asyncore","atexit","audioop","base64","bdb","binascii","binhex","bisect","builtins","bz2","calendar","cgi","cgitb","chunk","cmath","cmd","code","codecs","codeop","collections","collections.abc","colorsys","compileall","concurrent","concurrent.futures","configparser","contextlib","contextvars","copy","copyreg","cProfile","crypt","csv","ctypes","curses","curses.ascii","curses.panel","curses.textpad","dataclasses","datetime","dbm","dbm.dumb","dbm.gnu","dbm.ndbm","decimal","difflib","dis","distutils","distutils.archive_util","distutils.bcppcompiler","distutils.ccompiler","distutils.cmd","distutils.command","distutils.command.bdist","distutils.command.bdist_dumb","distutils.command.bdist_msi","distutils.command.bdist_packager","distutils.command.bdist_rpm","distutils.command.build","distutils.command.build_clib","distutils.command.build_ext","distutils.command.build_py","distutils.command.build_scripts","distutils.command.check","distutils.command.clean","distutils.command.config","distutils.command.install","distutils.command.install_data","distutils.command.install_headers","distutils.command.install_lib","distutils.command.install_scripts","distutils.command.register","distutils.command.sdist","distutils.core","distutils.cygwinccompiler","distutils.debug","distutils.dep_util","distutils.dir_util","distutils.dist","distutils.errors","distutils.extension","distutils.fancy_getopt","distutils.file_util","distutils.filelist","distutils.log","distutils.msvccompiler","distutils.spawn","distutils.sysconfig","distutils.text_file","distutils.unixccompiler","distutils.util","distutils.version","doctest","email","email.charset","email.contentmanager","email.encoders","email.errors","email.generator","email.header","email.headerregistry","email.iterators","email.message","email.mime","email.parser","email.policy","email.utils","encodings","encodings.idna","encodings.mbcs","encodings.utf_8_sig","ensurepip","enum","errno","faulthandler","fcntl","filecmp","fileinput","fnmatch","fractions","ftplib","functools","gc","getopt","getpass","gettext","glob","graphlib","grp","gzip","hashlib","heapq","hmac","html","html.entities","html.parser","http","http.client","http.cookiejar","http.cookies","http.server","idlelib","imaplib","imghdr","imp","importlib","importlib.abc","importlib.machinery","importlib.metadata","importlib.resources","importlib.util","inspect","io","ipaddress","itertools","json","json.tool","keyword","lib2to3","linecache","locale","logging","logging.config","logging.handlers","lzma","mailbox","mailcap","marshal","math","mimetypes","mmap","modulefinder","msilib","msvcrt","multiprocessing","multiprocessing.connection","multiprocessing.dummy","multiprocessing.managers","multiprocessing.pool","multiprocessing.shared_memory","multiprocessing.sharedctypes","netrc","nis","nntplib","numbers","operator","optparse","os","os.path","ossaudiodev","pathlib","pdb","pickle","pickletools","pipes","pkgutil","platform","plistlib","poplib","posix","pprint","profile","pstats","pty","pwd","py_compile","pyclbr","pydoc","queue","quopri","random","re","readline","reprlib","resource","rlcompleter","runpy","sched","secrets","select","selectors","shelve","shlex","shutil","signal","site","smtpd","smtplib","sndhdr","socket","socketserver","spwd","sqlite3","ssl","stat","statistics","string","stringprep","struct","subprocess","sunau","symtable","sys","sysconfig","syslog","tabnanny","tarfile","telnetlib","tempfile","termios","test","test.support","test.support.bytecode_helper","test.support.import_helper","test.support.os_helper","test.support.script_helper","test.support.socket_helper","test.support.threading_helper","test.support.warnings_helper","textwrap","threading","time","timeit","tkinter","tkinter.colorchooser","tkinter.commondialog","tkinter.dnd","tkinter.filedialog","tkinter.font","tkinter.messagebox","tkinter.scrolledtext","tkinter.simpledialog","tkinter.tix","tkinter.ttk","token","tokenize","trace","traceback","tracemalloc","tty","turtle","turtledemo","types","typing","unicodedata","unittest","unittest.mock","urllib","urllib.error","urllib.parse","urllib.request","urllib.response","urllib.robotparser","uu","uuid","venv","warnings","wave","weakref","webbrowser","winreg","winsound","wsgiref","wsgiref.handlers","wsgiref.headers","wsgiref.simple_server","wsgiref.util","wsgiref.validate","xdrlib","xml","xml.dom","xml.dom.minidom","xml.dom.pulldom","xml.etree.ElementTree","xml.parsers.expat","xml.parsers.expat.errors","xml.parsers.expat.model","xml.sax","xml.sax.handler","xml.sax.saxutils","xml.sax.xmlreader","xmlrpc","xmlrpc.client","xmlrpc.server","zipapp","zipfile","zipimport","zlib","zoneinfo"].includes(i),K=i=>/^(\d+!)?(\d+)(\.\d+)+([\\.\-\\_])?((a(lpha)?|b(eta)?|c|r(c|ev)?|pre(view)?)\d*)?(\.?(post|dev)\d*)?$/.test(i),Q={key:2},ye=R({__name:"RequirementsEditor",setup(i){const{loading:e,result:t,refetch:o}=I(()=>Promise.all([l.list(),l.recommendations()]).then(([s,r])=>({requirements:s,recommendations:r}))),{startPolling:q,endPolling:C}=U({task:o,interval:2e3});S(()=>q()),A(()=>C());function E(){M.openFile("requirements.txt")}async function T(s,r){await l.create(s,r).then(o),o()}const z=[{label:"Name",key:"name",hint:s=>H(s)?"This requirement is built-in should not be installed":void 0},{label:"Version",key:"version",placeholder:"latest",hint:s=>!s||K(s)?void 0:"Invalid version"}];async function P({name:s,version:r}){await l.create(s,r),o()}const j=B(()=>{var s,r;return{columns:[{name:"Name"},{name:"Version"},{name:"",align:"right"}],rows:(r=(s=t.value)==null?void 0:s.requirements.map(a=>({key:a.name,cells:[{type:"text",text:a.name},{type:"text",text:a.version},{type:"actions",actions:[{icon:J,label:"Delete",async onClick(){await a.delete(),o()},dangerous:!0}]}]})))!=null?r:[]}});return(s,r)=>(m(),b(D,null,{default:c(()=>{var a,y,_;return[g(F,{"entity-name":"Requirements",loading:n(e),title:"Requirements",description:"Specify pip requirements for your project. This will create and update your requirements.txt file.","empty-title":"No python requirements set",table:j.value,"create-button-text":"Add requirement",fields:z,live:"",create:P},{secondary:c(()=>[g(n(k),{onClick:r[0]||(r[0]=d=>E())},{default:c(()=>[p("Open requirements.txt")]),_:1})]),_:1},8,["loading","table"]),(a=n(t))!=null&&a.recommendations.length?(m(),b(n($),{key:0},{default:c(()=>[p(" Suggested requirements ")]),_:1})):h("",!0),(y=n(t))!=null&&y.recommendations.length?(m(),b(n(O),{key:1},{default:c(()=>[p(" The following requirements are being utilized by your code but are not listed in your requirements.txt. ")]),_:1})):h("",!0),(_=n(t))!=null&&_.recommendations.length?(m(),f("ul",Q,[(m(!0),f(L,null,W(n(t).recommendations,d=>(m(),f("li",{key:d.name},[p(v(d.name)+" ("+v(d.version)+") ",1),g(n(k),{onClick:Y=>{var x;return T(d.name,(x=d.version)!=null?x:void 0)}},{default:c(()=>[p(" Add to requirements ")]),_:2},1032,["onClick"])]))),128))])):h("",!0)]}),_:1}))}});export{ye as default};
//# sourceMappingURL=RequirementsEditor.dcf3533b.js.map
