(function(root){
'use strict';
const tokenize=text=>(text.toLowerCase().match(/[a-z0-9]+/g)||[]);
function search(docs,query,{method='bm25',limit=5}={}){
 if(!Number.isInteger(limit)||limit<1) return [];
 const terms=[...new Set(tokenize(query))]; if(!terms.length||!docs.length)return [];
 const bags=docs.map(d=>{const bag=new Map;for(const t of tokenize(d.title+' '+d.text))bag.set(t,(bag.get(t)||0)+1);return bag});
 const lengths=bags.map(b=>[...b.values()].reduce((a,b)=>a+b,0)); const avg=lengths.reduce((a,b)=>a+b,0)/docs.length;if(!avg)return [];
 const df=new Map;bags.forEach(b=>b.forEach((v,k)=>df.set(k,(df.get(k)||0)+1)));
 return docs.map((doc,i)=>{let score=0;const matched=[];for(const term of terms){const tf=bags[i].get(term)||0;if(tf){matched.push(term);score+=method==='overlap'?1:Math.log(1+(docs.length-df.get(term)+.5)/(df.get(term)+.5))*tf*2.5/(tf+1.5*(.25+.75*lengths[i]/avg))}}return {...doc,score,matched}}).filter(d=>d.score>0).sort((a,b)=>b.score-a.score||a.id.localeCompare(b.id)).slice(0,limit);
}
function evaluate(docs,cases,method='bm25'){
 const rows=cases.map(c=>{const hits=search(docs,c.query,{method,limit:5});const rank=hits.findIndex(h=>h.id===c.expected)+1;return {...c,rank,reciprocalRank:rank?1/rank:0}});
 return {rows,top1:rows.length?rows.filter(r=>r.rank===1).length/rows.length:0,mrr:rows.length?rows.reduce((s,r)=>s+r.reciprocalRank,0)/rows.length:0};
}
const api={tokenize,search,evaluate};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.SourceDesk=api;
})(typeof globalThis!=='undefined'?globalThis:this);
