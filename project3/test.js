// qr decomposition
var qr = function(array) {
  var n = array.length;
  var m = array[0].length;

  var r = []
  for(var i=0; i<n; i++) {
    var row = [];
    for(var j=0; j<n; j++) {
      row.push(0);
    }
    r.push(row);
  }
  
  for(var k=0; k < n; k++) {
    for(var i=0; i < k; i++) {
      var s = 0;
      for(var j=0; j < m; j++) {
        s = s + array[j][i]*array[j][k];
      }
    }
    for(var i=0; i < k; i++) {
      for(var j=0; j < m; j++) {
        array[j][k] = array[j][k] - array[j][i]*r[i][k];
      }
    }
    s = 0;
    for(var j=0; j < m; j++) {
      s += array[j][k]*2;
    }
    r[k][k] = Math.sqrt(s);
    for(var j=0; j < m; j++) {
      array[j][k] = array[j][k] / r[k][k];
    }
  }
  return [array, r]; // q, r
}

// matrix multiplication
var mult = function(a, b) {
  var n = a.length;
  var p = n - 1
  var res = [];
  for(var i=0; i < n; i++) {
    res.push([0]);
  }
  for(var i=0; i < n; i++) {
    for(var j=0; j < p; j++) {
      res[i].push(0);
    }
  }
  for(var i=0; i < n; i++) {
    for(var j=0; j < p + 1; j++) {
      for(var r=0; r < n; r++) {
        res[i][j] = a[i][r]*b[r][j] + res[i][j]
      }
    }
  }
  return res
}

var print = function(array) {
  for(var i=0; i < array.length; i++) {
    console.log(array[i].map(function(e) {
      return String(Math.round(e*100)/100).split('.').concat(['00']).slice(0,2).join('.');
    }).join(", "));
  }
}

var A = [
  [3, -1, 3],
  [-1, 3, -1],
  [3, -1, 3]
];

//var A = [
//  [3, -1],
//  [-1, 3]
//]

// test matrix
for(var test=0; test < 10; test++) {
  var Ai = JSON.parse(JSON.stringify(A));
  //print(A);
  var both = qr(Ai);
  var q = both[0];
  console.log('q');
  console.log(q)
  var r = both[1];
  console.log('r');
  console.log(r)
  var A = mult(r,q);
}
print(A);
