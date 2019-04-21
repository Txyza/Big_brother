function funcRoomID(roomID) {
    switch (roomID) {
        case "peregovorka":
            el = document.getElementById("peregovorka");
            el.color = "red";
            var rect = el.getBoundingClientRect();
            console.log(rect)
        case "lobby":
            break;
        case "kitchen":
            break;
    }
}

function getUsers() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}
