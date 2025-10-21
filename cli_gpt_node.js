const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();
const readline = require('readline');

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
const model = genAI.getGenerativeModel({ model: 'gemini-pro-latest' });

// Definisi warna ANSI
const green = '\x1b[32m';
const red = '\x1b[31m';
const yellow = '\x1b[33m';
const cyan = '\x1b[36m';
const reset = '\x1b[0m';

async function chatWithGemini() {
  // Cek dukungan ANSI (opsional)
  if (!process.stdout.isTTY) {
    console.log('Warning: Terminal tidak mendukung ANSI colors. Warna mungkin tidak muncul.');
  }

  // Dapatkan lebar terminal (default 80 jika tidak tersedia)
  const terminalWidth = process.stdout.columns || 80;
  const innerWidth = terminalWidth - 2; // Lebar dalam box (kurangi 2 untuk ║ di kiri dan kanan)

  console.clear();

  // Border atas dan bawah yang dinamis
  const topBorder = `${red}╔${'═'.repeat(innerWidth)}╗${reset}`;
  const bottomBorder = `${red}╚${'═'.repeat(innerWidth)}╝${reset}`;

  console.log(topBorder);

  // Baris 1: ##DITBOT CLI V0.0.2 (rata kanan)
  const titleText = '##DITBOT CLI V0.0.2';
  const titlePadding = ' '.repeat(Math.max(0, innerWidth - titleText.length));
  console.log(`${red}║${yellow}${titleText}${titlePadding}${red}║${reset}`);

  // Baris 2: Welcome back "radit" (rata kanan)
  const welcomeText = 'Welcome back "radit"';
  const welcomePadding = ' '.repeat(Math.max(0, innerWidth - welcomeText.length));
  console.log(`${red}║${reset}${welcomeText}${welcomePadding}${red}║${reset}`);

  // Baris 3: Workspace (dinamis, rata kanan)
  const workspaceText = `Workspace: ${process.cwd()}`;
  const workspacePadding = ' '.repeat(Math.max(0, innerWidth - workspaceText.length));
  console.log(`${red}║${reset}${workspaceText}${workspacePadding}${red}║${reset}`);

  // Baris 4: Tips (rata kanan)
  const tipsText = 'Tips: ketik /help atau "exit" untuk keluar';
  const tipsPadding = ' '.repeat(Math.max(0, innerWidth - tipsText.length));
  console.log(`${red}║${reset}${tipsText}${tipsPadding}${red}║${reset}`);

  console.log(bottomBorder);
  console.log(); // Baris kosong

  const messages = [];
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  async function ask() {
    rl.question(`${cyan}> ${reset}`, async (userInput) => {
      if (userInput.toLowerCase() === 'exit') {
        console.log(`${green}Goodbye, Radit! 👋${reset}`);
        rl.close();
        return;
      }

      messages.push({ role: 'user', content: userInput });

      try {
        const chat = model.startChat({
          history: messages.map(msg => ({
            role: msg.role === 'user' ? 'user' : 'model',
            parts: [{ text: msg.content }],
          })),
        });

        const result = await chat.sendMessage(userInput);
        const response = result.response.text();

        console.log(`${green}Gemini:${reset} ${response}`);
        messages.push({ role: 'assistant', content: response });
      } catch (error) {
        console.error(`${red}Error:${reset} ${error.message}`);
      }

      ask(); // loop lagi
    });
  }

  ask();
}

chatWithGemini();