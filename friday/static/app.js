const chat = document.getElementById("chat");
const textInput = document.getElementById("textInput");
const sendBtn = document.getElementById("sendBtn");
const micBtn = document.getElementById("micBtn");
const qrBtn = document.getElementById("qrBtn");
const qrModal = document.getElementById("qrModal");
const closeModal = document.getElementById("closeModal");
const ttsAudio = document.getElementById("ttsAudio");

function pinAl() {
  if (!PIN_GEREKLI) return "";
  let pin = localStorage.getItem("friday_pin");
  if (!pin) {
    pin = prompt("Friday PIN'ini gir:") || "";
    localStorage.setItem("friday_pin", pin);
  }
  return pin;
}

function mesajEkle(kimden, metin) {
  const div = document.createElement("div");
  div.className = "msg " + kimden;
  div.textContent = metin;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

function seslendir(metin, audioUrl) {
  if (audioUrl) {
    ttsAudio.src = audioUrl;
    ttsAudio.play().catch(() => {});
    return;
  }
  if (!("speechSynthesis" in window)) return;
  const utter = new SpeechSynthesisUtterance(metin);
  utter.lang = "tr-TR";
  const sesler = speechSynthesis.getVoices();
  const erkekSes =
    sesler.find(v => v.lang.startsWith("tr") && /male|erkek/i.test(v.name)) ||
    sesler.find(v => v.lang.startsWith("tr"));
  if (erkekSes) utter.voice = erkekSes;
  utter.pitch = 0.8;
  utter.rate = 0.95;
  speechSynthesis.speak(utter);
}

async function komutGonder(metin) {
  if (!metin || !metin.trim()) return;
  mesajEkle("user", metin);
  textInput.value = "";
  try {
    const res = await fetch("/api/command", {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Friday-Pin": pinAl() },
      body: JSON.stringify({ text: metin }),
    });
    if (res.status === 401) {
      localStorage.removeItem("friday_pin");
      mesajEkle("friday", "PIN yanlış, tekrar dene.");
      return;
    }
    const data = await res.json();
    mesajEkle("friday", data.reply);
    seslendir(data.reply, data.audio_url);
  } catch (e) {
    mesajEkle("friday", "Bağlantı hatası: " + e.message);
  }
}

sendBtn.onclick = () => komutGonder(textInput.value);
textInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") komutGonder(textInput.value);
});

// --- Mikrofon (sesli komut) ---
const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRec) {
  const tanima = new SpeechRec();
  tanima.lang = "tr-TR";
  tanima.interimResults = false;

  micBtn.onclick = () => {
    micBtn.classList.add("listening");
    try { tanima.start(); } catch (e) { /* zaten dinliyor olabilir */ }
  };
  tanima.onresult = (e) => {
    const metin = e.results[0][0].transcript;
    komutGonder(metin);
  };
  tanima.onend = () => micBtn.classList.remove("listening");
  tanima.onerror = () => micBtn.classList.remove("listening");
} else {
  micBtn.disabled = true;
  micBtn.title = "Bu tarayıcı sesli komutu desteklemiyor (Chrome veya Edge kullan)";
}

// --- QR modal ---
qrBtn.onclick = async () => {
  qrModal.classList.remove("hidden");
  document.getElementById("qrImg").src = "/qr?" + Date.now();
  try {
    const info = await fetch("/api/network-info").then(r => r.json());
    document.getElementById("networkUrl").textContent = info.url;
  } catch (e) {}
};
closeModal.onclick = () => qrModal.classList.add("hidden");
qrModal.addEventListener("click", (e) => { if (e.target === qrModal) qrModal.classList.add("hidden"); });

mesajEkle("friday", "Merhaba! Ben Friday. Yazarak ya da mikrofona basarak komut verebilirsin. 'yardım' yaz, neler yapabileceğimi gör.");
