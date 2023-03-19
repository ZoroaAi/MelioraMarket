import { hello, showItems } from "./scripts/tests.mjs";    
import {} from "./scripts/functions/search.mjs";


hello();


// Quantity Price:
quantity = document.getElementById('item_quantity').value;
price = document.getElementById('basket_item_price').value;
price = document.getElementById('item_quantity_price');

quantityPrice = quantity * price;
price.textContent = quantityPrice;
