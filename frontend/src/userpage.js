

function userpage(api){
    let rightbox=document.getElementById("rightbox");
    let chosebox=document.getElementById("like");
    let likeguess=document.getElementById("likeguess");

    let imggame=["https://upload.wikimedia.org/wikipedia/en/0/03/Super_Mario_Bros._box.png","https://upload.wikimedia.org/wikipedia/en/0/0a/Pokemonseason3DVDvol1.jpg","https://store-images.s-microsoft.com/image/apps.17382.13510798887677013.afcc99fc-bdcc-4b9c-8261-4b2cd93b8845.49beb011-7271-4f15-a78b-422c511871e4","https://c1-ebgames.eb-cdn.com.au/merchandising/images/packshots/73278a4c3e2145e1b56da1c4e0a52550_Large.png","https://images.g2a.com/newlayout/323x433/1x1x0/9fd25a2134bc/5bbb3191ae653a0e8d2bcf62","https://m.media-amazon.com/images/M/MV5BOTNiN2EzYmQtZjZjOS00MjZkLTkyYzQtY2Q2MzViNzVkMjJmXkEyXkFqcGdeQXVyOTk3NjY3NTM@._V1_.jpg","https://cdn.cdkeys.com/500x706/media/catalog/product/p/l/playerunknowns_battlegrounds_pugb_xbox_one_1.jpg","https://static.invenglobal.com/upload/image/2019/01/02/o1546463479317127.png","https://images-na.ssl-images-amazon.com/images/I/918y4X2gAwL._SL1500_.jpg","https://ubistatic19-a.akamaihd.net/marketingresource/en-gb/ubisoft/home/assets/images/moree3_upp_mobile_351278.jpg"]
    let gamenum=[5,2,1,4,5,2,3,1,1,6]
    let gamename=["Super Mario Bros.","New Super Mario Bros.","New Super Mario Bros. Wii","Super Mario World","Super Mario Odyssey","Pokemon Red / Green / Blue Version","Pokemon Gold / Silver Version","Just Dance 4","Wii Sports","Wii Sports Resort","Wii Fit","Wii Fit Plus","Grand Theft Auto V","World of Warcraft: Cataclysm","Super Smash Bros. Brawl","Red Dead Redemption 2","The Legend of Zelda: Ocarina of Time","Mario Kart Wii","Mario Kart DS","PlayerUnknown's Battlegrounds","Duck Hunt","Call of Duty: Black Ops 3","Tetris","Kinect Adventures!","Minecraft","Wii Play","Nintendogs","RollerCoaster Tycoon 3","Minecraft","Anno 2070"]
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

    submist_btn.onclick=function(){
        likeguess.style.display="block";
    }

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
            console.log(k)
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

                }


            }

        }


    }
}
export default userpage;