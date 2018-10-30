
// let ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
//
// let chatSocket = new WebSocket( ws_scheme + '://' + window.location.host +'/'+ ws_scheme +'/user/' + roomName + '/');
//
// chatSocket.onmessage = function(e) {
//     let data = JSON.parse(e.data);
//     let message = data['message'];
// };
//
// chatSocket.onclose = function(e) {
//     console.error('Chat socket closed unexpectedly');
// };
var goEasy = new GoEasy({
		appkey: 'BS-106b3947c7304a238d8b5ef8105f1cd0'
	});