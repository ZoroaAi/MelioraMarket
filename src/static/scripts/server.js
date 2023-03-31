// Send AJAX request to server to update basket item's quantity
function updateBasketItem(basketItemId, quantityInput) {
    const newQuantity = parseInt(quantityInput.value);
  
    if (isNaN(newQuantity) || newQuantity <= 0) {
      alert("Invalid quantity");
      return;
    }
  
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `/update_basket_item/${basketItemId}`, true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  
    xhr.onload = function () {
      if (xhr.status === 200) {
        const response = JSON.parse(xhr.responseText);
        if (!response.success) {
          alert(response.message);
        } else {
          location.reload();
        }
      } else {
        alert("An error occurred while updating the quantity");
      }
    };
  
    xhr.send(`quantity=${newQuantity}`);
  }
  