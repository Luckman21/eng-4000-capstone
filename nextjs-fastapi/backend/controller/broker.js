const aedes = require('aedes')();
const net = require('net');
const server = net.createServer(aedes.handle);

server.listen(1883, function () {
  console.log('Aedes MQTT broker running on port 1883');
});

// 👇 Listen for published messages
aedes.on('publish', function (packet, client) {
  if (client) {
    console.log(`[${new Date().toISOString()}] Message received from client '${client.id}'`);
  } else {
    console.log(`[${new Date().toISOString()}] Message published by broker`);
  }

  console.log(`→ Topic: ${packet.topic}`);
  console.log(`→ Payload: ${packet.payload.toString()}`);
  console.log('---');
});