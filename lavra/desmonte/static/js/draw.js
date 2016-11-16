function process() {
  // Change button name for canvas drawing mode
  this.setAttribute("value", "Clear");

  // Calculate drawing variables
  var prod = document.getElementById('id_producao').value; 
  var dens = document.getElementById('id_densidade').value; 
  var freq = document.getElementById('id_frequencia').value; 
  var turno = document.getElementById('id_turno').value; 
  var rcu = document.getElementById('id_rcu').value; 
  var inclinacao = document.getElementById('id_inclinacao').value; 
  var p1 = document.getElementById('id_p1').value; 
  var p2 = document.getElementById('id_p2').value; 
  var vfogo = prod / (52 * dens * freq);
  var pmh = vfogo / (7 * turno);
  var d = selectDiameter(rcu, pmh);
  var h = selectHeight(d);
  var [b, s, t, j, lf] = selectGeom(rcu, d);
  var l = h / Math.cos(inclinacao * Math.PI / 90) + (1 - inclinacao / 100) * j;
  var vr = b * s * h;
  var n = vfogo / vr;

  // Initialize drawing process
  var canvas = document.getElementById("canvas");
  canvas.setAttribute("width", 600);
  canvas.setAttribute("height", 300);
  // var canvas = document.getElementById('canvas');
  var ctx = canvas.getContext('2d');

  ctx.fillStyle = '#f0f0f0';
  ctx.fillRect(0, 0, 600, 300);
  
  ctx.fillCircle = function (x, y, radius, fillColor) {
    this.fillStyle = fillColor;
    this.beginPath();
    this.moveTo(x, y);
    this.arc(x, y, radius, 0, Math.PI * 2, false);
    this.fill();
  };

  canvas.onmousemove = function(e) {
    var x = e.pageX - this.offsetLeft;
    var y = e.pageY - this.offsetTop;

    var div = document.getElementById('coords');
    div.innerHTML = "x: " + x + " y: " + y;

    if (this.isDrawing) {

      var radius = 2;
      var fillColor = 'black';
      ctx.fillCircle(x, y, radius, fillColor);
    }
  };

  canvas.onmousedown = function(e) {
    this.isDrawing = true;
  };

  canvas.onmouseup = function(e) {
    this.isDrawing = false;
  };

  canvas.onmouseout = function(e) {
    this.isDrawing = false;
  }

}

function selectDiameter(rcu, pmh) {
  var ds = [65, 89, 150];
  if (rcu < 120) {
    var rcus = [190, 250, 550];
  } else {
    var rcus = [60, 110, 270];
  }

  var pair = {}; for (i = 0; i < rcus.length; i++) {
    pair[rcus[i]] = ds[i];
  }

  var calc = {};
  for (var key in pair) { calc[Math.abs(key-pmh)] = key
  }

  var min = 1000;
  var result = 0;
  for (var key in calc) {
    if (key < min) {
      min = key;
      result = calc[min];
    }
  }

  return pair[result];
}

function selectHeight(d) {
  if (d > 64 && d < 90) {
    return 9;
  } else {
    return 12.5;
  }
}

function selectGeom(rcu, d) {
  if (rcu <= 70) {
    var geom = [39, 51, 35, 10, 30];
  } else if (rcu > 70 && rcu <= 120) {
    var geom = [37, 47, 34, 11, 35];
  } else if (rcu >= 120 && rcu <= 180) {
    var geom = [35, 43, 32, 12, 40];
  } else if (rcu > 180) {
    var geom = [33, 38, 30, 12, 46];
  }

  var result = [];
  for (i = 0; i < geom.length; i++) {
    result.push(geom[i] * d / 1000);
  }

  return result;
}
