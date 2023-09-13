const loginForm = document.getElementById("login-form");
const contentContainer = document.getElementById("product-container");
const searchForm = document.getElementById("search-form");
const baseEndpoint = "http://localhost:8000/api";

if (loginForm) {
    loginForm.addEventListener("submit", handleLogin)
}
if (searchForm) {
    searchForm.addEventListener("submit", handleSearch)
}
function handleSearch(e) {
    e.preventDefault();

    // Get the search form data
    const searchFormData = new FormData(searchForm);
    const queryData = Object.fromEntries(searchFormData);
    const searchParams = new URLSearchParams(queryData);
    const searchEndpoint = `http://localhost:8000/v4/api/search/v2/?${searchParams.toString()}`;

    // Prepare headers
    const headers = {
        "Content-Type": "application/json"
    };

    // Refresh the access token if needed
    refreshAccessToken();
    const accessToken = localStorage.getItem("access");
    if (accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }

    // Create fetch options
    const options = {
        method: "GET",
        headers: headers
    };

    // Make the API request
    fetch(searchEndpoint, options)
        .then(res => {
            console.log(res)
            if (!res.ok) {
                throw new Error("Network response was not ok");
            }
            return res.json();
        })
        .then(data => {
            console.log("data:", data);
            if (contentContainer) {
                contentContainer.innerHTML = "";
                if (data && data.hits) {
                    let htmlStr = "";
                    for (let result of data.hits) {
                        htmlStr += `<li><pre>${JSON.stringify(result.title, null, 2)}</pre></li>`;
                    }
                    contentContainer.innerHTML = htmlStr;
                    if (data.hits.length === 0) {
                        contentContainer.innerHTML = "<p>No results found</p>";
                    }
                }
            }
        })
        .catch(err => console.error("Error searching:", err));
}


function handleLogin(e) {
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
        .then(([data, statusCode]) => {
            if (statusCode != 200) return refreshAccessToken();
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

function isTokenValid(token) {
    if (token.code && token.code === "token_not_valid") {
        refreshAccessToken();
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
            console.log("res: ", res)
            return res.json()
        })
        .then(data => {
            // refresh token
            console.log("validate res: ", data)
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
        body: JSON.stringify({ refresh: refreshToken })
    };

    fetch(refreshTokenEndpoint, options)
        .then(res => {
            return Promise.all([res.json(), Promise.resolve(res.status)]);
        })
        .then(([data, statusCode]) => {
            if (statusCode === 200) {
                localStorage.setItem("access", data.access);
            }
            console.log(statusCode, "refresh res: ", data);
        })
        .catch(err => console.log("err: ", err));
}


function isPreviousAuthenticated() {
    const accessToken = localStorage.getItem("access") || null;
    const refreshToken = localStorage.getItem("refresh") || null;
    if (!accessToken) {
        if (!refreshToken) {
            // contentContainer.innerHTML = "<h3>Authentication needed</h3>"
            return null
        }
    }
    productList()
}

isPreviousAuthenticated();

const searchClient = algoliasearch(
    'PD8GINBTDB',
    '5147ce3ac67e078d7d6a58e9167f0fb8'
)

const search = instantsearch({
  indexName: 'server_Book',
  searchClient,
});

search.addWidgets([
  instantsearch.widgets.searchBox({
    container: '#searchbox',
  }),

    instantsearch.widgets.clearRefinements({
    container: "#clear-refinements"
    }),


  instantsearch.widgets.refinementList({
      container: "#user-list",
      attribute: 'user'
  }),
  instantsearch.widgets.refinementList({
    container: "#public-list",
    attribute: 'public'
}),


  instantsearch.widgets.hits({
    container: '#hits',
    templates: {
        item: `
            <div>
                <div>{{#helpers.highlight}}{ "attribute": "title" }{{/helpers.highlight}}</div>
                <div>{{#helpers.highlight}}{ "attribute": "body" }{{/helpers.highlight}}</div>
                
                <p>{{ user }}</p><p>\${{ price }}
            
            </div>`
    }
  })
]);

search.start();