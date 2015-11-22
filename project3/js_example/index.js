var fileInput = document.getElementById('file-input');
var activate_button = document.getElementById('activate');

var string_to_number = function(elem) {
  return Number(elem);
};

var last_loaded_data = [];

var csv_reader = function(csv) {
  var rows = csv.split('\n');
  var by_mass = [];
  for(var i=0; i < rows.length; i++) {
    var row = rows[i].split(',').map(string_to_number);

    for(var j=0; j < row.length; j++) {
      if(by_mass[j] === undefined){
        by_mass[j] = [row[j]];
      } else {
        by_mass[j].push(row[j]);
      }
    }
  }
  return by_mass;
};

var fileSelectedEvent = function(e) {
  var files = e.target.files;

  var fileLoadEvt = function(file) {
    return function(e) {
      var csv = e.target.result;
      last_loaded_data = csv_reader(csv);
      return;
    };
  };

  for (var i=0, f = files[i]; i < files.length; i++) {
    var reader = new FileReader();
    reader.onload = fileLoadEvt(f);
    reader.readAsText(f);
  }
};

fileInput.addEventListener('change', fileSelectedEvent);

var build_generator = function(data) {
  return function*() {
    var i = 0;
    while(true) {
      var ret = [];
      for(var j=0; j < data.length; j++) {
        ret.push(data[j][i]+2); // offset
      }
      yield { vals: ret, frame: i };
      i++;
      if(i > data[0].length - 1) {
        i = 0;
      }
    }
  };
};

var plot_motion = function(data_generator) {
  var positions = data_generator.next().value.vals;
  var canvas_element = document.getElementById('canvas');
  var w = 100;
  canvas.width = w*positions.length+2*w;
  canvas.height = 2*w;

  var ctx = canvas_element.getContext('2d');

  var interval = setInterval(function() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var both = data_generator.next().value;
    positions = both.vals;
    var frame = both.frame;
    for(var i=0; i < positions.length; i++) {
      var pos = positions[i];
      ctx.fillRect(w+i*w+pos*5, 20, 20, 20);
      ctx.fillText("Frame " + frame, 0, 10);
    }
  }, 10);

  return;
};

var activatedEvent = function(e) {
  if(last_loaded_data === undefined || last_loaded_data === []) {
    return;
  }
  var data_gen = build_generator(last_loaded_data);
  plot_motion(data_gen());
  return;
};

activate_button.addEventListener('click', activatedEvent);
