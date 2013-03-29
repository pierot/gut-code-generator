var http = require('http'),
    url = require('url'),
    _ = require('underscore'),
    meta = require('./package.json');

var port = process.argv[2] || 3001;

function range(start, limit) {
  var step = limit.charCodeAt(0) - start.charCodeAt(0) > 0 ? 1 : -1
  var result = [];

  while(start !== limit) {
    result.push(start)

    start = String.fromCharCode(start.charCodeAt(0) + step);
  }

  return result;
}

function random_alphanum(size) {
  var chars = range('a', 'z');
  chars = chars.concat(range('A', 'Z'));
  chars = chars.concat(range('0', '9'));

  chars = _.difference(chars, ['i', 'I', 'o', 'O', 'l', '1', '0']);

  var res = [];

  for(var i = 0; i < size; i++) {
    res.push(chars[_.random(chars.length - 1)]);
  }

  return res.join('');
}

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/plain'});

  var paths = url.parse(req.url).pathname.split('/').slice(1);
  var count = paths[0] || 100;
  var size = paths[1] || 5;

  console.log('Generating ' + count + ' codes of length ' + size);

  for(var i = 0; i < count; i++) {
    res.write(random_alphanum(size) + '\n');
  }

  res.end('\n');
}).listen(port, "127.0.0.1");

console.log(meta.name + ' running at http://127.0.0.1:' + port + '/');
