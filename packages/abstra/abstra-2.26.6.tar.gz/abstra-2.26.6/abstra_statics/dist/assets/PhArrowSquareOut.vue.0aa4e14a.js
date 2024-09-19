import{d as H,B as n,f as i,o as t,X as l,Z as m,R as v,eb as f,a as r}from"./vue-router.daa9090b.js";(function(){try{var o=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(o._sentryDebugIds=o._sentryDebugIds||{},o._sentryDebugIds[e]="16910ee6-6c5e-4c86-a040-8dd09cfd0534",o._sentryDebugIdIdentifier="sentry-dbid-16910ee6-6c5e-4c86-a040-8dd09cfd0534")}catch{}})();const y=["width","height","fill","transform"],w={key:0},A=r("path",{d:"M228,104a12,12,0,0,1-24,0V69l-59.51,59.51a12,12,0,0,1-17-17L187,52H152a12,12,0,0,1,0-24h64a12,12,0,0,1,12,12Zm-44,24a12,12,0,0,0-12,12v64H52V84h64a12,12,0,0,0,0-24H48A20,20,0,0,0,28,80V208a20,20,0,0,0,20,20H176a20,20,0,0,0,20-20V140A12,12,0,0,0,184,128Z"},null,-1),Z=[A],b={key:1},k=r("path",{d:"M184,80V208a8,8,0,0,1-8,8H48a8,8,0,0,1-8-8V80a8,8,0,0,1,8-8H176A8,8,0,0,1,184,80Z",opacity:"0.2"},null,-1),L=r("path",{d:"M224,104a8,8,0,0,1-16,0V59.32l-66.33,66.34a8,8,0,0,1-11.32-11.32L196.68,48H152a8,8,0,0,1,0-16h64a8,8,0,0,1,8,8Zm-40,24a8,8,0,0,0-8,8v72H48V80h72a8,8,0,0,0,0-16H48A16,16,0,0,0,32,80V208a16,16,0,0,0,16,16H176a16,16,0,0,0,16-16V136A8,8,0,0,0,184,128Z"},null,-1),M=[k,L],B={key:2},S=r("path",{d:"M192,136v72a16,16,0,0,1-16,16H48a16,16,0,0,1-16-16V80A16,16,0,0,1,48,64h72a8,8,0,0,1,0,16H48V208H176V136a8,8,0,0,1,16,0Zm32-96a8,8,0,0,0-8-8H152a8,8,0,0,0-5.66,13.66L172.69,72l-42.35,42.34a8,8,0,0,0,11.32,11.32L184,83.31l26.34,26.35A8,8,0,0,0,224,104Z"},null,-1),I=[S],_={key:3},x=r("path",{d:"M222,104a6,6,0,0,1-12,0V54.49l-69.75,69.75a6,6,0,0,1-8.48-8.48L201.51,46H152a6,6,0,0,1,0-12h64a6,6,0,0,1,6,6Zm-38,26a6,6,0,0,0-6,6v72a2,2,0,0,1-2,2H48a2,2,0,0,1-2-2V80a2,2,0,0,1,2-2h72a6,6,0,0,0,0-12H48A14,14,0,0,0,34,80V208a14,14,0,0,0,14,14H176a14,14,0,0,0,14-14V136A6,6,0,0,0,184,130Z"},null,-1),z=[x],C={key:4},D=r("path",{d:"M224,104a8,8,0,0,1-16,0V59.32l-66.33,66.34a8,8,0,0,1-11.32-11.32L196.68,48H152a8,8,0,0,1,0-16h64a8,8,0,0,1,8,8Zm-40,24a8,8,0,0,0-8,8v72H48V80h72a8,8,0,0,0,0-16H48A16,16,0,0,0,32,80V208a16,16,0,0,0,16,16H176a16,16,0,0,0,16-16V136A8,8,0,0,0,184,128Z"},null,-1),N=[D],E={key:5},P=r("path",{d:"M220,104a4,4,0,0,1-8,0V49.66l-73.16,73.17a4,4,0,0,1-5.66-5.66L206.34,44H152a4,4,0,0,1,0-8h64a4,4,0,0,1,4,4Zm-36,28a4,4,0,0,0-4,4v72a4,4,0,0,1-4,4H48a4,4,0,0,1-4-4V80a4,4,0,0,1,4-4h72a4,4,0,0,0,0-8H48A12,12,0,0,0,36,80V208a12,12,0,0,0,12,12H176a12,12,0,0,0,12-12V136A4,4,0,0,0,184,132Z"},null,-1),$=[P],j={name:"PhArrowSquareOut"},F=H({...j,props:{weight:{type:String},size:{type:[String,Number]},color:{type:String},mirrored:{type:Boolean}},setup(o){const e=o,s=n("weight","regular"),h=n("size","1em"),V=n("color","currentColor"),c=n("mirrored",!1),d=i(()=>{var a;return(a=e.weight)!=null?a:s}),u=i(()=>{var a;return(a=e.size)!=null?a:h}),g=i(()=>{var a;return(a=e.color)!=null?a:V}),p=i(()=>e.mirrored!==void 0?e.mirrored?"scale(-1, 1)":void 0:c?"scale(-1, 1)":void 0);return(a,q)=>(t(),l("svg",f({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 256 256",width:u.value,height:u.value,fill:g.value,transform:p.value},a.$attrs),[m(a.$slots,"default"),d.value==="bold"?(t(),l("g",w,Z)):d.value==="duotone"?(t(),l("g",b,M)):d.value==="fill"?(t(),l("g",B,I)):d.value==="light"?(t(),l("g",_,z)):d.value==="regular"?(t(),l("g",C,N)):d.value==="thin"?(t(),l("g",E,$)):v("",!0)],16,y))}});export{F};
//# sourceMappingURL=PhArrowSquareOut.vue.0aa4e14a.js.map
