

// import your app here
import initApp from './main.js';

//const API_URL = 'http://127.0.0.1:5000';
//localhost：5000
//let hostname = window.location.hostname;
//const API_URL = hostname;
// comment above line and uncomment below line when when you start using the back-end server
import API_URL from './backend_url.js';

// and run it
initApp(API_URL);
//initApp();