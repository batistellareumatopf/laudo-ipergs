(function () {
  const API_URL = 'https://laudo-ipergs.onrender.com/api/chat';
  const WA_NUMBER = '5554999597009';
  const WA_MSG = encodeURIComponent('Olá! Gostaria de agendar uma consulta com o Dr. Fábio Batistella.');

  const css = `
    #fb-chat-btn {
      position: fixed; bottom: 28px; right: 28px; z-index: 9999;
      width: 60px; height: 60px; border-radius: 50%;
      background: #1a6fc4; color: #fff; border: none; cursor: pointer;
      box-shadow: 0 4px 16px rgba(0,0,0,0.25);
      font-size: 26px; display: flex; align-items: center; justify-content: center;
      transition: transform 0.2s;
    }
    #fb-chat-btn:hover { transform: scale(1.08); }
    #fb-chat-box {
      position: fixed; bottom: 100px; right: 28px; z-index: 9998;
      width: 340px; max-height: 500px;
      background: #fff; border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.18);
      display: none; flex-direction: column; overflow: hidden;
      font-family: Arial, sans-serif; font-size: 14px;
    }
    #fb-chat-header {
      background: #1a6fc4; color: #fff;
      padding: 14px 16px; display: flex; align-items: center; gap: 10px;
    }
    #fb-chat-header .avatar {
      width: 40px; height: 40px; border-radius: 50%;
      background: #fff; color: #1a6fc4;
      display: flex; align-items: center; justify-content: center;
      font-weight: bold; font-size: 15px; flex-shrink: 0;
    }
    #fb-chat-header .info { flex: 1; }
    #fb-chat-header .info strong { display: block; font-size: 14px; }
    #fb-chat-header .info span { font-size: 11px; opacity: 0.85; }
    #fb-chat-close { background: none; border: none; color: #fff; font-size: 20px; cursor: pointer; }
    #fb-chat-msgs {
      flex: 1; overflow-y: auto; padding: 12px;
      display: flex; flex-direction: column; gap: 8px;
      background: #f4f7fb; min-height: 200px; max-height: 300px;
    }
    .fb-msg { max-width: 85%; padding: 8px 12px; border-radius: 12px; line-height: 1.5; }
    .fb-msg.bot { background: #fff; border: 1px solid #dde3ef; align-self: flex-start; border-bottom-left-radius: 3px; }
    .fb-msg.user { background: #1a6fc4; color: #fff; align-self: flex-end; border-bottom-right-radius: 3px; }
    .fb-msg.typing { color: #888; font-style: italic; }
    #fb-chat-wa {
      background: #25d366; color: #fff; border: none;
      padding: 8px 14px; border-radius: 20px; cursor: pointer;
      font-size: 13px; display: flex; align-items: center; gap: 6px;
      margin: 4px 12px 8px; width: calc(100% - 24px);
    }
    #fb-chat-footer {
      padding: 10px 12px; background: #fff; border-top: 1px solid #eee;
      display: flex; gap: 8px;
    }
    #fb-chat-input {
      flex: 1; border: 1px solid #ccc; border-radius: 20px;
      padding: 8px 14px; font-size: 13px; outline: none;
    }
    #fb-chat-send {
      background: #1a6fc4; color: #fff; border: none;
      border-radius: 50%; width: 36px; height: 36px; cursor: pointer; font-size: 16px;
    }
  `;

  const style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  document.body.insertAdjacentHTML('beforeend', `
    <button id="fb-chat-btn" title="Falar com Dr. Fábio">💬</button>
    <div id="fb-chat-box">
      <div id="fb-chat-header">
        <div class="avatar">FB</div>
        <div class="info">
          <strong>Assistente do Dr. Fábio</strong>
          <span>Reumatologista • Passo Fundo</span>
        </div>
        <button id="fb-chat-close">×</button>
      </div>
      <div id="fb-chat-msgs">
        <div class="fb-msg bot">Olá, como está? Eu sou o assistente do Dr. Fábio, estou aqui para lhe ajudar!</div>
      </div>
      <button id="fb-chat-wa">
        <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
          <path d="M13.601 2.326A7.85 7.85 0 0 0 7.994 0C3.627 0 .068 3.558.064 7.926c0 1.399.366 2.76 1.057 3.965L0 16l4.204-1.102a7.9 7.9 0 0 0 3.79.965h.004c4.368 0 7.926-3.558 7.93-7.93A7.9 7.9 0 0 0 13.6 2.326zM7.994 14.521a6.6 6.6 0 0 1-3.356-.92l-.24-.144-2.494.654.666-2.433-.156-.251a6.56 6.56 0 0 1-1.007-3.505c0-3.626 2.957-6.584 6.591-6.584a6.56 6.56 0 0 1 4.66 1.931 6.56 6.56 0 0 1 1.928 4.66c-.004 3.639-2.961 6.592-6.592 6.592m3.615-4.934c-.197-.099-1.17-.578-1.353-.646-.182-.065-.315-.099-.445.099-.133.197-.513.646-.627.775-.114.133-.232.148-.43.05-.197-.1-.836-.308-1.592-.985-.59-.525-.985-1.175-1.103-1.372-.114-.198-.011-.304.088-.403.087-.088.197-.232.296-.346.1-.114.133-.198.198-.33.065-.134.034-.248-.015-.347-.05-.099-.445-1.076-.612-1.47-.16-.389-.323-.335-.445-.34-.114-.007-.247-.007-.38-.007a.73.73 0 0 0-.529.247c-.182.198-.691.677-.691 1.654s.71 1.916.81 2.049c.098.133 1.394 2.132 3.383 2.992.47.205.84.326 1.129.418.475.152.904.129 1.246.08.38-.058 1.171-.48 1.338-.943.164-.464.164-.86.114-.943-.049-.084-.182-.133-.38-.232"/>
        </svg>
        Agendar consulta pelo WhatsApp
      </button>
      <div id="fb-chat-footer">
        <input id="fb-chat-input" type="text" placeholder="Digite sua dúvida...">
        <button id="fb-chat-send">➤</button>
      </div>
    </div>
  `);

  let history = [];
  let open = false;

  function toggleChat() {
    open = !open;
    document.getElementById('fb-chat-box').style.display = open ? 'flex' : 'none';
    if (open) document.getElementById('fb-chat-input').focus();
  }

  function addMsg(text, role) {
    const msgs = document.getElementById('fb-chat-msgs');
    const div = document.createElement('div');
    div.className = 'fb-msg ' + role;
    div.textContent = text;
    msgs.appendChild(div);
    msgs.scrollTop = msgs.scrollHeight;
    return div;
  }

  async function sendMsg() {
    const input = document.getElementById('fb-chat-input');
    const text = input.value.trim();
    if (!text) return;
    input.value = '';
    addMsg(text, 'user');
    const typing = addMsg('Digitando...', 'bot typing');
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, history }),
      });
      const data = await res.json();
      typing.remove();
      const reply = data.reply || 'Desculpe, não consegui responder agora.';
      addMsg(reply, 'bot');
      history.push({ role: 'user', content: text });
      history.push({ role: 'assistant', content: reply });
      if (history.length > 20) history = history.slice(-20);
    } catch {
      typing.remove();
      addMsg('Erro de conexão. Tente novamente.', 'bot');
    }
  }

  document.getElementById('fb-chat-btn').addEventListener('click', toggleChat);
  document.getElementById('fb-chat-close').addEventListener('click', toggleChat);
  document.getElementById('fb-chat-send').addEventListener('click', sendMsg);
  document.getElementById('fb-chat-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') sendMsg();
  });
  document.getElementById('fb-chat-wa').addEventListener('click', () => {
    window.open(`https://wa.me/${WA_NUMBER}?text=${WA_MSG}`, '_blank');
  });
})();
