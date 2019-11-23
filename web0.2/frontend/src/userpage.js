
//current_username,current_token
function userpage(api){
    let rightbox=document.getElementById("rightbox");
    let chosebox=document.getElementById("like");
    let likeguess=document.getElementById("likeguess");
    console.log(localStorage.getItem('current_username'));
    console.log(localStorage.getItem('current_token'));


    let imggame=["https://upload.wikimedia.org/wikipedia/en/0/03/Super_Mario_Bros._box.png","https://upload.wikimedia.org/wikipedia/en/0/0a/Pokemonseason3DVDvol1.jpg","https://store-images.s-microsoft.com/image/apps.17382.13510798887677013.afcc99fc-bdcc-4b9c-8261-4b2cd93b8845.49beb011-7271-4f15-a78b-422c511871e4","https://c1-ebgames.eb-cdn.com.au/merchandising/images/packshots/73278a4c3e2145e1b56da1c4e0a52550_Large.png","https://images.g2a.com/newlayout/323x433/1x1x0/9fd25a2134bc/5bbb3191ae653a0e8d2bcf62","https://m.media-amazon.com/images/M/MV5BOTNiN2EzYmQtZjZjOS00MjZkLTkyYzQtY2Q2MzViNzVkMjJmXkEyXkFqcGdeQXVyOTk3NjY3NTM@._V1_.jpg","https://cdn.cdkeys.com/500x706/media/catalog/product/p/l/playerunknowns_battlegrounds_pugb_xbox_one_1.jpg","https://static.invenglobal.com/upload/image/2019/01/02/o1546463479317127.png","https://images-na.ssl-images-amazon.com/images/I/918y4X2gAwL._SL1500_.jpg","https://ubistatic19-a.akamaihd.net/marketingresource/en-gb/ubisoft/home/assets/images/moree3_upp_mobile_351278.jpg"]
    let gamenum=[5,2,1,4,5,2,3,1,1,6]
    let gamename=["Super Mario Bros.","New Super Mario Bros.","New Super Mario Bros. Wii","Super Mario World","Super Mario Odyssey","Pokemon Red / Green / Blue Version","Pokemon Gold / Silver Version","Just Dance 4","Wii Sports","Wii Sports Resort","Wii Fit","Wii Fit Plus","Grand Theft Auto V","World of Warcraft: Cataclysm","Super Smash Bros. Brawl","Red Dead Redemption 2","The Legend of Zelda: Ocarina of Time","Mario Kart Wii","Mario Kart DS","PlayerUnknown's Battlegrounds","Duck Hunt","Call of Duty: Black Ops 3","Tetris","Kinect Adventures!","Minecraft","Wii Play","Nintendogs","RollerCoaster Tycoon 3","Minecraft","Anno 2070"]
    let gameid={"Super Mario Bros.":"2","New Super Mario Bros.":"7","New Super Mario Bros. Wii":"9","Super Mario World":"19","Super Mario Odyssey":"49","Pokemon Red / Green / Blue Version":"6","Pokemon Gold / Silver Version":"16","Just Dance 4":"146","Wii Sports":"1","Wii Sports Resort":"5","Wii Fit":"17","Wii Fit Plus":"18","Grand Theft Auto V":"20","World of Warcraft: Cataclysm":"283","Super Smash Bros. Brawl":"53","Red Dead Redemption 2":"46","The Legend of Zelda: Ocarina of Time":"128","Mario Kart Wii":"3","Mario Kart DS":"15","PlayerUnknown's Battlegrounds":"4","Duck Hunt":"11","Call of Duty: Black Ops 3":"35","Tetris":"8","Kinect Adventures!":"13","Minecraft":"10","Wii Play":"12","Nintendogs":"14","RollerCoaster Tycoon 3":"87","Anno 2070":"1617"}

    let preference=[];
    function removeAllChild(ele) {

        while (ele.hasChildNodes())
        {
            ele.removeChild(ele.firstChild);
        }
    }
    let submist_btn=document.createElement("button");
    submist_btn.textContent="submit"
    submist_btn.classList.add("button-primary");
    submist_btn.style.float='left';
    chosebox.appendChild(submist_btn);



    // let rightcontent=document.createElement('div');
    // rightcontent.id="rightcontent";
    // rightcontent.classList.add('rightcontent');
    // rightbox.appendChild(rightcontent);

    for(let i=1;i<11;i++){
        let btl=document.getElementById("gamegenre"+i);
        btl.onclick=function(){
            removeAllChild(rightbox);
            let leftcontent=document.createElement('div');
            //leftcontent.style.display="none"
            leftcontent.id="leftcontent"+i
            leftcontent.classList.add('leftcontent');
            let img=document.createElement('img');
            img.src=imggame[i-1]
            img.classList.add("genre_img");
            leftcontent.appendChild(img);
            rightbox.appendChild(leftcontent);

            let middlecontent=document.createElement('div');
            middlecontent.id="middlecontent"+i;
            middlecontent.classList.add('middlecontent');
            rightbox.appendChild(middlecontent);


            let k=0;
            if(i>1){
                for(let w=1;w<i;w++) {
                    k+=gamenum[w-1];
                }
            }
            //console.log(k)
            for(let j=1;j<=gamenum[i-1];j++){
                let btn_label = document.createElement('button')
                btn_label.textContent=gamename[k];
                btn_label.classList.add('btn_label');
                let btn_label2 = document.createElement('button')
                btn_label2.textContent=gamename[k];
                btn_label2.classList.add('btn_label2');
                btn_label2.style.display='none';
                chosebox.appendChild(btn_label2);
                k++;

                middlecontent.appendChild(btn_label);
                btn_label.onclick=function(){
                    btn_label.style.display='none';
                    btn_label2.style.display='block';
                    console.log(gameid[btn_label2.textContent]);
                    preference.push(gameid[btn_label2.textContent]);
                    console.log(preference);
                }


            }

        }


    }
    
    submist_btn.onclick=function(){

        
        let details = {
                method: 'POST',
                headers: {
                    'accept': 'application/json',
                    'Content-Type':'application/json',
                    'AUTH-TOKEN':localStorage.getItem('current_token')
                },
                body: JSON.stringify({"username": localStorage.getItem('current_username'), "preference": preference})
        }
        const getPro3 = fetch(api + "/recommends", details);

        let token = getPro3.then(response => {
            if(response.status === 200) {
                console.log("choose success")
                let details2={
                    method: 'GET',
                    headers:{
                        'accept': 'application/json',
                        'Content-Type':'application/json',
                        'AUTH-TOKEN':localStorage.getItem('current_token')
                    }
                }
                const getPro4 = fetch(api+"/recommends/"+localStorage.getItem('current_username'),details2);
                getPro4.then(response=>{
                    if(response.status===200){
                        let token = response.json();
                        token.then(data=>{
                            console.log(data)
                            let game_recommendation = document.getElementById('game_recommendation');
                            for(let item of data.recommendation){
                                let button_g = document.createElement("button");
                                button_g.textContent=item;
                                console.log(item);
                                button_g.classList.add('btn_label2');
                                button_g.style.setProperty('background-color', '#70D6DB');
                                button_g.style.setProperty('color', 'black');
                                button_g.style.setProperty('border-color', '#FCC11D');
                                game_recommendation.appendChild(button_g);

                            }
                            likeguess.style.display="block";
                        })
                    }
                })

            }else if(response.status === 400){
                alert("You should choose more than 3 games")

            }else if(response.status === 403){
                let detailsx = {
                    method: 'PUT',
                    headers: {
                        'accept': 'application/json',
                        'Content-Type':'application/json',
                        'AUTH-TOKEN':localStorage.getItem('current_token')
                    },
                    body: JSON.stringify({"preference": preference})
                }
                const getProx = fetch(api + "/recommends/"+localStorage.getItem('current_username'), detailsx);
                getProx.then(response=>{
                    if(response.status === 200){
                        console.log("update success")
                        let details_={
                            method: 'GET',
                            headers:{
                                'accept': 'application/json',
                                'Content-Type':'application/json',
                                'AUTH-TOKEN':localStorage.getItem('current_token')
                            }
                        }
                        const getPro_ = fetch(api+"/recommends/"+localStorage.getItem('current_username'),details_);
                        getPro_.then(response=> {
                            if (response.status === 200) {
                                let token = response.json();
                                token.then(data => {
                                    console.log(data)
                                    let game_recommendation = document.getElementById('game_recommendation');
                                    for (let item of data.recommendation) {
                                        let button_g = document.createElement("button");
                                        button_g.textContent = item;
                                        console.log(item);
                                        button_g.classList.add('btn_label2');
                                        button_g.style.setProperty('background-color', '#70D6DB');
                                        button_g.style.setProperty('color', 'black');
                                        button_g.style.setProperty('border-color', '#FCC11D');
                                        game_recommendation.appendChild(button_g);

                                    }
                                    likeguess.style.display = "block";
                                })
                            }
                        })
                    }else if(response.status === 400){
                        alert("You should choose more than 3 games")
                    }else{
                        alert("input wrong")
                    }
                })
            }else{
                alert("input wrong")
            }
        });

    }
}
export default userpage;
