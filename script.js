const chatWindow = document.getElementById('chatWindow');
const composer = document.getElementById('composer');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const suggestions = document.getElementById('suggestions');

function addBubble(text, sender){
  const bubble = document.createElement('div');
  bubble.className = `bubble ${sender}`;
  const p = document.createElement('p');
  p.textContent = text;
  bubble.appendChild(p);
  chatWindow.appendChild(bubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return bubble;
}

function addTypingIndicator(){
  const bubble = document.createElement('div');
  bubble.className = 'bubble bot typing';
  bubble.innerHTML = '<span></span><span></span><span></span>';
  chatWindow.appendChild(bubble);
  chatWindow.scrollTop = chatWindow.scrollHeight;
  return bubble;
}

async function sendMessage(text){
  if(!text.trim()) return;

  addBubble(text, 'user');
  messageInput.value = '';
  sendBtn.disabled = true;
  const typingBubble = addTypingIndicator();

  try{
    const res = await fetch('/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text })
    });
    if(!res.ok) throw new Error('Server error');
    const data = await res.json();
    typingBubble.remove();
    addBubble(data.answer, 'bot');
  }catch(err){
    typingBubble.remove();
    addBubble("Something went wrong on my end — please try again in a moment.", 'bot');
  }finally{
    sendBtn.disabled = false;
    messageInput.focus();
  }
}

composer.addEventListener('submit', (e) => {
  e.preventDefault();
  sendMessage(messageInput.value);
});

suggestions.addEventListener('click', (e) => {
  const chip = e.target.closest('.chip');
  if(!chip) return;
  sendMessage(chip.dataset.q);
});
