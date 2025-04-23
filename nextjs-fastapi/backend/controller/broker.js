const aedes = require('aedes')();
const net = require('net');
const server = net.createServer(aedes.handle);

server.listen(1883, '0.0.0.0', () => {
  console.log('Aedes MQTT broker running on port 1883 and accessible externally');
});


aedes.on('client', client => {
  console.log(`[BROKER] Client connected: ${client.id}`);
});

aedes.on('subscribe', (subscriptions, client) => {
  console.log(`[BROKER] ${client.id} subscribed to:`, subscriptions.map(s => s.topic));
});

aedes.on('publish', (packet, client) => {
  if (client) {
    console.log(`[BROKER] ${client.id} published to ${packet.topic}: ${packet.payload.toString()}`);
  }
});