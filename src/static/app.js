import { hello, showItems } from "./scripts/tests.mjs";    
import {} from "./scripts/functions/search.mjs";


hello();

const showRegisterFormBtn = document.getElementById('show-register-page');
const showLoginFormBtn = document.getElementById('show-login-form-page');
const loginForm = document.getElementById('login-container');
const registerForm = document.getElementById('register-container');

showRegisterFormBtn.addEventListener('click', () => {
  loginForm.style.display = 'none';
  registerForm.style.display = 'block';
});

showLoginFormBtn.addEventListener('click', () => {
  loginForm.style.display = 'block';
  registerForm.style.display = 'none';
});
