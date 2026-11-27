document.addEventListener('DOMContentLoaded',()=>{
const toggle=document.querySelector('.menu-toggle'),nav=document.querySelector('.nav');if(toggle&&nav)toggle.addEventListener('click',()=>nav.classList.toggle('open'));
const params=new URLSearchParams(location.search),select=document.getElementById('serviceSelect'),requested=params.get('servicio');const pick=()=>{if(select&&requested){const o=[...select.options].find(x=>x.textContent===requested);if(o)select.value=o.value}};pick();
const date=document.getElementById('dateInput');if(date){const d=new Date();d.setMinutes(d.getMinutes()-d.getTimezoneOffset());date.min=d.toISOString().split('T')[0]}
const af=document.getElementById('appointmentForm');if(af)af.addEventListener('submit',async e=>{e.preventDefault();const m=document.getElementById('appointmentMessage'),btn=af.querySelector('button');m.style.color='';m.textContent='Guardando tu cita...';btn.disabled=true;try{const r=await fetch(af.action,{method:'POST',body:new FormData(af),headers:{'X-Requested-With':'XMLHttpRequest'}});const d=await r.json();if(d.ok){m.textContent=d.mensaje;af.reset();pick()}else{m.style.color='#ff6b6b';m.innerHTML=d.errores.join('<br>')}}catch(err){m.style.color='#ff6b6b';m.textContent='No se pudo guardar la cita. Intenta de nuevo.'}btn.disabled=false});
const cf=document.getElementById('contactForm');if(cf)cf.addEventListener('submit',e=>{e.preventDefault();document.getElementById('contactMessage').textContent='✓ Mensaje enviado correctamente. ¡Gracias por contactarnos!';cf.reset()});
const filters=document.querySelectorAll('.filter'),products=document.querySelectorAll('.product-card');filters.forEach(x=>x.addEventListener('click',()=>{filters.forEach(y=>y.classList.remove('active'));x.classList.add('active');const c=x.dataset.filter;products.forEach(p=>p.style.display=c==='todos'||p.dataset.category===c?'':'none')}));
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const money=n=>'$'+Number(n).toLocaleString('es-MX',{minimumFractionDigits:0,maximumFractionDigits:2});
let cart=JSON.parse(localStorage.getItem('blacklineCart')||'[]').filter(i=>i&&i.id),count=document.getElementById('cartCount'),box=document.getElementById('cartBox');
const qb='margin-left:6px;min-width:30px;padding:4px 8px;background:none;border:1px solid #303431;color:#d4ae62;cursor:pointer';
const save=()=>localStorage.setItem('blacklineCart',JSON.stringify(cart));
function update(msg){
  if(count)count.textContent=cart.reduce((s,i)=>s+i.qty,0);
  if(!box)return;
  if(!cart.length&&!msg){box.classList.add('hidden');box.innerHTML='';return}
  box.classList.remove('hidden');
  const total=cart.reduce((s,i)=>s+i.price*i.qty,0);
  box.innerHTML='<h3>Tu carrito</h3>'+(msg?`<div class="form-message">${esc(msg)}</div>`:'')
    +cart.map(i=>`<div class="cart-row"><span>${esc(i.name)} × ${i.qty}</span><span>${money(i.price*i.qty)}
      <button type="button" data-act="menos" data-id="${i.id}" title="Quitar una pieza" style="${qb}">−</button>
      <button type="button" data-act="mas" data-id="${i.id}" title="Agregar una pieza" style="${qb}">+</button>
      <button type="button" data-act="quitar" data-id="${i.id}" title="Eliminar producto" style="${qb};color:#ff6b6b">✕</button></span></div>`).join('')
    +(cart.length?`<div class="cart-total">Total: ${money(total)}</div>
    <form id="checkoutForm" style="display:grid;gap:10px;margin-top:16px">
      <h4>Datos del cliente</h4>

      <input required name="nombre" maxlength="120" placeholder="Nombre completo" style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

      <input required type="email" name="correo" placeholder="Correo electrónico" style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

      <input required type="tel" name="telefono" maxlength="30" placeholder="Número de teléfono" style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

      <h4>Dirección de envío</h4>

      <input required name="direccion" maxlength="200" placeholder="Calle y número" style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

      <input required name="colonia" maxlength="120" placeholder="Colonia" style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

      <input required name="municipio" maxlength="120" placeholder="Municipio" style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

      <input required name="codigo_postal" maxlength="10" placeholder="Código postal" style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

      <h4>Pago con tarjeta</h4>

<input required name="titular" maxlength="100"
placeholder="Nombre del titular"
style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

<input required name="tarjeta" inputmode="numeric"
maxlength="19" pattern="[0-9 ]{13,19}"
placeholder="Número de tarjeta"
style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

<input required name="vencimiento" placeholder="Fecha de vencimiento (MM/AA)"
pattern="(0[1-9]|1[0-2])/[0-9]{2}"
style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

<input required name="cvv" inputmode="numeric"
maxlength="4" pattern="[0-9]{3,4}"
placeholder="CVV "
style="padding:12px;background:#090a0a;border:1px solid #303431;color:#fff">

<p style="font-size:12px;color:#aaa">
</p>

      <button class="btn btn-primary">Realizar pago y finalizar compra →</button>

      <button type="button" id="clearCart" class="btn btn-small">Vaciar carrito</button>

      <div id="checkoutMsg" class="form-message"></div>
</form>`:'');
}
document.querySelectorAll('.add-cart').forEach(b=>b.addEventListener('click',()=>{const id=Number(b.dataset.id),n=b.dataset.name,p=Number(b.dataset.price),old=cart.find(i=>i.id===id);old?old.qty++:cart.push({id,name:n,price:p,qty:1});save();update();b.textContent='✓ Agregado';setTimeout(()=>b.textContent='Agregar',900)}));
if(box){
  box.addEventListener('click',e=>{
    const t=e.target;
    if(t.id==='clearCart'){cart=[];save();update();return}
    const act=t.dataset&&t.dataset.act;if(!act)return;
    const it=cart.find(i=>i.id===Number(t.dataset.id));if(!it)return;
    if(act==='mas')it.qty=Math.min(20,it.qty+1);
    else if(act==='menos')it.qty-=1;
    else if(act==='quitar')it.qty=0;
    cart=cart.filter(i=>i.qty>0);save();update();
  });
  box.addEventListener('submit',async e=>{
    if(e.target.id!=='checkoutForm')return;e.preventDefault();
    const f=e.target,m=document.getElementById('checkoutMsg'),btn=f.querySelector('.btn-primary');
    m.style.color='';m.textContent='Procesando tu compra...';btn.disabled=true;
    try{
      const token=(document.querySelector('[name=csrfmiddlewaretoken]')||{}).value||'';
      const r=await fetch(box.dataset.checkoutUrl,{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':token},
      body:JSON.stringify({
  nombre:f.nombre.value,
  correo:f.correo.value,
  telefono:f.telefono.value,
  direccion:f.direccion.value,
  colonia:f.colonia.value,
  municipio:f.municipio.value,
  codigo_postal:f.codigo_postal.value,
  items:cart.map(i=>({id:i.id,qty:i.qty}))
})}); 
      const d=await r.json();
      if(d.ok){cart=[];save();update(d.mensaje)}else{m.style.color='#ff6b6b';m.innerHTML=d.errores.map(esc).join('<br>');btn.disabled=false}
    }catch(err){m.style.color='#ff6b6b';m.textContent='No se pudo procesar la compra. Intenta de nuevo.';btn.disabled=false}
  });
}
const cb=document.getElementById('cartButton');if(cb&&box)cb.addEventListener('click',()=>box.classList.toggle('hidden'));update();
});