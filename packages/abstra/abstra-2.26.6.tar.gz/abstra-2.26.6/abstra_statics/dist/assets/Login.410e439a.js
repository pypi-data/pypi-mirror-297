import{_}from"./Login.vue_vue_type_script_setup_true_lang.afd938c9.js";import{b as f,u as b}from"./workspaceStore.74650beb.js";import{d as m,eq as l,ed as y,X as g,b as w,u as d,o as k,$ as h}from"./vue-router.daa9090b.js";import"./Logo.217c4b13.js";import"./CircularLoading.12e4b10b.js";import"./index.2b93a546.js";import"./url.f89b68d7.js";import"./colorHelpers.cbe2471c.js";(function(){try{var e=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},o=new Error().stack;o&&(e._sentryDebugIds=e._sentryDebugIds||{},e._sentryDebugIds[o]="f1b58c7b-af9c-4f09-b103-a86ac1bf1b9b",e._sentryDebugIdIdentifier="sentry-dbid-f1b58c7b-af9c-4f09-b103-a86ac1bf1b9b")}catch{}})();const v={class:"runner"},I=m({__name:"Login",setup(e){const o=l(),r=y(),i=f(),a=b(),p=async()=>{await i.signUp();const{redirect:t,...s}=r.query;if(t){await o.push({path:t,query:s,params:r.params});return}o.push({name:"playerHome",query:s})};return(t,s)=>{var n,c,u;return k(),g("div",v,[w(_,{"logo-url":(c=(n=d(a).state.workspace)==null?void 0:n.logoUrl)!=null?c:void 0,"brand-name":(u=d(a).state.workspace)==null?void 0:u.brandName,onDone:p},null,8,["logo-url","brand-name"])])}}});const N=h(I,[["__scopeId","data-v-907be835"]]);export{N as default};
//# sourceMappingURL=Login.410e439a.js.map
