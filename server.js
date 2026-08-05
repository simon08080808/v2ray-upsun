const http = require('http');

const TARGET_HOST = 'simon.benbilal237free.xyz';
const TARGET_PORT = 80;
const PORT = process.env.PORT || 8080;

const server = http.createServer((req, res) => {
  // Transmettre tous les headers du client en remplaçant Host
  const headers = { ...req.headers, host: TARGET_HOST };

  const proxyReq = http.request(
    {
      hostname: TARGET_HOST,
      port: TARGET_PORT,
      path: req.url,
      method: req.method,
      headers: headers
    },
    (proxyRes) => {
      res.writeHead(proxyRes.statusCode, proxyRes.headers);
      proxyRes.pipe(res, { end: true });
    }
  );

  proxyReq.on('error', (err) => {
    res.writeHead(502, { 'Content-Type': 'text/plain' });
    res.end('Proxy Error');
  });

  // Streaming direct des paquets entrants
  req.pipe(proxyReq, { end: true });
});

// Gestion des upgrades WebSocket / HTTP2 Streams
server.on('upgrade', (req, socket, head) => {
  const headers = { ...req.headers, host: TARGET_HOST };

  const proxyReq = http.request({
    hostname: TARGET_HOST,
    port: TARGET_PORT,
    path: req.url,
    method: req.method,
    headers: headers
  });

  proxyReq.on('upgrade', (proxyRes, proxySocket, proxyHead) => {
    socket.write(
      `HTTP/${proxyRes.httpVersion} ${proxyRes.statusCode} ${proxyRes.statusMessage}\r\n` +
      Object.keys(proxyRes.headers).map(k => `${k}: ${proxyRes.headers[k]}`).join('\r\n') +
      '\r\n\r\n'
    );
    if (proxyHead && proxyHead.length) socket.write(proxyHead);
    proxySocket.pipe(socket);
    socket.pipe(proxySocket);
  });

  proxyReq.on('error', () => {
    socket.destroy();
  });

  if (head && head.length) proxyReq.write(head);
  req.pipe(proxyReq);
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Relay active on port ${PORT}`);
});
