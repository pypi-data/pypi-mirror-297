import{C as E}from"./CrudView.187e7b93.js";import{a as D}from"./asyncComputed.a9aefa60.js";import{d as P,W as F,aq as V,u as t,o as u,X as C,aR as z,ee as L,c as I,w as s,b as o,aF as l,ec as x,d7 as k,cK as G,bx as M,$ as U,ed as q,f as H,a as S,bP as N,dd as W,d8 as A,d6 as T,R as K,d1 as X,f1 as Y,d9 as J,cD as O}from"./vue-router.daa9090b.js";import"./gateway.143b9d5b.js";import{g as Q,B as Z,a as tt}from"./datetime.e0bb10fd.js";import{P as et}from"./project.c819dd2a.js";import"./tables.6c4080db.js";import{C as st,r as B}from"./router.2e40d4d3.js";import{u as ot}from"./polling.1a044af4.js";import{_ as at,E as rt}from"./ExecutionStatusIcon.vue_vue_type_script_setup_true_lang.91637b19.js";import{G as it}from"./PhArrowCounterClockwise.vue.81fdc59e.js";import{F as R}from"./PhArrowSquareOut.vue.0aa4e14a.js";import{G as nt}from"./PhChats.vue.ec150648.js";import{I as lt}from"./PhCopySimple.vue.ad3f2b7d.js";import{F as dt}from"./PhRocketLaunch.vue.c8d1dc06.js";import{A as ct}from"./index.c441aec0.js";import"./DocsButton.vue_vue_type_script_setup_true_lang.ef44101d.js";import"./BookOutlined.37a8944e.js";import"./url.f89b68d7.js";import"./PhDotsThreeVertical.vue.00f8a21a.js";import"./index.91d5283b.js";import"./popupNotifcation.6bc3253c.js";import"./record.7a59ec24.js";import"./string.c6f29545.js";import"./LoadingOutlined.d9c72a6b.js";(function(){try{var _=typeof window<"u"?window:typeof global<"u"?global:typeof self<"u"?self:{},i=new Error().stack;i&&(_._sentryDebugIds=_._sentryDebugIds||{},_._sentryDebugIds[i]="0489ca81-fb78-475f-99d7-f7c53d2ce838",_._sentryDebugIdIdentifier="sentry-dbid-0489ca81-fb78-475f-99d7-f7c53d2ce838")}catch{}})();class g{constructor(i,d,f,m){this.major=i,this.minor=d,this.patch=f,this.dev=m}static from(i){if(i===null)return new g(0,0,0);const d=/^(\d+\.\d+\.\d+)(.dev(\d+))?$/,f=i.match(d);if(!f)return new g(0,0,0);const[,m,,w]=f,[h,c,v]=m.split(".").map(Number),y=w?Number(w):void 0;return isNaN(h)||isNaN(c)||isNaN(v)?new g(0,0,0):y&&isNaN(y)?new g(0,0,0):new g(h,c,v,y)}gte(i){return this.major!==i.major?this.major>=i.major:this.minor!==i.minor?this.minor>=i.minor:this.patch>=i.patch}get version(){const i=this.dev?`.dev${this.dev}`:"";return`${this.major}.${this.minor}.${this.patch}${i}`}}const pt=g.from("2.16.10"),ut={key:0,class:"flex-row"},ft={key:1,class:"flex-row"},mt={key:2,class:"flex-row"},gt=P({__name:"ExecutionsShort",props:{stageId:{},projectId:{}},emits:["select"],setup(_,{emit:i}){const d=_,f=new rt,{result:m,refetch:w,loading:h}=D(async()=>{const{executions:e}=await f.list({projectId:d.projectId,stageId:d.stageId,limit:6});return e}),c=e=>{i("select",e)},v=e=>Q(e,{weekday:void 0}),{startPolling:y,endPolling:$}=ot({task:w,interval:15e3});return F(()=>y()),V(()=>$()),(e,n)=>t(m)?(u(),C("div",ut,[(u(!0),C(z,null,L(t(m),r=>(u(),I(t(G),{key:r.id,title:v(r.createdAt),onClick:a=>c(r)},{content:s(()=>[o(t(k),null,{default:s(()=>[l("Status: "+x(r.status),1)]),_:2},1024),o(t(k),null,{default:s(()=>[l("Duration: "+x(r.duration_seconds),1)]),_:2},1024),o(t(k),null,{default:s(()=>[l("Build: "+x(r.buildId.slice(0,6)),1)]),_:2},1024)]),default:s(()=>[o(at,{status:r.status},null,8,["status"])]),_:2},1032,["title","onClick"]))),128))])):t(h)?(u(),C("div",ft,[o(t(M))])):(u(),C("div",mt,"None"))}});const _t=U(gt,[["__scopeId","data-v-9d19fd00"]]),ht={style:{"max-width":"250px",overflow:"hidden","text-overflow":"ellipsis ellipsis","white-space":"nowrap"}},yt={key:1},bt={class:"desc",style:{"margin-bottom":"80px",padding:"10px 30px","background-color":"#f6f6f6","border-radius":"5px"}},kt=P({__name:"Live",setup(_){const d=q().params.projectId,f=()=>{var n;const e=(n=c.value)==null?void 0:n.project.getUrl();e&&window.open(e,"_blank")},m=()=>{var b,p,j;const e=(p=(b=c.value)==null?void 0:b.buildSpec)==null?void 0:p.abstraVersion;if(!e)return;let n="threads";g.from(e).gte(pt)||(n="_player/"+n);const a=((j=c.value)==null?void 0:j.project.getUrl())+n;window.open(a,"_blank")},w=e=>{B.push({name:"logs",params:{projectId:d},query:{stageId:e.stageId,executionId:e.id}})},{loading:h,result:c}=D(async()=>{const n=(await Z.list(d)).find(b=>b.latest);if(!n)return null;const[r,a]=await Promise.all([tt.get(n.id),et.get(d)]);return{buildSpec:r,project:a}}),v=e=>{var a;if(!("path"in e)||!e.path)return;const n=e.type==="form"?`/${e.path}`:`/_hooks/${e.path}`,r=(a=c.value)==null?void 0:a.project.getUrl(n);!r||(navigator.clipboard.writeText(r),O.success("Copied URL to clipboard"))},y=e=>e.type=="form"?`/${e.path}`:e.type=="hook"?`/_hooks/${e.path}`:e.type=="job"?`${e.schedule}`:"",$=H(()=>{var r;const e=[{name:"Type",align:"left"},{name:"Title",align:"left"},{name:"Trigger",align:"left"},{name:"Last Runs"},{name:"",align:"right"}],n=(r=c.value)==null?void 0:r.buildSpec;return n?{columns:e,rows:n.runtimes.map(a=>({key:a.id,cells:[{type:"tag",text:a.type.charAt(0).toUpperCase()+a.type.slice(1),tagColor:"default"},{type:"slot",key:"title",payload:{runtime:a}},{type:"slot",key:"trigger",payload:{runtime:a}},{type:"slot",key:"last-runs",payload:{runtime:a}},{type:"actions",actions:[{icon:it,label:"View script logs",onClick:()=>B.push({name:"logs",params:{projectId:d},query:{stageId:a.id}})},{icon:lt,label:"Copy URL",onClick:()=>v(a),hide:!["form","hook"].includes(a.type)}]}]}))}:{columns:e,rows:[]}});return(e,n)=>{var r,a,b;return t(h)||((b=(a=(r=t(c))==null?void 0:r.buildSpec)==null?void 0:a.runtimes.length)!=null?b:0)>0?(u(),I(E,{key:0,"empty-title":"","entity-name":"build",description:"Access and monitor your project's current scripts here.",table:$.value,loading:t(h),title:"Live View"},{description:s(()=>[o(t(W),{gap:"middle",style:{"margin-top":"12px"}},{default:s(()=>[o(t(N),{onClick:f},{default:s(()=>[l(" Home"),o(t(R),{class:"icon",size:16})]),_:1}),o(t(N),{onClick:m},{default:s(()=>[l(" Threads"),o(t(R),{class:"icon",size:16})]),_:1})]),_:1})]),title:s(({payload:p})=>{var j;return[S("div",ht,[p.runtime.type!="form"?(u(),I(t(A),{key:0},{default:s(()=>[l(x(p.runtime.title),1)]),_:2},1024)):p.runtime.type=="form"?(u(),I(t(T),{key:1,href:(j=t(c))==null?void 0:j.project.getUrl(p.runtime.path),target:"_blank"},{default:s(()=>[l(x(p.runtime.title),1)]),_:2},1032,["href"])):K("",!0)])]}),"last-runs":s(({payload:p})=>[o(_t,{"stage-id":p.runtime.id,"project-id":t(d),onSelect:w},null,8,["stage-id","project-id"])]),trigger:s(({payload:p})=>[o(t(X),{color:"default",class:"ellipsis"},{default:s(()=>[l(x(y(p.runtime)),1)]),_:2},1024)]),_:1},8,["table","loading"])):(u(),C("section",yt,[S("div",bt,[o(t(J),{style:{display:"flex","align-items":"center",gap:"5px"},level:3},{default:s(()=>[o(t(Y),{size:"30"}),l(" Getting started ")]),_:1}),o(t(k),null,{default:s(()=>[l(" Check out the documentation: "),o(t(T),{href:"https://docs.abstra.io",target:"_blank"},{default:s(()=>[l("Abstra Docs")]),_:1})]),_:1}),o(t(k),null,{default:s(()=>[l(" Install the editor using pip: "),o(t(A),{code:"",copyable:""},{default:s(()=>[l("pip install abstra")]),_:1})]),_:1}),o(t(k),null,{default:s(()=>[l(" Run the editor: "),o(t(A),{code:"",copyable:""},{default:s(()=>[l("abstra editor my-new-project")]),_:1})]),_:1}),o(t(k),null,{default:s(()=>[l(" Feeling lost? "),o(t(N),{target:"_blank",type:"default",size:"small",onClick:n[0]||(n[0]=()=>t(st).showNewMessage("I need help getting started with Abstra"))},{default:s(()=>[o(t(nt))]),_:1})]),_:1})]),o(t(ct),{status:"info",title:"Waiting for your first deploy!","sub-title":"Your live stages will appear here once you make your first deploy"},{icon:s(()=>[o(t(dt),{size:"100",color:"#d14056"})]),_:1})]))}}});const Wt=U(kt,[["__scopeId","data-v-90c62d52"]]);export{Wt as default};
//# sourceMappingURL=Live.22dbd80b.js.map
