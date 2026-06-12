const http = require('http');
const fs = require('fs');
const path = require('path');
http.createServer((req, res) => {
  const f = path.join(__dirname, 'ame_no_owarini.html');
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  fs.createReadStream(f).pipe(res);
}).listen(8431, '127.0.0.1');
