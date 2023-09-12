const loginForm = document.getElementById("login-form");
const contentContainer = document.getElementById("product-container");
const searchForm =document.getElementById("search-form");
const baseEndpoint = "http://localhost:8000/api";

if (loginForm) {
    loginForm.addEventListener("submit", handleLogin)
}
if (searchForm) {
    searchForm.addEventListener("submit", handleSearch)
}
function handleSearch(e) {
    e.preventDefault();
    const searchFormData = new FormData(searchForm);
    const queryData = Object.fromEntries(searchForm);
    const searchParams = new URLSearchParams(queryData);
    const searchEndpoints = `${baseEndpoint}/search/?${searchParams}`
    const accessToken = localStorage.getItem("access")
    const headers = {
        "Content-Type": "application/json"
    }
    if (accessToken) headers["Authorization"] = `Bearer ${accessToken}`
    const options = {
        method: "GET",
        headers: headers
    }
    fetch(endpoint, options)
    .then(res => res.json())
    .then(data => {
        const validData = isTokenValid(data);
        if (validData && contentContainer) {
            contentContainer.innerHTML = ""
            if (data && data.hits) {
                let htmlStr = "";
                for (let result of data.hits) {
                    htmlStr += `<li>${result.title}</li>`
                }
                contentContainer.innerHTML = htmlStr;
                if (data.hits.length===0) {
                    contentContainerinnerHTML = "<p>No results Found</p>"
                } else {
                    contentContainer.innerHTML = "<p>No results found</p>"
                }
            }
        }
    })
    .catch(err => console.log("error search: ", err))
}

function handleLogin (e) {
    e.preventDefault();
    const loginEndpoint = `${baseEndpoint}/token/`;
    const loginFormData = new FormData(loginForm);
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

function handleAuthData(authData, callback) {
    const { access, refresh } = authData;

    if (typeof access !== 'string' || typeof refresh !== 'string') {
        return;
    }

    localStorage.setItem('access', access);
    localStorage.setItem('refresh', refresh);

    if (callback && typeof callback === 'function') {
        callback();
    }
}

const productList = () => {
    const productListEndpoint = `${baseEndpoint}/products`
    const accessToken = localStorage.getItem("access");
    console.log(accessToken)
    const options = {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`
        }
    }
    fetch(productListEndpoint, options)
    .then(res => {
        return Promise.all([res.json(), Promise.resolve(res.status)]);
    })
    .then(([data, statusCode])=> {
        if (statusCode !=200) return refreshAccessToken();
        writeInContainer(data)
    })
    .catch(err => {
        console.log("Error: ", err);
    });
}

function writeInContainer(data) {
    if (contentContainer) {
        contentContainer.innerHTML = `<pre>${JSON.stringify(data, null, 4)}</pre>`
    }
}

function isTokenValid (token){
    if (token.code && token.code === "token_not_valid") {
        alert("Please login again!!!");
        return false
    }
    return true
}

function validateJWTToken() {
    const endpoint = `${baseEndpoint}/token/verify/`
    const accessToken = localStorage.getItem("access") || null;
    if (!accessToken) {
        refreshAccessToken();
        return false;
    }
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`
        },
        body: JSON.stringify({
            token: localStorage.getItem("access")
        })
    }
    fetch(endpoint, options)
    .then(res => {
        console.log("res: ",res)
        return res.json()})
    .then(data => {
        // refresh token
        console.log("validate res: ",data)
    })
    .catch(err => console.log("Validate error:", err))
}

function refreshAccessToken() {
    const refreshToken = localStorage.getItem("refresh") || null;
    const refreshTokenEndpoint = `${baseEndpoint}/token/refresh/`;

    if (!refreshToken) {
        // contentContainer.innerHTML = "<h3>Unauthorization</h3>";
        return false;
    }

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access")}`
        },
        body: JSON.stringify({refresh: refreshToken}) 
    };

    fetch(refreshTokenEndpoint, options)
        .then(res => {
            return Promise.all([res.json(), Promise.resolve(res.status)]);
        })
        .then(([data, statusCode]) => {
            if (statusCode === 200) {
                localStorage.setItem("access", data.access);
                productList();
            }
            console.log(statusCode, "refresh res: ", data);
        })
        .catch(err => console.log("err: ", err));
}


function isPreviousAuthenticated() {
    const accessToken = localStorage.getItem("access") || null;
    const refreshToken = localStorage.getItem("refresh") || null;
    if (!accessToken){
        if (!refreshToken) {
            // contentContainer.innerHTML = "<h3>Authentication needed</h3>"
            return null
        }
    }
    productList()
}

isPreviousAuthenticated();
