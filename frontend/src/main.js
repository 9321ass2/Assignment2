

// import your own scripts here.



import login from './login.js';
// your app must take an apiUrl as an argument --
// this will allow us to verify your apps behaviour with 
// different datasets.
function initApp(apiUrl) {
  // your app initialisation goes here
    const api = apiUrl;
    login(api)

}

export default initApp;
