webpackJsonp([6],{"F0+0":function(e,a){},F5Is:function(e,a,r){"use strict";Object.defineProperty(a,"__esModule",{value:!0});var o=r("gyMJ"),t={data:function(){return{clocksPerPage:5,clocksCurrentPage:1,fields:["ClockName","FeaturesNum","LifePhase","Platform","Tissue","Reference"],clocksData:[{ClockName:"Horvath Clock",Tissue:"Pan-tissue",FeaturesNum:353,Platform:"HM450","Error(Years)":3.5,Reference:"<a href='https://doi.org/10.1186/gb-2013-14-10-r115'>Horvath, 2013</a>",LifePhase:"lifespan"},{ClockName:"Skin&Blood Clock",Tissue:"Blood,Epithelium,Saliva,Skin",FeaturesNum:"391",Platform:"HM450, HMEPIC",Reference:"<a href='https://doi.org/10.18632/aging.101508'>Horvath et al., 2018</a>","Error(Years)":4.5,LifePhase:"lifespan"},{ClockName:"Zhang Clock",Tissue:"Adipose,Blood,Brain,Breast,Liver,Saliva,Uterine",FeaturesNum:514,Platform:"HM450, HMEPIC",Reference:"<a href='https://doi.org/10.1186/s13073-019-0667-1'>Zhang et al., 2019</a>","Error(Years)":5.6,LifePhase:"lifespan"},{ClockName:"Hannum Clock",Tissue:"Blood",FeaturesNum:"71",Platform:"HM450",Reference:"<a href='https://doi.org/10.1016/j.molcel.2012.10.016'>Hannum et al., 2013</a>","Error(Years)":3.8,LifePhase:"lifespan"},{ClockName:"Weidner Clock",Tissue:"Blood",FeaturesNum:"3",Platform:"HM27",Reference:"<a href='https://doi.org/10.18632/aging.101414'>Weidner et al., 2014</a>","Error(Years)":5.6,LifePhase:"lifespan"},{ClockName:"Lin Clock",Tissue:"Blood",FeaturesNum:102,Platform:"HM450",Reference:"<a href='https://doi.org/10.18632/aging.100908'>Lin et al., 2016</a>","Error(Years)":.35,LifePhase:"lifespan"},{ClockName:"PedBE",Tissue:"Buccal,Epithelial",FeaturesNum:"94",Platform:"HM450",Reference:"<a href='https://doi.org/10.1073/pnas.1820843116'>McEwen et al., 2020</a>","Error(Years)":5.6,LifePhase:"adult"},{ClockName:"FeSTwo",Tissue:"Multi",FeaturesNum:70,Platform:"HM450",Reference:"<a href='https://doi.org/10.1016/j.compbiomed.2020.104008'>Wei et al., 2020</a>","Error(Years)":5.6,LifePhase:"adult"},{ClockName:"MEAT",Tissue:"skeletal muscle",FeaturesNum:156,Platform:"HM27, HM450, HMEPIC",Reference:"<a href='https://doi.org/10.1002/jcsm.12556'>Voisin et al., 2020</a>","Error(Years)":5.6,LifePhase:"adult"},{ClockName:"AltumAge",Tissue:"Multi",FeaturesNum:20318,Platform:"HM27, HM450, HMEPIC",Reference:"<a href='https://www.nature.com/articles/s41514-022-00085-y'>Camillo et al., 2022</a>","Error(Years)":5.6,LifePhase:"adult"},{ClockName:"PhenoAge",Tissue:"Multi",FeaturesNum:513,Platform:"HM27, HM450, HMEPIC",Reference:"<a href='https://doi.org/10.18632/aging.101414'>Levine  et al., 2018</a>","Error(Years)":5.6,LifePhase:"adult"},{ClockName:"BNN",Tissue:"Multi",FeaturesNum:353,Platform:"HM27, HM450",Reference:"<a href='https://doi.org/10.1101/2020.04.21.052605'>Gonzalez et al., 2020</a>","Error(Years)":5.6,LifePhase:"adult"},{ClockName:"EPM",Tissue:"Multi",FeaturesNum:1e3,Platform:"HM450",Reference:"<a href='https://doi.org/10.1093/bioinformatics/btaa585'>Farrell et al., 2020</a>","Error(Years)":5.6,LifePhase:"lifespan"},{ClockName:"Cortical Clock",Tissue:"Cortex",FeaturesNum:347,Platform:"HM450",Reference:"<a href='https://doi.org/10.1093/brain/awaa334'>Shireby et al., 2020</a>","Error(Years)":5.6,LifePhase:"lifespan"},{ClockName:"VidalBralo Clock",Tissue:"Blood",FeaturesNum:8,Platform:"HM27, HM450",Reference:"<a href='https://doi.org/10.3389/fgene.2016.00126'> Vidal-Bralo et al., 2016</a>","Error(Years)":5.6,LifePhase:"adult"}]}},computed:{clocksTableRows:function(){return this.clocksData.length}},created:function(){var e=this;Object(o.b)().then(function(a){console.log(a.data),e.clocksData=a.data.data})}},s={render:function(){var e=this,a=e.$createElement,r=e._self._c||a;return r("div",{staticClass:"clocksBox"},[r("b-row",[r("h3",[e._v("Currently Available Clocks in "),r("i",{staticStyle:{color:"red"}},[e._v("DNAm Clocks")]),e._v(" are Listed in Table Below")])]),r("hr"),e._v(" "),r("b-row",[r("b-table",{attrs:{id:"clocksTable",fields:e.fields,items:e.clocksData,"head-variant":"light","per-page":e.clocksPerPage,"current-page":e.clocksCurrentPage,pagination:!0,responsive:""},scopedSlots:e._u([{key:"cell(Reference)",fn:function(a){return[r("span",{domProps:{innerHTML:e._s(a.value)}})]}}])}),e._v(" "),r("b-pagination",{attrs:{"total-rows":e.clocksTableRows,"per-page":e.clocksPerPage,align:"right","aria-controls":"sampleTable"},model:{value:e.clocksCurrentPage,callback:function(a){e.clocksCurrentPage=a},expression:"clocksCurrentPage"}})],1)],1)},staticRenderFns:[]};var l=r("VU/8")(t,s,!1,function(e){r("F0+0")},"data-v-c17afc2c",null);a.default=l.exports}});
//# sourceMappingURL=6.4afc4d56423b9542e316.js.map