// MQTT connection parameters
var hostname = 'test.mosquitto.org'; // Could be changed to localhost if 
var port = 8080;
//var hostname = window.location.hostname;
//var port = 9001;
var command_topic = "/rtmsg/d25638bb-17c2-46ac-b26e-ce1f67268088/commands";
var sensor_topic = "/rtmsg/d25638bb-17c2-46ac-b26e-ce1f67268088/sensors";
var qos = 0;


function generateUUID()
{
    //var d = new Date().getTime();
    var d = Date.now()
    if(window.performance && typeof window.performance.now === "function")
    {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
	    var r = (d + Math.random()*16)%16 | 0;
	    d = Math.floor(d/16);
	    return (c=='x' ? r : (r&0x3|0x8)).toString(16);
	});
    return uuid;
}


function subscribe(client, topic, qos)
{
    console.info('Subscribing to: Topic: ', topic, '. QoS: ', qos);
    client.subscribe(topic, {qos: Number(qos)});
}


// called when the client connects
function onConnect(context)
{
    var ctx = context.invocationContext;
    // Once a connection has been made, make a subscription and send a message.
    console.info("Client Connected. Context:");
    console.info(context);
    var statusSpan = document.getElementById("connectionstatus");
    statusSpan.innerHTML = "Connected to: " + ctx.host
	                   + ':' + ctx.port
	                   + ' with client ID ' + ctx.clientId;

    // Subscribe to notifications
    subscribe(ctx.client, ctx.topic, ctx.qos);
    subscribe(ctx.client, sensor_topic + "/camera1", ctx.qos);
}


// called when the client loses its connection
function onConnectionLost(responseObject)
{
    if (responseObject.errorCode !== 0)
    {
	console.info("Connection Lost: " + responseObject.errorMessage);
	var statusSpan = document.getElementById("connectionstatus");
	statusSpan.innerHTML = "Connection lost";
    }
}


function connect(subscribe_topic, qos)
{
    var clientId = generateUUID();

    console.info('Connecting to topic:', subscribe_topic);
    console.info('Connecting to Server: Hostname: ', hostname, '. Port: ', port, '. Client ID: ', clientId);
    client = new Paho.MQTT.Client(hostname, Number(port), clientId);
    // set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // connect the client
    client.connect({onSuccess:onConnect,
		invocationContext: {host : hostname, 
                                    port: port, 
                                    clientId: clientId, 
                                    topic: subscribe_topic, 
                                    qos: qos, 
                                    client: client}
	});
    var statusSpan = document.getElementById("connectionstatus");
    statusSpan.innerHTML = 'Connecting...';

    return client;
}


function publish(client, message, topic, qos)
{
    if(message == undefined || !message)
	return;

    //console.info('Publishing Message: Topic: ', topic, '. QoS: ' + qos + '. Message: ', message);
    message = new Paho.MQTT.Message(message);
    message.destinationName = topic;
    message.qos = Number(qos);
    client.send(message);
}


function decodeArrayBuffer(buffer)
{
    var mime;
    var a = new Uint8Array(buffer);
    var nb = a.length;
        
    if (nb < 4)
        return null;
        
    var b0 = a[0];
    var b1 = a[1];
    var b2 = a[2];
    var b3 = a[3];
    if (b0 == 0x89 && b1 == 0x50 && b2 == 0x4E && b3 == 0x47)
        mime = 'image/png';
    else if (b0 == 0xff && b1 == 0xd8)
        mime = 'image/jpeg';
    else if (b0 == 0x47 && b1 == 0x49 && b2 == 0x46)
        mime = 'image/gif';
    else
        return null;
        
    var binary = "";
    for (var i = 0; i < nb; i++)
        binary += String.fromCharCode(a[i]);
    var base64 = window.btoa(binary);
    return 'data:' + mime + ';base64,' + base64;
}
