/* ================================================================
   script.js — AutoLavado Cloud
   Consume API REST en Azure App Service
   DB: GCP Cloud SQL (PostgreSQL)
================================================================ */

// ── CONFIGURACIÓN ────────────────────────────────────────────────
// ⚠️ Reemplazar con la URL real de tu Azure App Service tras el despliegue
const API_BASE = "https://TU-APP.azurewebsites.net";

// ── ESTADO ───────────────────────────────────────────────────────
let editandoVehiculoId = null;
let vehiculosCache     = [];   // para el select de servicios y la tabla

// ── PRECIOS SUGERIDOS ────────────────────────────────────────────
const PRECIOS = {
  lavado_basico:    15000,
  lavado_completo:  25000,
  lavado_premium:   45000,
  encerado:         35000,
  tapizado:         60000,
  motor:            55000,
};

// ── LABELS ───────────────────────────────────────────────────────
const TIPO_LABEL = {
  sedan:"Sedán", camioneta:"Camioneta", moto:"Moto", bus:"Bus", camion:"Camión"
};
const SERVICIO_LABEL = {
  lavado_basico:"🫧 Lavado Básico", lavado_completo:"🚿 Lavado Completo",
  lavado_premium:"✨ Lavado Premium", encerado:"🌟 Encerado",
  tapizado:"🪑 Tapizado", motor:"⚙️ Motor",
};
const ESTADO_LABEL = {
  pendiente:"⏳ Pendiente", en_proceso:"🔄 En proceso",
  completado:"✅ Completado", cancelado:"❌ Cancelado",
};

// ── UTILIDADES ───────────────────────────────────────────────────
async function apiFetch(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    let msg = `Error ${res.status}`;
    try { const b = await res.json(); msg = b.detail || msg; } catch (_) {}
    throw new Error(msg);
  }
  if (res.status === 204) return null;
  return res.json();
}

function showToast(msg, tipo = "success") {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.className = `toast ${tipo}`;
  t.classList.remove("hidden");
  clearTimeout(t._tid);
  t._tid = setTimeout(() => t.classList.add("hidden"), 3200);
}

function setLoadingState(prefix, loading, error = null) {
  document.getElementById(`loading-${prefix}`).classList.toggle("hidden", !loading);
  const errEl = document.getElementById(`error-${prefix}`);
  if (error) { errEl.textContent = `⚠️ ${error}`; errEl.classList.remove("hidden"); }
  else errEl.classList.add("hidden");
  if (!loading && !error) document.getElementById(`tabla-${prefix}`).classList.remove("hidden");
  else if (loading) document.getElementById(`tabla-${prefix}`).classList.add("hidden");
}

function formatCOP(n) {
  return new Intl.NumberFormat("es-CO", { style:"currency", currency:"COP", maximumFractionDigits:0 }).format(n);
}
function formatFecha(iso) {
  if (!iso) return "—";
  return new Date(iso).toLocaleDateString("es-CO", { day:"2-digit", month:"short", year:"numeric", hour:"2-digit", minute:"2-digit" });
}

// ── NAVEGACIÓN ───────────────────────────────────────────────────
document.querySelectorAll(".nav-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    const view = btn.dataset.view;
    document.querySelectorAll(".view").forEach(v => v.classList.add("hidden"));
    document.getElementById(`view-${view}`).classList.remove("hidden");
    if (view === "vehiculos") cargarVehiculos();
    if (view === "servicios") cargarServicios();
  });
});

// ════════════════════════════════════════════════════════════════
//  VEHÍCULOS
// ════════════════════════════════════════════════════════════════

async function cargarVehiculos() {
  setLoadingState("vehiculos", true);
  try {
    vehiculosCache = await apiFetch("/api/vehiculos");
    renderTablaVehiculos(vehiculosCache);
    setLoadingState("vehiculos", false);
  } catch (e) {
    setLoadingState("vehiculos", false, e.message);
  }
}

function renderTablaVehiculos(lista) {
  const tbody = document.getElementById("tbody-vehiculos");
  if (!lista.length) {
    tbody.innerHTML = `<tr><td colspan="8" class="empty-row">Sin vehículos registrados</td></tr>`;
    return;
  }
  tbody.innerHTML = lista.map(v => `
    <tr>
      <td><strong>#${v.id}</strong></td>
      <td><code style="font-weight:700;color:var(--azure)">${v.placa}</code></td>
      <td>${v.marca} <span style="color:var(--muted)">${v.modelo}</span> <small style="color:var(--muted)">${v.anio ?? ""}</small></td>
      <td><span class="badge badge-${v.tipo}">${TIPO_LABEL[v.tipo] ?? v.tipo}</span></td>
      <td>${v.color ?? "—"}</td>
      <td>${v.propietario}</td>
      <td>${v.telefono ?? "—"}</td>
      <td>
        <div class="actions">
          <button class="btn btn-gcp"    onclick="verHistorial(${v.id},'${v.placa}')">📋 Historial</button>
          <button class="btn btn-edit"   onclick="editarVehiculo(${v.id})">✏️ Editar</button>
          <button class="btn btn-danger" onclick="eliminarVehiculo(${v.id},'${v.placa}')">🗑️</button>
        </div>
      </td>
    </tr>`).join("");
}

// ── Formulario vehículo ──────────────────────────────────────────
document.getElementById("btn-nuevo-vehiculo").addEventListener("click", () => {
  editandoVehiculoId = null;
  document.getElementById("form-vehiculo-titulo").textContent = "🚗 Nuevo vehículo";
  limpiarFormVehiculo();
  document.getElementById("form-vehiculo").classList.remove("hidden");
  document.getElementById("v-placa").focus();
});

document.getElementById("btn-cancelar-vehiculo").addEventListener("click", () =>
  document.getElementById("form-vehiculo").classList.add("hidden"));

document.getElementById("btn-guardar-vehiculo").addEventListener("click", guardarVehiculo);

function limpiarFormVehiculo() {
  ["placa","marca","modelo","anio","color","propietario","telefono"].forEach(id =>
    document.getElementById(`v-${id}`).value = "");
  document.getElementById("v-tipo").value = "sedan";
}

async function guardarVehiculo() {
  const placa       = document.getElementById("v-placa").value.trim().toUpperCase();
  const marca       = document.getElementById("v-marca").value.trim();
  const modelo      = document.getElementById("v-modelo").value.trim();
  const propietario = document.getElementById("v-propietario").value.trim();

  if (!placa)       { showToast("La placa es obligatoria", "error-toast"); return; }
  if (!marca)       { showToast("La marca es obligatoria", "error-toast"); return; }
  if (!modelo)      { showToast("El modelo es obligatorio", "error-toast"); return; }
  if (!propietario) { showToast("El propietario es obligatorio", "error-toast"); return; }

  const payload = {
    placa, marca, modelo, propietario,
    anio:     parseInt(document.getElementById("v-anio").value)  || null,
    color:    document.getElementById("v-color").value.trim()    || null,
    tipo:     document.getElementById("v-tipo").value,
    telefono: document.getElementById("v-telefono").value.trim() || null,
  };

  try {
    if (editandoVehiculoId) {
      await apiFetch(`/api/vehiculos/${editandoVehiculoId}`, { method:"PUT", body:JSON.stringify(payload) });
      showToast("✅ Vehículo actualizado");
    } else {
      await apiFetch("/api/vehiculos", { method:"POST", body:JSON.stringify(payload) });
      showToast("✅ Vehículo registrado");
    }
    document.getElementById("form-vehiculo").classList.add("hidden");
    cargarVehiculos();
  } catch (e) {
    showToast(e.message, "error-toast");
  }
}

async function editarVehiculo(id) {
  try {
    const v = await apiFetch(`/api/vehiculos/${id}`);
    editandoVehiculoId = id;
    document.getElementById("form-vehiculo-titulo").textContent = "✏️ Editar vehículo";
    document.getElementById("v-placa").value       = v.placa;
    document.getElementById("v-marca").value       = v.marca;
    document.getElementById("v-modelo").value      = v.modelo;
    document.getElementById("v-anio").value        = v.anio ?? "";
    document.getElementById("v-color").value       = v.color ?? "";
    document.getElementById("v-tipo").value        = v.tipo;
    document.getElementById("v-propietario").value = v.propietario;
    document.getElementById("v-telefono").value    = v.telefono ?? "";
    document.getElementById("form-vehiculo").classList.remove("hidden");
    window.scrollTo({ top:0, behavior:"smooth" });
  } catch (e) {
    showToast(e.message, "error-toast");
  }
}

async function eliminarVehiculo(id, placa) {
  if (!confirm(`¿Eliminar el vehículo con placa ${placa} y todos sus servicios?`)) return;
  try {
    await apiFetch(`/api/vehiculos/${id}`, { method:"DELETE" });
    showToast("🗑️ Vehículo eliminado");
    cargarVehiculos();
  } catch (e) {
    showToast(e.message, "error-toast");
  }
}

// ── Modal historial ───────────────────────────────────────────────
async function verHistorial(vehiculoId, placa) {
  try {
    const servicios = await apiFetch(`/api/vehiculos/${vehiculoId}/servicios`);
    document.getElementById("modal-titulo").textContent = `📋 Historial — Placa ${placa}`;
    if (!servicios.length) {
      document.getElementById("modal-body").innerHTML =
        `<p style="color:var(--muted);text-align:center;padding:1.5rem">Sin servicios registrados para este vehículo.</p>`;
    } else {
      const totalPagado = servicios
        .filter(s => s.estado === "completado")
        .reduce((acc, s) => acc + parseFloat(s.precio), 0);
      document.getElementById("modal-body").innerHTML = `
        <p style="font-size:.82rem;color:var(--muted);margin-bottom:.85rem">
          ${servicios.length} servicio(s) · Total pagado: <strong style="color:var(--gcp)">${formatCOP(totalPagado)}</strong>
        </p>
        ${servicios.map(s => `
          <div class="servicio-item">
            <div class="servicio-item-header">
              <span class="servicio-item-tipo">${SERVICIO_LABEL[s.tipo_servicio] ?? s.tipo_servicio}</span>
              <span class="servicio-item-precio">${formatCOP(s.precio)}</span>
            </div>
            <div class="servicio-item-footer">
              <span class="badge badge-${s.estado}">${ESTADO_LABEL[s.estado] ?? s.estado}</span>
              <span>📅 ${formatFecha(s.fecha_servicio)}</span>
              ${s.observaciones ? `<span>💬 ${s.observaciones}</span>` : ""}
            </div>
          </div>`).join("")}`;
    }
    document.getElementById("modal-overlay").classList.remove("hidden");
  } catch (e) {
    showToast(e.message, "error-toast");
  }
}

document.getElementById("btn-cerrar-modal").addEventListener("click", () =>
  document.getElementById("modal-overlay").classList.add("hidden"));
document.getElementById("modal-overlay").addEventListener("click", e => {
  if (e.target === e.currentTarget) e.currentTarget.classList.add("hidden");
});

// ════════════════════════════════════════════════════════════════
//  SERVICIOS
// ════════════════════════════════════════════════════════════════

async function cargarServicios() {
  setLoadingState("servicios", true);
  try {
    await cargarVehiculosSelect();
    const servicios = await apiFetch("/api/servicios");
    renderTablaServicios(servicios);
    setLoadingState("servicios", false);
  } catch (e) {
    setLoadingState("servicios", false, e.message);
  }
}

function renderTablaServicios(lista) {
  const tbody = document.getElementById("tbody-servicios");
  if (!lista.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="empty-row">Sin servicios registrados</td></tr>`;
    return;
  }
  tbody.innerHTML = lista.map(s => {
    const v = vehiculosCache.find(v => v.id === s.vehiculo_id);
    const placa = v ? v.placa : `ID ${s.vehiculo_id}`;
    return `
      <tr>
        <td><strong>#${s.id}</strong></td>
        <td><code style="font-weight:700;color:var(--azure)">${placa}</code></td>
        <td>${SERVICIO_LABEL[s.tipo_servicio] ?? s.tipo_servicio}</td>
        <td style="font-weight:700;color:var(--gcp)">${formatCOP(s.precio)}</td>
        <td><span class="badge badge-${s.estado}">${ESTADO_LABEL[s.estado] ?? s.estado}</span></td>
        <td style="font-size:.8rem;color:var(--muted)">${formatFecha(s.fecha_servicio)}</td>
        <td>
          <div class="actions">
            <button class="btn btn-danger" onclick="eliminarServicio(${s.id})">🗑️ Eliminar</button>
          </div>
        </td>
      </tr>`;
  }).join("");
}

// ── Formulario servicio ──────────────────────────────────────────
document.getElementById("btn-nuevo-servicio").addEventListener("click", async () => {
  await cargarVehiculosSelect();
  document.getElementById("s-tipo").value   = "lavado_basico";
  document.getElementById("s-precio").value = PRECIOS["lavado_basico"];
  document.getElementById("s-estado").value = "pendiente";
  document.getElementById("s-obs").value    = "";
  document.getElementById("form-servicio").classList.remove("hidden");
});

// Precio sugerido automático al cambiar tipo
document.getElementById("s-tipo").addEventListener("change", function() {
  const precio = PRECIOS[this.value];
  if (precio) document.getElementById("s-precio").value = precio;
});

document.getElementById("btn-cancelar-servicio").addEventListener("click", () =>
  document.getElementById("form-servicio").classList.add("hidden"));

document.getElementById("btn-guardar-servicio").addEventListener("click", async () => {
  const vehiculo_id = parseInt(document.getElementById("s-vehiculo").value);
  const precio      = parseFloat(document.getElementById("s-precio").value);

  if (!vehiculo_id) { showToast("Selecciona un vehículo", "error-toast"); return; }
  if (!precio || precio <= 0) { showToast("El precio debe ser mayor a 0", "error-toast"); return; }

  const payload = {
    vehiculo_id,
    tipo_servicio: document.getElementById("s-tipo").value,
    precio,
    estado:        document.getElementById("s-estado").value,
    observaciones: document.getElementById("s-obs").value.trim() || null,
  };

  try {
    await apiFetch("/api/servicios", { method:"POST", body:JSON.stringify(payload) });
    showToast("✅ Servicio registrado");
    document.getElementById("form-servicio").classList.add("hidden");
    cargarServicios();
  } catch (e) {
    showToast(e.message, "error-toast");
  }
});

async function cargarVehiculosSelect() {
  if (!vehiculosCache.length) vehiculosCache = await apiFetch("/api/vehiculos");
  const sel = document.getElementById("s-vehiculo");
  sel.innerHTML = vehiculosCache.length
    ? vehiculosCache.map(v => `<option value="${v.id}">${v.placa} — ${v.propietario} (${v.marca} ${v.modelo})</option>`).join("")
    : `<option value="">Sin vehículos registrados</option>`;
}

async function eliminarServicio(id) {
  if (!confirm("¿Eliminar este servicio?")) return;
  try {
    await apiFetch(`/api/servicios/${id}`, { method:"DELETE" });
    showToast("🗑️ Servicio eliminado");
    cargarServicios();
  } catch (e) {
    showToast(e.message, "error-toast");
  }
}

// ── INICIO ───────────────────────────────────────────────────────
cargarVehiculos();
