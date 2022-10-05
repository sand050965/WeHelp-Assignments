let windowMobile = window.matchMedia("(max-width: 600px)");
let windowPad = window.matchMedia("(max-width: 1200px)");
let items = document.getElementById("items");
let gridContainer = document.getElementById("grid-container");
let lisImg = document.querySelector(".list-img");
let titleGrid = document.querySelector(".title-grid");
let btn = document.querySelector(".btn");

// 側拉選單
let sideMenu = document.getElementById("side-menu");

// 點擊漢堡圖示開啟側拉選單
let openSideMenu = () => {
    let event = window.event;
    sideMenu.style.width = "250px";
    event.stopPropagation();
};

// 點擊漢堡圖示關閉側拉選單
let closeSideMenu = () => {
    if (sideMenu.style.width == "250px") {
        sideMenu.style.width = "0px";
    }
};

// 取得台北市政府提供景點公開資料並顯示在網頁畫面中
let cnt = 0;
let showCnt = 0;
let getData = () => {
    let src = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json";
    let promotionGrid = document.getElementById("promotion-grid");
    let titleGrid = document.getElementById("title-grid");
    fetch(src).then(function (response) {
        return response.json();
    }).then(function (data) {
        data.result.results.forEach(item => {
            // 取景點名
            let title = item.stitle;
            // 取圖片網址
            let imgSrc = "https" + item.file.split("https")[1];

            // 創建圖片div，並將圖片放置進去
            let emelmentImgContainer = document.createElement("div");
            let elementImg = document.createElement("img");
            elementImg.src = imgSrc;
            imgContainer = addImgCss(emelmentImgContainer, elementImg, cnt);// 設置img css屬性

            // 創建景點名div，並將景點名的值放置進去
            let elementText = document.createElement("div");
            let text = document.createTextNode(title);
            elementText.appendChild(text);
            elementText = addTextCss(elementText, cnt);//設置text css屬性

            // 創建圖片與景點名div容器，並將圖片與景點名放置進去
            let elementContentContainer = document.createElement("div");
            elementContentContainer = addContentCss(elementContentContainer, cnt);// 設置容器 css屬性
            elementContentContainer.appendChild(emelmentImgContainer);
            elementContentContainer.appendChild(elementText);

            if (cnt <= 1) {
                promotionGrid.appendChild(elementContentContainer);
            } else {
                titleGrid.appendChild(elementContentContainer);
            }
            cnt++;
        });
        mediaQuery();
    });
    showCnt += 10;
};

// 設置img css屬性
let addImgCss = (imgContainer, img, cnt) => {
    if (cnt <= 1) { // promotion區塊圖片的css
        img.className = "promotion-img";
        imgContainer.className = "promotion-img";
        return imgContainer.appendChild(img);
    } else { // title區塊圖片的css
        imgContainer.className = "title-img-container";
        img.className = "title-img";
        return imgContainer.appendChild(img);
    }
}

// 設置text css屬性
let addTextCss = (text, cnt) => {
    if (cnt <= 1) { // promotion區塊文字的css
        text.className = "promotion-text";
        return text;
    } else { // title區塊文字的css
        text.className = "title-text";
        return text;
    }
};


// 設置容器 css屬性
let addContentCss = (content, cnt) => {

    if (cnt <= 1) {//promotion
        content.id = "promotion" + cnt;
        content.style.display = "flex";
        content.style.gridColumn = (cnt * 2 + 1) + "/" + (cnt * 2 + 3);// 設定promotion的grid-column
        content.style.gridRow = "1/2";// 設定promotion的grid-row
    } else {
        content.id = "title" + cnt;
        content.style.gridColumn = ((cnt - 2) % 4 + 1) + "/" + ((cnt - 2) % 4 + 2);// 設定title的grid-column
        content.style.gridRow = (parseInt((cnt - 2) / 4) + 1) + "/" + (parseInt((cnt - 2) / 4) + 2);// 設定title的grid-row
        if (cnt >= 10) {
            content.style.display = "none"
        }
    }

    return content;
}

// 按鈕Load More功能，載入更多景點資訊
let loadMore = () => {
    for (let i = showCnt; i < showCnt + 8; i++) {
        document.getElementById("title" + i).style.display = "block";
        mediaQuery();
    }
    showCnt += 8;
    if (showCnt === cnt) {
        document.getElementById("button").style.display = "none";
    }
}

// 滑鼠移入按鈕
let over = (e) => {
    e.style.backgroundColor = "rgb(234, 231, 231)";
    
}

// 滑鼠移出按鈕
let out = (e) => {
    e.style.backgroundColor = "lightgrey";
}

// 滑鼠按下按鈕
let down = (e) => {
    e.style.fontWeight = "bold";
    btn.setAttribute("style", "outline: solid 5px; background-color: grey;");
}

// 滑鼠放開按鈕
let up = (e) => {
    e.style.fontWeight = "normal";
    btn.setAttribute("style", "outline: solid 3px;");
}



// 視窗寬度有變動，會調整css屬性
let mediaQuery = () => {

    if (windowMobile.matches) { // 300px < 螢幕解析度的寬度 <= 600px 

        gridContainer.style.width = "90%";

        // 調整grid網格大小按固定比例縮放
        titleGrid.setAttribute("style", "grid-auto-rows: calc(90vw * 3 / 4);");

        // 將item列表隱藏，並顯示漢堡圖
        items.children[0].setAttribute("style", "display: none;");
        items.children[1].setAttribute("style", "display: none;");
        items.children[2].setAttribute("style", "display: none;");
        items.children[3].setAttribute("style", "display: none;");
        lisImg.setAttribute("style", "display: block;");

        //  調整按鈕css屬性
        btn.style.paddingTop = "10px";
        btn.style.paddingBottom = "10px";
        btn.style.paddingLeft = "30px";
        btn.style.paddingRight = "30px";
        btn.style.fontSize = "15px";


        for (let i = 0; i < cnt; i++) {
            if (i <= 1) { // 計算promotion區塊的grid格線位置
                let ePromotion = document.getElementById("promotion" + i);
                ePromotion.style.gridColumn = "1/2";
                ePromotion.style.gridRow = (i + 1) + "/" + (i + 2);
            } else { // 計算title區塊的grid格線位置
                let eTitle = document.getElementById("title" + i);
                eTitle.style.gridArea = (i - 1) + "/" + 1 + "/" + i + "/" + 2;
            }
        }

    } else if (windowPad.matches) { // 600px < 螢幕解析度的寬度 <= 1200px

        gridContainer.style.width = "90%";

        // 調整grid網格大小按固定比例縮放
        titleGrid.setAttribute("style", "grid-auto-rows: calc(((90vw - 20px) / 2) * 3 / 4);");

        //  調整按鈕css屬性
        btn.style.paddingTop = "15px";
        btn.style.paddingBottom = "15px";
        btn.style.paddingLeft = "45px";
        btn.style.paddingRight = "45px";
        btn.style.fontSize = "15px";

        if (cnt < 2) {
            return;
        }

        for (let i = 2; i < cnt; i++) { // 計算title區塊的grid格線位置
            let eTitle = document.getElementById("title" + i);
            eTitle.style.gridColumn = ((i % 2) + 1) + "/" + ((i % 2) + 2);
            eTitle.style.gridRow = (parseInt(i / 2)) + "/" + (parseInt(i / 2 + 1));
        }

    } else { // 螢幕解析度的寬度 > 1200px
        gridContainer.style.width = "1200px";

        // 調整grid網格大小按固定比例縮放
        titleGrid.setAttribute("style", "grid-auto-rows: calc((1140px/4)*3/4)");

        //  調整按鈕css屬性
        btn.style.paddingTop = "20px";
        btn.style.paddingBottom = "20px";
        btn.style.paddingLeft = "60px";
        btn.style.paddingRight = "60px";
        btn.style.fontSize = "20px";

        for (let i = 0; i < cnt; i++) {
            if (i <= 1) { // 計算promotion區塊的grid格線位置
                let ePromotion = document.getElementById("promotion" + i);
                ePromotion.style.gridColumn = (i * 2 + 1) + "/" + (i * 2 + 3);
                ePromotion.style.gridRow = "1/2";
            } else { // 計算title區塊的grid格線位置
                let eTitle = document.getElementById("title" + i);
                eTitle.style.gridArea = (parseInt((i - 2) / 4) + 1) + "/" + ((i - 2) % 4 + 1) + "/" + (parseInt((i - 2) / 4) + 2) + "/" + ((i - 2) % 4 + 2);
            }
        }
    }
}

// 連線取得資料
getData();

// 動態調整Media Query
mediaQuery();

// 如果螢幕大小有變動，動態調整Media Query
windowMobile.addEventListener('change', mediaQuery);
windowPad.addEventListener('change', mediaQuery);