// populate the list of cupcakes on page load

BASE_URL = 'http://localhost:5000/api/cupcakes'

async function populateList() {
    resp = await axios.get(BASE_URL)
    cupcakes = resp.data.cupcakes;

    for (let cupcake of cupcakes) {
        $listItem = addListHTML(cupcake);
        $('#cupcake-list').append($listItem);
    }
}

function addListHTML(cupcake) {
    return `<li>
                <p>${cupcake.flavor}</p>
                <p>${cupcake.size}</p>
                <p>${cupcake.rating}</p>
                <img src="${cupcake.image}" width="100">
            </li>`;
}

populateList();


// handles button click to add cupcake to database AND page

function updateListOnSubmit(flavor, size, rating, image) {
    return `<li>
                <p>${flavor}</p>
                <p>${size}</p>
                <p>${rating}</p>
                <img src="${image}" width="100">
            </li>`;
}

async function addCupcake(e) {
    e.preventDefault();

    const flavor = $('#flavor').val();
    const size = $('#size').val();
    const rating = $('#rating').val();
    const image = $('#image').val() == '' ? null : $('#image').val();

    await axios.post(BASE_URL, data = {
        flavor: flavor,
        size: size,
        rating: rating,
        image: image
    });

    $newItem = updateListOnSubmit(flavor, size, rating, image);
    $('#cupcake-list').append($newItem)
}

$('button').on('click', addCupcake);