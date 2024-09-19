import{d as u,B as h,f as H,o as t,X as r,Z as g,R as f,eb as c,a as l}from"./vue-router.daa9090b.js";(function(){try{var o=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},e=new Error().stack;e&&(o._sentryDebugIds=o._sentryDebugIds||{},o._sentryDebugIds[e]="89f8a882-c902-4455-b382-f1fa470c8a3e",o._sentryDebugIdIdentifier="sentry-dbid-89f8a882-c902-4455-b382-f1fa470c8a3e")}catch{}})();const p=["width","height","fill","transform"],y={key:0},w=l("path",{d:"M216,44H40A12,12,0,0,0,28,56V208a20,20,0,0,0,20,20H88a20,20,0,0,0,20-20V164h40v12a20,20,0,0,0,20,20h40a20,20,0,0,0,20-20V56A12,12,0,0,0,216,44Zm-12,64H172V68h32ZM84,68v40H52V68Zm0,136H52V132H84Zm24-64V68h40v72Zm64,32V132h32v40Z"},null,-1),M=[w],b={key:1},A=l("path",{d:"M216,56v64H160V56ZM40,208a8,8,0,0,0,8,8H88a8,8,0,0,0,8-8V120H40Z",opacity:"0.2"},null,-1),k=l("path",{d:"M216,48H40a8,8,0,0,0-8,8V208a16,16,0,0,0,16,16H88a16,16,0,0,0,16-16V160h48v16a16,16,0,0,0,16,16h40a16,16,0,0,0,16-16V56A8,8,0,0,0,216,48Zm-8,64H168V64h40ZM88,64v48H48V64Zm0,144H48V128H88Zm16-64V64h48v80Zm64,32V128h40v48Z"},null,-1),B=[A,k],D={key:2},I=l("path",{d:"M160,56v96a8,8,0,0,1-8,8H112a8,8,0,0,1-8-8V56a8,8,0,0,1,8-8h40A8,8,0,0,1,160,56Zm64-8H184a8,8,0,0,0-8,8v52a4,4,0,0,0,4,4h48a4,4,0,0,0,4-4V56A8,8,0,0,0,224,48Zm4,80H180a4,4,0,0,0-4,4v44a16,16,0,0,0,16,16h24a16,16,0,0,0,16-16V132A4,4,0,0,0,228,128ZM80,48H40a8,8,0,0,0-8,8v52a4,4,0,0,0,4,4H84a4,4,0,0,0,4-4V56A8,8,0,0,0,80,48Zm4,80H36a4,4,0,0,0-4,4v76a16,16,0,0,0,16,16H72a16,16,0,0,0,16-16V132A4,4,0,0,0,84,128Z"},null,-1),S=[I],_={key:3},x=l("path",{d:"M216,50H40a6,6,0,0,0-6,6V208a14,14,0,0,0,14,14H88a14,14,0,0,0,14-14V158h52v18a14,14,0,0,0,14,14h40a14,14,0,0,0,14-14V56A6,6,0,0,0,216,50Zm-6,64H166V62h44ZM90,62v52H46V62Zm0,146a2,2,0,0,1-2,2H48a2,2,0,0,1-2-2V126H90Zm12-62V62h52v84Zm106,32H168a2,2,0,0,1-2-2V126h44v50A2,2,0,0,1,208,178Z"},null,-1),z=[x],C={key:4},N=l("path",{d:"M216,48H40a8,8,0,0,0-8,8V208a16,16,0,0,0,16,16H88a16,16,0,0,0,16-16V160h48v16a16,16,0,0,0,16,16h40a16,16,0,0,0,16-16V56A8,8,0,0,0,216,48ZM88,208H48V128H88Zm0-96H48V64H88Zm64,32H104V64h48Zm56,32H168V128h40Zm0-64H168V64h40Z"},null,-1),E=[N],P={key:5},$=l("path",{d:"M216,52H40a4,4,0,0,0-4,4V208a12,12,0,0,0,12,12H88a12,12,0,0,0,12-12V156h56v20a12,12,0,0,0,12,12h40a12,12,0,0,0,12-12V56A4,4,0,0,0,216,52ZM92,208a4,4,0,0,1-4,4H48a4,4,0,0,1-4-4V124H92Zm0-92H44V60H92Zm64,32H100V60h56Zm56,28a4,4,0,0,1-4,4H168a4,4,0,0,1-4-4V124h48Zm0-60H164V60h48Z"},null,-1),j=[$],K={name:"PhKanban"},R=u({...K,props:{weight:{type:String},size:{type:[String,Number]},color:{type:String},mirrored:{type:Boolean}},setup(o){const e=o,n=h("weight","regular"),d=h("size","1em"),i=h("color","currentColor"),s=h("mirrored",!1),V=H(()=>{var a;return(a=e.weight)!=null?a:n}),m=H(()=>{var a;return(a=e.size)!=null?a:d}),Z=H(()=>{var a;return(a=e.color)!=null?a:i}),v=H(()=>e.mirrored!==void 0?e.mirrored?"scale(-1, 1)":void 0:s?"scale(-1, 1)":void 0);return(a,q)=>(t(),r("svg",c({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 256 256",width:m.value,height:m.value,fill:Z.value,transform:v.value},a.$attrs),[g(a.$slots,"default"),V.value==="bold"?(t(),r("g",y,M)):V.value==="duotone"?(t(),r("g",b,B)):V.value==="fill"?(t(),r("g",D,S)):V.value==="light"?(t(),r("g",_,z)):V.value==="regular"?(t(),r("g",C,E)):V.value==="thin"?(t(),r("g",P,j)):f("",!0)],16,p))}});export{R as G};
//# sourceMappingURL=PhKanban.vue.51043e37.js.map
