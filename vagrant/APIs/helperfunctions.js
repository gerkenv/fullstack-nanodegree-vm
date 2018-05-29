const fetch = require('node-fetch')

// GET /maps/api/geocode/json?address=Jakarta,Indonesia&amp;key=AIzaSyDkLj8d9d-lew69WuDWjoXTIKr06p9BNxE HTTP/1.1
// Host: maps.googleapis.com
// Cache-Control: no-cache
// Postman-Token: f8dd2f82-5fbb-92ca-05bb-e5254c2e5af3

function simpleFetch(method, url, data) {
  // Default options are marked with *
  return fetch(url, {
    //body: JSON.stringify(data), // must match 'Content-Type' header
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, same-origin, *omit
    headers: {
      'user-agent': 'Mozilla/4.0 MDN Example',
      'content-type': 'application/json'
    },
    method: method, // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, cors, *same-origin
    redirect: 'follow', // manual, *follow, error
    referrer: 'no-referrer', // *client, no-referrer
  })
  .then(response => {
    console.log(response);
    return response.json();
  }) // parses response to JSON
};

// simpleFetch('GET', 'http://127.0.0.1:5000/readHello', {})
simpleFetch('GET', 'http://www.google.com', {})
.then(response => console.log(response))
.catch(error => console.log(error));