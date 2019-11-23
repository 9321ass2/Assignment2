

// import your own scripts here.



import login from './login.js';
import userpage from "./userpage.js"
import developerpage from "./gamedeveloperpage.js"
// your app must take an apiUrl as an argument --
// this will allow us to verify your apps behaviour with 
// different datasets.
function initApp(apiUrl) {
  // your app initialisation goes here
  	console.log(":1")
  	let thead = document.getElementById("thead");
  	
	let th1 = document.createElement("th");
  	th1.textContent="🔥";
  	thead.appendChild(th1);

  	let th2 = document.createElement("td");
  	th2.textContent="Name  ";
  	thead.appendChild(th2);

  	let th3 = document.createElement("td");
  	th3.textContent=" Platform  ";
  	thead.appendChild(th3);

  	let th4 = document.createElement("td");
  	th4.textContent=" Developer";
  	thead.appendChild(th4);

  	let th5 = document.createElement("td");
  	th5.textContent=" Rating";
  	thead.appendChild(th5);

  	let th6 = document.createElement("td");
  	th6.textContent=" Sales";
  	thead.appendChild(th6);

  	const api = apiUrl;
  	let details = {
				method: 'GET',
				headers: {
					'accept': 'application/json'
				}
	}
	//getPro.then(res => {res.json()})
	//getPro.then(res => {res.json()})
	let getPro = fetch(api + "/games/topsales", details);
	getPro.then(response => {
		if (response.status === 200) {
			let token = response.json();
			//console.log(token)
			let i = 1;
			token.then(data => {
				//console.log(data)
				for (let element of data) {
					//console.log(element)
					let row = document.getElementById("row" + i);

					let th = document.createElement("th");
					th.textContent = i;
					row.appendChild(th);

					for (let item in element) {
						if (item === "Identifier") {
							break;
						}
						let td = document.createElement("td");
						td.textContent = element[item];
						// console.log(td)
						row.appendChild(td);

					}
					i++;
				}
			})
		}
	})

	// let token = getPro.then(response => {
	// 	response.json()
	// });
	

	

    login(api)
    userpage(api)
	developerpage(api)

}

export default initApp;
