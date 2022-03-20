'use strict';

// Declare Variables
var remoteConnection;
var sendChannel;
var receiveChannel;
const dataChannelSend = document.querySelector('input#message');
const dataChannelReceive = document.querySelector('div#text_chat');
const sendButton = document.querySelector('button#send');
const closeButton = document.querySelector('button#disconnect');

// Bind Buttons to functions
//closeButton.onclick = closeDataChannels;
  // NOTE: sendMessage function + bind is located in message_channel.html

socket.on('Message', async function(message){
  if(message.from == username){return}
  console.log("Recieved Message: ", message);
  if (message.answer) {
      console.log("Got an answer");
      const remoteDesc = new RTCSessionDescription(message.answer);
      await remoteConnection.setRemoteDescription(remoteDesc);
  }
  else if (message.offer) {
      console.log("Got an offer");
      remoteConnection.setRemoteDescription(new RTCSessionDescription(message.offer));
      const answer = await remoteConnection.createAnswer();
      await remoteConnection.setLocalDescription(answer);
      socket.emit('Message', {'answer': answer, 'room':room_ID, 'from':username});
      console.log("Just sent answer");
  }
  else if (message.new_ice_candidate) {
    console.log("Ice Candidate passed");
      try {
          await remoteConnection.addIceCandidate(message.new_ice_candidate);
      } catch (e) {
          console.error('Error adding received ice candidate', e);
      }
  }
});


async function makeCall(){
  console.log("Initiating");
  const configuration = {'iceServers': [{'urls': 'stun:stun.l.google.com:19302'}]}
  remoteConnection = new RTCPeerConnection(configuration);
  sendChannel = remoteConnection.createDataChannel("from_" + username);
  setupListeners();
  if(initiator){
    console.log("Entering as initiator");

    const offer = await remoteConnection.createOffer();
    await remoteConnection.setLocalDescription(offer);
    socket.emit('Message', {'offer': offer, 'room':room_ID, 'from':username});
    console.log("Just sent offer");
  }
  else{
    console.log("Entering as reciever");
  }
  console.log("Finished making call");
}


function setupListeners(){
  // Setup for ICE Listening:
  // Listen for local ICE candidates on the local RTCPeerConnection
  remoteConnection.addEventListener('icecandidate', event => {
      if (event.candidate) {
        console.log("Found a local candidate");
        socket.emit('Message', {'new_ice_candidate': event.candidate, 'room':room_ID, 'from':username});
      }
  });

  remoteConnection.addEventListener('connectionstatechange', event => {
      if (remoteConnection.connectionState === 'connected') {
          console.log("We're connected!");
      }
  });

  remoteConnection.addEventListener('datachannel', event => {
    receiveChannel = event.channel;
    setupReceiveListeners();
  });

  // Enable textarea and button when opened
  sendChannel.addEventListener('open', event => {
      dataChannelSend.disabled = false;
      sendButton.disabled = false;
  });

  // Disable input when closed
  sendChannel.addEventListener('close', event => {
      dataChannelSend.disabled = true;
      sendButton.disabled = true;
  });

  console.log("setup listeners");
}

function setupReceiveListeners(){
  receiveChannel.addEventListener('message', event => {
    console.log("Recieved Message");
    var message = event.data;
    dataChannelReceive.innerHTML += target + ": " + message + "<br>";
  });
}

// Users Passing Messages:
function sendMessage(){
  console.log("Sending Message");
  var message = dataChannelSend.value;
  // Log message Locally + Send
  dataChannelReceive.innerHTML += username + ": " + message + "<br>";
  sendChannel.send(message);
  // QOL Stuff
  dataChannelReceive.scrollTop = dataChannelReceive.scrollHeight;
}
