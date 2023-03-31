export function updateBasketItemQuantity(button, basketItemId, change) {
    console.log('Updating Item Quantity');
    const quantityInput = button.parentElement.querySelector(".item_quantity");
    const currentQuantity = parseInt(quantityInput.value);

    if (isNaN(currentQuantity) || currentQuantity <= 0) {
        alert("Invalid quantity");
        return;
    }

    const newQuantity = currentQuantity + change;

    if (newQuantity <= 0) {
        alert("Quantity cannot be less than 1");
        return;
    }

    const csrfToken = getCsrfToken();
    if (!csrfToken) {
        alert("CSRF token not found");
        return;
    }

    const xhr = new XMLHttpRequest();
    xhr.open("POST", `/update_basket_item/${basketItemId}`, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);

    xhr.onload = function () {
        if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        if (!response.success) {
            alert(response.message);
        } else {
            quantityInput.value = newQuantity;
            location.reload();
        }
        } else {
        alert("An error occurred while updating the quantity");
        }
    };

    xhr.send(`quantity=${newQuantity}`);
}
  