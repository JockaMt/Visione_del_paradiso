const searchInput = document.getElementById('filtro');
const resultsList = document.getElementById('lista');
let debounceTimeout;

const path = window.location.pathname;
const listType = path.includes('rooms') ? 'rooms' : path.includes('services') ? 'services' : path.includes('events') ? 'events' : null;
console.log(`Username from session storage: ${username}`);

const card = (item) => {
    if (listType == 'rooms') {
        return (
            `
                <div onclick="select('${item.id}')" class="flex flex-col group bg-white dark:bg-gray-800 flex-1 overflow-hidden hover:scale-105 duration-300 rounded shadow-md hover:shadow-lg transition-all ease-[cubic-bezier(.01,2.48,.38,.52)] duration-300 min-w-48 w-auto h-auto">
                    <img class="w-full max-h-40 h-full object-cover" alt="item_image" src="${item.image}">
                    <div class="p-4 flex flex-col justify-between">
                        <p>${item.title}</p>
                        <div class="flex justify-between">
                        <p class="text-primary font-bold text-lg">${item.price}</p>
                        </div>
                        <p class="flex text-sm text-gray-600 dark:text-gray-200/50 duration-300">${item.description}</p>
                    </div>
                </div>
            `
        )
    } else if (listType == 'services') {
        return (
            `
                <div onclick="select(${item.id})" class="group bg-white dark:bg-gray-800 flex-1 overflow-hidden hover:scale-105 duration-300 rounded shadow-md hover:shadow-lg transition-all ease-[cubic-bezier(.01,2.48,.38,.52)] duration-300 min-w-48 w-auto h-auto">
                    <img class="w-full max-h-40 object-cover" alt="item_image" src="${item.image}">
                    <div class="p-4 flex flex-col justify-between">
                        <div class="flex justify-between">
                            <p class="first-letter:capitalize">${item.title}</p>
                        </div>
                        <p class="first-letter:capitalize flex text-sm text-gray-600 dark:text-gray-200/50 duration-300">${item.description}</p>
                    </div>
                </div>
            `
        )
    } else if (listType == 'events') {
        return (
            `
                <div onclick="select(${item.id})" class="group bg-white dark:bg-gray-800 flex-1 overflow-hidden hover:scale-105 duration-300 rounded shadow-md hover:shadow-lg transition-all ease-[cubic-bezier(.01,2.48,.38,.52)] duration-300 min-w-48 w-auto h-auto">
                    <div class="p-4 flex flex-col border-t-10 py-10 justify-between">
                        <div class="flex justify-between">
                            <p>${item.title}</p>
                        </div>
                        <p class="flex text-sm text-gray-600 dark:text-gray-200/50 duration-300">${item.description}</p>
                    </div>
                </div>
            `
        )
    }
}

searchInput.addEventListener('input', () => {
    clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(async () => {
        const searchTerm = searchInput.value;
        const response = await fetch(`/buscar?termo=${encodeURIComponent(searchTerm)}&type=${listType}&user=${username}`);
        const items = await response.json();

        resultsList.innerHTML = '';

        if (items.length === 0) {
            resultsList.innerHTML = '<p class="col-span-full text-center text-gray-500">Nenhum resultado encontrado.</p>';
        } else {
            items.forEach(item => {
                resultsList.insertAdjacentHTML('beforeend', card(item));
            });
        }
    }, 200); // debounce de 300ms
});

// Carrega todos os itens no início (se desejar)
window.addEventListener('DOMContentLoaded', () => {
    searchInput.dispatchEvent(new Event('input'));
});

const select = (id) => {
    if (listType === 'rooms') {
        window.location.href = `/rooms/room/${id}`;
    }
    if (listType === 'services') {
        window.location.href = `/services/service/${id}`;
    }
    if (listType === 'events') {
        window.location.href = `/events/event/${id}`;
    }
}