const loginForm = document.getElementById("login-form");
const contentContainer = document.getElementById("product-container")
const baseEndpoint = "http://localhost:8000/api";

if (loginForm) {
    loginForm.addEventListener("submit", handleLogin)
}

function handleLogin(e) {
    console.log(e);
    e.preventDefault();
    const loginEndpoint = `${baseEndpoint}/token/`;
    const loginFormData = new FormData(loginForm);
    console.log(loginFormData)
    const loginObjectFormData = Object.fromEntries(loginFormData);
    const options = {
        method: "POST",
        headers: {
            "content-Type": "application/json"
        },
        body: JSON.stringify(loginObjectFormData)
    }
    fetch(loginEndpoint, options)
    .then(res => {
        return res.json()
    })
    .then(data => handleAuthData(data, productList))
    .catch(err => {
        console.log("err", err)
    })
}

const handleAuthData = (authData, callback) => {
    localStorage.setItem("access", authData.access);
    localStorage.setItem("refresh", authData.refresh)
    if (callback) {
        callback();
    }
}

const productList = () => {
    const productListEndpoint = `${baseEndpoint}/products`
    const accessToken = localStorage.getItem("access");
    const options = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`
        }
    }
    fetch(productListEndpoint, options)
    .then(res => res.json())
    .then(data => {
        writeInContainer(data);
    })
    .catch(err => console.log("Error: ", err));
}

const writeInContainer = (data) => {
    if (contentContainer) {
        contentContainer.innerHTML = `<pre>${JSON.stringify(data, null, 4)}</pre>`
    }
}
productList();