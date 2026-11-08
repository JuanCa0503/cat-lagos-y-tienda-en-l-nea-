document.addEventListener("DOMContentLoaded", () => {
    cargarAutopartes();

    const searchInput = document.getElementById("search-input");
    const categoryFilter = document.getElementById("category-filter");

    if (searchInput) searchInput.addEventListener("input", filtrarProductos);
    if (categoryFilter) categoryFilter.addEventListener("change", filtrarProductos);
});

let todasLasAutopartes = [];

async function cargarAutopartes() {
    const grid = document.getElementById("products-grid");
    try {
        const response = await fetch("/api/autopartes");
        const data = await response.json();
        
        if (data.error) {
            grid.innerHTML = `<div class="col-span-full text-center py-12 text-red-500">Error: ${data.error}</div>`;
            return;
        }

        todasLasAutopartes = data;
        mostrarProductos(todasLasAutopartes);
    } catch (error) {
        grid.innerHTML = `<div class="col-span-full text-center py-12 text-red-500">No se pudieron cargar los artículos.</div>`;
    }
}

function mostrarProductos(productos) {
    const grid = document.getElementById("products-grid");
    if (!productos || productos.length === 0) {
        grid.innerHTML = `<div class="col-span-full text-center py-12 text-gray-500">No hay autopartes registradas.</div>`;
        return;
    }

    grid.innerHTML = productos.map(item => `
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden flex flex-col justify-between hover:shadow-md transition">
            <div>
                <!-- Imagen del producto -->
                <div class="h-48 w-full bg-gray-100 overflow-hidden relative">
                    <img src="${item.imagen_url || 'https://images.unsplash.com/photo-1486006920555-c77dce18193b?auto=format&fit=crop&w=500&q=80'}" 
                         alt="${item.nombre}" 
                         class="w-full h-full object-cover">
                </div>
                <div class="p-5">
                    <div class="flex justify-between items-start mb-2">
                        <span class="bg-sky-100 text-sky-800 text-xs font-semibold px-2.5 py-0.5 rounded">${item.categoria || 'General'}</span>
                        <span class="text-xs text-gray-400 font-mono">${item.codigo_sku || 'S/N'}</span>
                    </div>
                    <h3 class="font-bold text-slate-800 text-base mb-1">${item.nombre}</h3>
                    <p class="text-xs text-gray-500 mb-4">${item.descripcion || 'Sin descripción detallada.'}</p>
                </div>
            </div>
            <div class="px-5 pb-5 flex items-center justify-between pt-4 border-t border-gray-100">
                <span class="text-lg font-bold text-slate-900">$${item.precio !== null && item.precio !== undefined ? Number(item.precio).toFixed(2) : '0.00'}</span>
                <span class="text-xs font-medium text-emerald-600 bg-emerald-50 px-2 py-1 rounded">Stock: ${item.stock ?? 0}</span>
            </div>
        </div>
    `).join("");
}

function filtrarProductos() {
    const query = document.getElementById("search-input").value.toLowerCase();
    const categoriaSeleccionada = document.getElementById("category-filter").value;

    const filtrados = todasLasAutopartes.filter(item => {
        const coincideTexto = (item.nombre && item.nombre.toLowerCase().includes(query)) || 
                              (item.codigo_sku && item.codigo_sku.toLowerCase().includes(query));
        const coincideCategoria = categoriaSeleccionada === "TODAS" || item.categoria === categoriaSeleccionada;
        return coincideTexto && coincideCategoria;
    });

    mostrarProductos(filtrados);
}
