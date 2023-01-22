import { hello } from "./tests.mjs";    

// Go to Login Page:
loginButt = document.getElementById('butt');
loginButt.addEventListener(onclick,() => {
    window.location("../pages/login.html")
})