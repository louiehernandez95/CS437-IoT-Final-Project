// /*
// I am using a backend server to interface to the raspberry pi,  where bluetooth connection/wifi connection exists
// */

document.onkeydown = updateKey;

var server_port = 5000;
var server_addr = "127.0.0.1";

// // Get Diagnostics every 5 seconds
setInterval(function () {

    readpower();
    readtemp();

}, 5000);

// // set type on onInit
document.addEventListener("DOMContentLoaded", function () {
    const button = document.getElementById("dispenserButton");

    button.onmousedown = function() {
        start();
    }

    button.onmouseup = function() {
        end();
    }

    const range = document.getElementById("strength");
    range.onmouseup = function(e) {
        adjust();
    }
});

var counter;

function start() {
    counter = setInterval(function() {
    rotate();
    }, 300);
  }

function end() {
    clearInterval(counter)
    stop();
}

function updateKey(e) {
    e = e || window.event;
    if (e.keyCode == '13') { // Enter
        rotate()
    }

    if (e.keyCode == '69') { // E
        // stop
        stop();
    }
}

function rotate() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", `http://${server_addr}:${server_port}/rotate`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
}

function stop() {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", `http://${server_addr}:${server_port}/stop`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send();
}

function adjust() {
    const rangeValue = document.getElementById("strength").value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", `http://${server_addr}:${server_port}/adjust`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({ power: rangeValue }));
}

function readtemp() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `http://${server_addr}:${server_port}/temp`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;
        if (this.status == 200) {
            var data = JSON.parse(this.responseText);
            document.getElementById("temp").innerHTML = data["temperature"];
        }
    }
    xhr.send();
}

function readpower() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", `http://${server_addr}:${server_port}/power`, true);
    xhr.setRequestHeader('Content-Type', 'application/json');

    xhr.onreadystatechange = function () {
        if (this.readyState != 4) return;
        if (this.status == 200) {
            var data = JSON.parse(this.responseText);
            document.getElementById("power").innerHTML = data["power"];
        }
    }
    xhr.send();
}