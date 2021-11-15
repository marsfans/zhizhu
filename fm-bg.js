var ctx = null;
var img = null;
var cnt = 10;
var col = 0;

var mouse = [1,1];
var color = [];

document.onmousemove = function (e) {

    mouse[0] = e.pageX / 15;
    mouse[1] = e.pageY / -5;
}

function init() {

    img = document.getElementById('canvas');
    ctx = img.getContext('2d');

    window.setInterval(clock, 10);
}

function gradientColor() {

    var pos = (col++) & 127;

    if (pos == 0) {
        color[0] = {r:Math.random() * 255|0, g:Math.random() * 255|0, b:Math.random() * 255|0};
        color[1] = {r:Math.random() * 255|0, g:Math.random() * 255|0, b:Math.random() * 255|0};
    }

    return ['rgb(',
         ((color[0].r + ((color[1].r - color[0].r) / 128) * pos)|0), ',',
         ((color[0].g + ((color[1].g - color[0].g) / 128) * pos)|0), ',',
         ((color[0].b + ((color[1].b - color[0].b) / 128) * pos)|0), ')'].join('');
}

function clock() {

    var i = 44;
    ctx.fillRect(0, 0, 800, 450, ctx.drawImage(img, 10, 2, 780, 448, 0, 3, 800, 450), ctx.fillStyle='rgba(0, 0, 0, 0.01)');

    cnt+= 44;

    ctx.fillStyle = gradientColor();
    while (i--) {
        ctx.fillRect(i * 40 + 40 - mouse[0], 250 - mouse[1] +Math.sin(cnt + i + Math.sin(i) * Math.sin((cnt << 1) - (i >> 3))) * 50, 20, 1);
    }
}