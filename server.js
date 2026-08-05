const net = require('net');

const TARGET_HOST = 'simon.benbilal237free.xyz';
const TARGET_PORT = 80;
const PORT = process.env.PORT || 8080;

const server = net.createServer((clientSocket) => {
  const targetSocket = net.connect(TARGET_PORT, TARGET_HOST, () => {
    clientSocket.pipe(targetSocket);
    targetSocket.pipe(clientSocket);
  });

  clientSocket.on('error', () => targetSocket.destroy());
  targetSocket.on('error', () => clientSocket.destroy());
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`TCP Relay running on port ${PORT}`);
});
