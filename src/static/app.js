import { hello, showItems } from "./scripts/tests.mjs";   
import { openCloseMenu, openCloseSearch } from "./scripts/functions/navSearch.mjs"; 
hello();

// openCloseSearch(); openCloseMenu();

fetch("../test_data/tesco_test.json")
.then(response => response.json())
.then(data => showItems(data))

showItems(data)