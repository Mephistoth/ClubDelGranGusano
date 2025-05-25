// static/videollamada/webrtc.js

console.log("✅ Archivo webrtc.js cargado y ejecutándose");

const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');

let localStream;
let peerConnection;

// Obtener nombre de sala desde URL
const pathParts = window.location.pathname.split('/').filter(Boolean);
const roomName = pathParts[pathParts.length - 1];

let ws;  // ✅ Declara 'ws' aquí, fuera del if

if (!roomName) {
    console.error("❌ No se pudo obtener el nombre de la sala");
} else {
    console.log("🔵 Conectando a sala:", roomName);

    // ✅ Inicializamos 'ws' dentro del else
    ws = new WebSocket(`ws://localhost:8000/ws/videollamada/${roomName}/`);

    ws.onopen = () => {
        console.log("🟢 Conexión WebSocket establecida");
    };

    // Manejo de errores WebSocket
    ws.onerror = (error) => {
        console.error("🔴 Error en WebSocket:", error);
    };

    // Acceso a medios locales
    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
            console.log("🎥 Acceso a medios concedido");
            localVideo.srcObject = stream;
            localStream = stream;

            // Llamamos a createPeerConnection después de tener 'ws'
            createPeerConnection(stream);
        })
        .catch(err => {
            console.error("🚫 Error accediendo a medios:", err);
        });
}

async function createPeerConnection(localStream) {
    const configuration = {
        iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
    };
    
    peerConnection = new RTCPeerConnection(configuration);

    // Agregar tus propios tracks
    localStream.getTracks().forEach(track => {
        peerConnection.addTrack(track, localStream);
    });

    // ✅ Ahora sí puedes usar 'ws', porque está en el scope global
    peerConnection.onicecandidate = event => {
        if (event.candidate) {
            console.log("📡 Enviando candidato ICE:", event.candidate);
            ws.send(JSON.stringify({
                type: "candidate",
                candidate: event.candidate,
            }));
        }
    };

    // Recibir track remoto
    peerConnection.ontrack = event => {
        console.log("📥 Track remoto recibido:", event.streams[0]);
        remoteVideo.srcObject = event.streams[0];
    };

    // Señalización WebRTC por WebSocket
    ws.onmessage = async function(event) {
        const message = JSON.parse(event.data);
        console.log("📩 Mensaje recibido:", message.type);

        try {
            if (message.type === 'offer') {
                console.log("📩 Recibido offer");

                if (peerConnection.signalingState !== 'stable') {
                    console.warn("⚠️ Estado no estable, saltando offer");
                    return;
                }

                await peerConnection.setRemoteDescription(new RTCSessionDescription(message));
                const answer = await peerConnection.createAnswer();
                await peerConnection.setLocalDescription(answer);
                ws.send(JSON.stringify(answer));

            } else if (message.type === 'answer') {
                console.log("📩 Recibido answer");

                if (!peerConnection.remoteDescription) {
                    console.warn("⚠️ Sin remote description aún");
                    return;
                }

                await peerConnection.setRemoteDescription(new RTCSessionDescription(message));

            } else if (message.type === 'candidate') {
                console.log("📩 Recibiendo candidato ICE...");
                await peerConnection.addIceCandidate(new RTCIceCandidate(message.candidate));
            }
        } catch (err) {
            console.error("🔴 Error procesando mens aje:", err);
        }
    };

    // Enviar oferta inicial
    ws.onopen = async () => {
        console.log("🟢 WebSocket abierto, iniciando oferta...");
        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);
        ws.send(JSON.stringify(offer));
    };
}