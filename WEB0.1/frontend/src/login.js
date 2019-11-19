

function login(api){
	let login_button=document.getElementById("login")
	let signup_button=document.getElementById("signup")
	let page=document.getElementById("page-content")
	let login_page=document.getElementById("login-page")
	let user_page=document.getElementById("user-page")
	let gamer_photo=document.getElementById("gamer_photo")
    let user="";
    let current_token="";

//login&signup -page
	let container = document.createElement('DIV');
	container.classList.add('container');
	login_page.appendChild(container);
	let row = document.createElement('DIV');
	row.classList.add('row');
	container.appendChild(row);
	let colMdOffset3 = document.createElement('DIV');
	colMdOffset3.classList.add('col-md-offset-3');
	colMdOffset3.classList.add('col-md-6');
	row.appendChild(colMdOffset3);
	let formHorizontal = document.createElement('FORM');
	formHorizontal.classList.add('form-horizontal');
	colMdOffset3.appendChild(formHorizontal);
	let heading = document.createElement('SPAN');
	heading.classList.add('heading');
	formHorizontal.appendChild(heading);
	heading.textContent = 'LOGIN';
	let formGroup = document.createElement('DIV');
	formGroup.classList.add('form-group');
	formHorizontal.appendChild(formGroup);
	let inputEmail3 = document.createElement('INPUT');
	inputEmail3.type = 'email';
	inputEmail3.classList.add('form-control');
	inputEmail3.id = 'inputEmail3';
	inputEmail3.placeholder = 'Username';
	formGroup.appendChild(inputEmail3);
	let fa = document.createElement('I');
	fa.classList.add('fa');
	fa.classList.add('fa-user');
	formGroup.appendChild(fa);
	let help = document.createElement('DIV');
	help.classList.add('form-group');
	help.classList.add('help');
	formHorizontal.appendChild(help);
	let inputPassword3 = document.createElement('INPUT');
	inputPassword3.type = 'password';
	inputPassword3.classList.add('form-control');
	inputPassword3.id = 'inputPassword3';
	inputPassword3.placeholder = 'Password';
	help.appendChild(inputPassword3);
	let faLock = document.createElement('I');
	faLock.classList.add('fa');
	faLock.classList.add('fa-lock');
	help.appendChild(faLock);
	let faQuestionCircle = document.createElement('A');
	faQuestionCircle.href = '#';
	faQuestionCircle.classList.add('fa');
	faQuestionCircle.classList.add('fa-question-circle');
	help.appendChild(faQuestionCircle);
	let formGroup1 = document.createElement('DIV');
	formGroup1.classList.add('form-group');
	formHorizontal.appendChild(formGroup1);
	let mainCheckbox = document.createElement('DIV');
	mainCheckbox.classList.add('main-checkbox');
	formGroup1.appendChild(mainCheckbox);
	let checkbox1 = document.createElement('INPUT');
	checkbox1.type = 'checkbox';
	checkbox1.value = 'None';
	checkbox1.id = 'checkbox1';
	checkbox1.name = 'check';
	mainCheckbox.appendChild(checkbox1);
	let nodeName1 = document.createElement('LABEL');
	nodeName1.for = 'checkbox1';
	mainCheckbox.appendChild(nodeName1);
	let text = document.createElement('SPAN');
	text.classList.add('text');
	formGroup1.appendChild(text);
	text.textContent = 'Remember me';
	let btn = document.createElement('BUTTON');
	btn.type = 'submit';
	btn.classList.add('btn');
	btn.classList.add('btn-default');
	formGroup1.appendChild(btn);
	btn.textContent = 'LOGIN';
	let btn2 = document.createElement('BUTTON');
	btn2.type = 'submit';
	btn2.classList.add('btn');
	btn2.classList.add('btn-default');
	formGroup1.appendChild(btn2);
	btn2.textContent = 'SIGNUP';

//signup page
	signup_button.onclick=function(){
		console.log("signup")
		page.style.display = "none"
		user_page.style.display="none"
		login_page.style.display = "block"
		btn.style.display="none"
		btn2.style.display="block"
		heading.textContent = 'SIGNUP';
		btn2.onclick=function(){
			let username=inputEmail3.value;
			let password=inputPassword3.value;

			const details = {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({"username": username, "password": password, "email": "COMP9321@unsw.com", "role": 1})
			}
			const getPro1 = fetch(api + "/Authen/register", details);
			let token = getPro1.then(response => response.json());
			token.then(data => {
					console.log(data);
					if (data.hasOwnProperty("Status")) {
						alert("signup Success!");
						console.log("signup success");
						login_button.click();

					} else {
						alert("Input message is wrong!");
						console.log("signup filed");
					}
				}
			)
		}
	}
//signup page

//login  page
	login_button.onclick=function(){
		console.log("login")
		page.style.display = "none"
		user_page.style.display="none"
		login_page.style.display = "block"
		btn2.style.display="none"
		btn.style.display="block"
		heading.textContent = 'LOGIN';
		btn.onclick=function(){
			let username=inputEmail3.value;
			let password=inputPassword3.value;
			localStorage.setItem('current_username',username)
			//localStorage.setItem('current_token',current_token)
			//processing
			const details = {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
					'username': username,
					'password': password
				}
			}
			const getPro2 = fetch(api + "/Authen/token", details);
			let token = getPro2.then(response => response.json());
			token.then(data => {
					console.log(data);
					if (data.hasOwnProperty("token")) {
                        user=username;
                        current_token=data.token;
                        localStorage.setItem('current_username',username);
                        localStorage.setItem('current_token',current_token);
						console.log(localStorage.getItem('current_username'));
    					console.log(localStorage.getItem('current_token'));
						alert("Success!");
						console.log("Login success");
						login_page.style.display="none"
						user_page.style.display="block"
						login_button.style.display="none"
						signup_button.style.display="none"
						gamer_photo.style.display="block"

					} else {
						alert("Input message is wrong!");
						console.log("LOGIN filed");
					}
				}
			)
		}
	}
	//arr=[user,current_token]

}
//login  page
export default login;
