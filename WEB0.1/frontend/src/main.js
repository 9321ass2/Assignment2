

// import your own scripts here.



import login from './login.js';
import userpage from "./userpage.js"
// your app must take an apiUrl as an argument --
// this will allow us to verify your apps behaviour with 
// different datasets.
function initApp(apiUrl) {
  // your app initialisation goes here
  	console.log(":1")
  	let thead = document.getElementById("thead");
  	
	let th1 = document.createElement("th");
  	th1.textContent="# ";
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
					'Content-Type': 'application/json'
				}
	}
	let getPro = fetch(api + "/Data/topsales", details);
	let token = getPro.then(response => response.json());
	let i=1;

	token.then(data => {
		console.log(":2")
		for(let element of data.top3){

			let row = document.getElementById("row"+i);
			
			let th = document.createElement("th");
			th.textContent=i;
			row.appendChild(th);
			console.log(row)
			for(let item of element){
				let td = document.createElement("td");
				td.textContent=item;
				console.log(td)
				row.appendChild(td);

			}
			i++;
		}
	})

    login(api)
    userpage(api)

}

export default initApp;
