import { hello, showItems } from "./scripts/tests.mjs";    
import {} from "./scripts/functions/search.mjs";


hello();


// searchBar = document.getElementById('searchBar');
// searchBar.addEventListener('input', (e) => {
//     let value = e.target.value;
//     // Check if input exists and is greater than 0
//     if (value && value.trim().length > 0){
//         value. value.trim().toLowerCase();

//         // Return results that include the value of the search
//         setDiv(items.filter(item => {
//             return item.name.includes(value);
//         }))
//     }else{
        
//     }
// })

function setDiv(results){
    for(const item of results){
        const resultItem= document.createElement('div');
        resultItem.classList.add('result-item');
        const text = document.createTextNode(item.title)
        resultItem.appendChild(text)
        list.appendChild(resultItem)
    }
}
