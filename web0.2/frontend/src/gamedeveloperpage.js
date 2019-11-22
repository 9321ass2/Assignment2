
function developerpage(api) {

    let selction1 = document.getElementById("option_platform")
    let selction2 = document.getElementById("option_genre")
    let selction3 = document.getElementById("option_years")

    let selction4 = document.getElementById("option_platform2")
    let selction5 = document.getElementById("option_genre2")

    let selction6 = document.getElementById("option_platform3")
    let selction7 = document.getElementById("option_genre3")


    let input1 = document.getElementById("ip1")
    let input2 = document.getElementById("ip2")
    let input3 = document.getElementById("ip3")

    let input4 = document.getElementById("ipt1")
    let input5 = document.getElementById("ipt2")

    let platforms = ['Wii', 'NES', 'PC', 'GB', 'DS', 'X360', 'SNES', 'PS3', 'PS4',
        '3DS', 'PS2', 'GBA', 'NS', 'GEN',
        'N64', 'PS', 'XOne', 'WiiU', 'XB', 'PSP', '2600', 'GC', 'GBC', 'PSN', 'PSV', 'DC', 'SAT', 'SCD',
        'WS', 'XBL', 'Amig', 'VC', 'NG', 'WW', 'PCE', '3DO', 'GG', 'OSX', 'PCFX', 'Mob', 'And', 'Ouya', 'DSiW',
        'MS', 'DSi', 'VB', 'Linux', 'MSD', 'C128', 'AST', 'Lynx', '7800', '5200', 'S32X', 'MSX', 'FMT', 'ACPC',
        'C64', 'BRW', 'AJ', 'ZXS', 'NGage',
        'GIZ', 'WinP', 'iQue', 'iOS', 'Arc', 'ApII', 'Aco', 'BBCM', 'TG16', 'CDi', 'CD32', 'Int']
    let genres = ['Sports', 'Platform', 'Racing', 'Shooter', 'Role-Playing',
        'Puzzle', 'Misc', 'Party', 'Simulation', 'Action', 'Action-Adventure',
        'Fighting', 'Strategy', 'Adventure', 'Music', 'MMO', 'Sandbox',
        'Visual Novel', 'Board Game', 'Education']
    let years = [2020,2021,2022,2023,2024,2025,2026,2027,2028,2029,2030]

    for(let i of platforms){
        let option1 = document.createElement("option")
        let option2 = document.createElement("option")
        let option3 = document.createElement("option")
        option1.value = i
        option1.text = i
        option2.value = i
        option2.text = i
        option3.value = i
        option3.text = i

        selction1.appendChild(option1)
        selction4.appendChild(option2)
        selction6.appendChild(option3)

    }
    for(let i of genres){
        let option1 = document.createElement("option")
        let option2 = document.createElement("option")
        let option3 = document.createElement("option")
        option1.value = i
        option1.text = i
        option2.value = i
        option2.text = i
        option3.value = i
        option3.text = i

        selction2.appendChild(option1)
        selction5.appendChild(option2)
        selction7.appendChild(option3)
    }
    for(let i of years){
        let option = document.createElement("option")
        option.value = i
        option.text = i
        selction3.appendChild(option)
    }
    let pr1_bt = document.getElementById("pr1_bt")
    pr1_bt.onclick=function(){
        let details={
            method: 'GET',
            headers:{
                'accept': 'application/json',
                'AUTH-TOKEN':localStorage.getItem('current_token')
            }
        }
        const getPro = fetch(api+"/predict/linear?year="+selction3.value+"&platform="+selction6.value+"&genre="+selction7.value,details);
        getPro.then(response=>{
            if(response.status===200) {
                let p=response.json()
                p.then(data=>{
                    for(let i of data){
                        let text=document.getElementById("ss3")
                        text.textContent=" GAME :"+i.Name
                    }


                })

            }else{
                console.log("pr3 wrong")
            }
        })
    }

    let pr2_bt = document.getElementById("pr2_bt")
    let pre_string=input1.value+" "+input2.value+" "+input3.value+" "+selction4.value+" "+selction5.value
    pr2_bt.onclick=function(){
        let details2={
            method: 'GET',
            headers:{
                'accept': 'application/json',
                'AUTH-TOKEN':localStorage.getItem('current_token')
            }
        }
        const getPro = fetch(api+"/predict/esrb?game_information="+pre_string,details2);
        getPro.then(response=>{
            if(response.status===200) {
                let p=response.json()
                p.then(data=>{
                    let text=document.getElementById("ss2")
                    text.textContent="GAME ESRB:"+data.predict_ESRB
                    text.style.color="white"

                })
            }else{
                console.log("pr2 wrong")
            }
        })
    }

    let pr3_bt = document.getElementById("pr3_bt")
    pr3_bt.onclick=function(){
        let details={
            method: 'GET',
            headers:{
                'accept': 'application/json',
                'AUTH-TOKEN':localStorage.getItem('current_token')
            }
        }
        const getPro = fetch(api+"/games/topscores?top="+input4.value+"&year="+input5.value+"&platform="+selction6.value+"&genre="+selction7.value,details);
        getPro.then(response=>{
            if(response.status===200) {
                let p=response.json()
                p.then(data=>{
                    for(let i of data){

                        let text=document.getElementById("ss3")
                        text.textContent="GAME:"+i.Name
                    }

                })

            }else{
                console.log("pr1 wrong")
            }
        })
    }
    let details3={
        method: 'GET',
        headers:{
            'accept': 'application/json',
            'AUTH-TOKEN':localStorage.getItem('current_token')
        }
    }
    let a=document.getElementById("g_1")
    const getPro_1 = fetch(api+"/games/populargames",details3)
    getPro_1.then(response=>{
        if(response.status===200){
            let p=response.json()
            p.then(data=>{
                for(let i of data){
                    // console.log(i)
                    // console.log(i.Name)
                    let s=document.createElement("span")

                    s.textContent="🎮"+i.Name
                    s.classList.add("ss")
                    a.appendChild(s)
                }
            })
        }
    })









}
export default developerpage;