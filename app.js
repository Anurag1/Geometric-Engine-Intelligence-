const people=[
 ['Newton',450,325],['Kepler',450,80],['Galileo',220,135],['Descartes',680,135],['Hooke',760,300],['Huygens',700,510],['Boyle',520,570],['Bacon',300,570],['Halley',120,470],['Euclid',95,275],['Archimedes',170,180],['Pappus',190,430],['Leibniz',450,610]
];
const known=[['Newton','Kepler'],['Newton','Galileo'],['Newton','Hooke'],['Newton','Huygens'],['Newton','Halley'],['Newton','Leibniz'],['Newton','Descartes'],['Newton','Boyle'],['Newton','Bacon'],['Kepler','Galileo'],['Euclid','Archimedes'],['Archimedes','Pappus'],['Bacon','Boyle']];
const svg=document.querySelector('#graph'), result=document.querySelector('#result'), search=document.querySelector('#search'), stats=document.querySelector('#stats');
const names=people.map(p=>p[0]); const key=(a,b)=>[a,b].sort().join('|'); const knownSet=new Set(known.map(([a,b])=>key(a,b)));
function render(){
 svg.innerHTML='';
 const q=search.value.trim().toLowerCase();
 const visible=new Set(names.filter(n=>!q||n.toLowerCase().includes(q)));
 for(let i=0;i<people.length;i++)for(let j=i+1;j<people.length;j++){
  const a=people[i],b=people[j], line=document.createElementNS('http://www.w3.org/2000/svg','line');
  line.setAttribute('x1',a[1]);line.setAttribute('y1',a[2]);line.setAttribute('x2',b[1]);line.setAttribute('y2',b[2]);
  line.setAttribute('stroke',knownSet.has(key(a[0],b[0]))?'#52607e':'#273047');line.setAttribute('stroke-width',knownSet.has(key(a[0],b[0]))?'2':'1');line.setAttribute('opacity',q?(visible.has(a[0])&&visible.has(b[0])?.55:.06):.55);svg.appendChild(line);
 }
 people.forEach(([name,x,y])=>{const g=document.createElementNS('http://www.w3.org/2000/svg','g');g.style.cursor='pointer';g.style.opacity=q&& !visible.has(name)?.12:1;const c=document.createElementNS('http://www.w3.org/2000/svg','circle');c.setAttribute('cx',x);c.setAttribute('cy',y);c.setAttribute('r',name==='Newton'?34:25);c.setAttribute('fill',name==='Newton'?'#f0b429':'#111a2c');c.setAttribute('stroke',name==='Newton'?'#fff0a3':'#7180ff');c.setAttribute('stroke-width','2');const t=document.createElementNS('http://www.w3.org/2000/svg','text');t.setAttribute('x',x);t.setAttribute('y',y+45);t.setAttribute('text-anchor','middle');t.setAttribute('fill','#e8edff');t.setAttribute('font-size','14');t.textContent=name;g.append(c,t);g.onclick=()=>showNode(name);svg.appendChild(g)});
 stats.textContent=`${people.length} nodes • ${people.length*(people.length-1)/2} possible edges • ${knownSet.size} seeded edges • ${people.length*(people.length-1)/2-knownSet.size} unexplored`;
}
function showNode(name){const unexplored=names.filter(n=>n!==name&&!knownSet.has(key(name,n)));result.innerHTML=`<strong>${name}</strong><br>${unexplored.length} unexplored pairwise edges. Candidate questions: “Why is this relationship absent?” and “What would happen if these two idea clusters were combined?”`;}
document.querySelector('#reset').onclick=()=>{search.value='';result.textContent='Select a node or run discovery.';render()};document.querySelector('#discover').onclick=()=>{const candidates=[];for(let i=0;i<names.length;i++)for(let j=i+1;j<names.length;j++)if(!knownSet.has(key(names[i],names[j])))candidates.push([names[i],names[j]]);const [a,b]=candidates[Math.floor(candidates.length/2)];result.innerHTML=`<strong>Unexplored edge:</strong> ${a} ↔ ${b}<br>Hypothesis seed: compare their concepts, evidence and contradictions; identify a test that could distinguish a genuinely new relationship from a superficial analogy.`};search.addEventListener('input',render);render();
