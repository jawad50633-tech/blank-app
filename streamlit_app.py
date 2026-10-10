
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Puter AI Chat",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 1100px;
        padding-top: 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🤖 Puter AI Chat")
st.caption("AI chat powered by Puter.js and Streamlit")

components.html(
    """
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <script src="https://js.puter.com/v2/"></script>
      <style>
        * { box-sizing: border-box; }

        body {
          margin: 0;
          font-family: Arial, sans-serif;
          color: #e5e7eb;
          background: #111827;
        }

        .app {
          max-width: 900px;
          margin: auto;
          border: 1px solid #374151;
          border-radius: 16px;
          overflow: hidden;
          background: #111827;
        }

        .topbar {
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 12px;
          padding: 16px;
          background: #1f2937;
          border-bottom: 1px solid #374151;
        }

        .brand { font-size: 17px; font-weight: bold; }

        select, button, textarea {
          font: inherit;
        }

        select {
          max-width: 190px;
          padding: 9px;
          border-radius: 8px;
          color: white;
          background: #111827;
          border: 1px solid #4b5563;
        }

        #messages {
          height: 390px;
          overflow-y: auto;
          padding: 18px;
        }

        .msg {
          padding: 12px 14px;
          margin: 10px 0;
          border-radius: 12px;
          max-width: 90%;
          white-space: pre-wrap;
          overflow-wrap: anywhere;
          line-height: 1.6;
        }

        .user {
          margin-left: auto;
          background: #1d4ed8;
          color: white;
        }

        .assistant {
          margin-right: auto;
          background: #273449;
          color: #f3f4f6;
        }

        .status {
          padding: 0 18px 12px;
          color: #9ca3af;
          font-size: 13px;
        }

        .composer {
          padding: 14px;
          border-top: 1px solid #374151;
          background: #1f2937;
        }

        textarea {
          display: block;
          width: 100%;
          resize: vertical;
          min-height: 75px;
          max-height: 160px;
          padding: 12px;
          border-radius: 10px;
          border: 1px solid #4b5563;
          color: white;
          background: #111827;
          outline: none;
        }

        .actions {
          display: flex;
          justify-content: space-between;
          gap: 10px;
          margin-top: 10px;
        }

        button {
          cursor: pointer;
          padding: 10px 16px;
          border: 0;
          border-radius: 8px;
          font-weight: bold;
        }

        #send {
          background: #2563eb;
          color: white;
        }

        #clear {
          background: #374151;
          color: white;
        }

        button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .hint {
          padding: 12px 16px;
          color: #9ca3af;
          font-size: 12px;
          text-align: center;
        }
      </style>
    </head>
    <body>
      <div class="app">
        <div class="topbar">
          <div class="brand">✦ AI Assistant</div>
          <select id="model">
            <option value="openai/gpt-6-astra">
              GPT-6 Astra
            </option>
          </select>
        </div>

        <div id="messages">
          <div class="msg assistant">
            Hello! 👋 I'm your AI assistant.
            What would you like to learn today?
          </div>
        </div>

        <div id="status" class="status">Ready to chat</div>

        <div class="composer">
          <textarea id="prompt"
            placeholder="Ask me anything..."></textarea>
          <div class="actions">
            <button id="clear" type="button">Clear chat</button>
            <button id="send" type="button">Send ↑</button>
          </div>
        </div>

        <div class="hint">
          Responses are generated through Puter.js.
          Internet access is required.
        </div>
      </div>

      <script>
        const messages = document.getElementById("messages");
        const promptBox = document.getElementById("prompt");
        const sendButton = document.getElementById("send");
        const clearButton = document.getElementById("clear");
        const statusBox = document.getElementById("status");
        const modelSelect = document.getElementById("model");

        // Keep conversation history in this browser component.
        const history = [];

        function addMessage(role, text) {
          const div = document.createElement("div");
          div.className = "msg " + role;
          div.textContent = text;
          messages.appendChild(div);
          messages.scrollTop = messages.scrollHeight;
          return div;
        }

        async function sendMessage() {
          const prompt = promptBox.value.trim();
          if (!prompt || sendButton.disabled) return;

          addMessage("user", prompt);
          promptBox.value = "";
          sendButton.disabled = true;
          statusBox.textContent = "Thinking...";

          const model = modelSelect.value;

          try {
            if (!window.puter || !puter.ai) {
              throw new Error(
                "Puter.js did not load. Check your internet connection."
              );
            }

            const response = await puter.ai.chat(
              prompt,
              {
                model: model,
                messages: history
              }
            );

            let answer = "";

            if (typeof response === "string") {
              answer = response;
            } else {
              answer =
                response?.message?.content ??
                response?.text ??
                JSON.stringify(response);
            }

            // Some APIs return content as an array of text blocks.
            if (Array.isArray(answer)) {
              answer = answer
                .map(item => item.text || "")
                .join("\\n");
            }

            answer = String(answer);

            history.push(
              { role: "user", content: prompt },
              { role: "assistant", content: answer }
            );

            addMessage("assistant", answer);
            statusBox.textContent = "Ready to chat";

          } catch (error) {
            addMessage(
              "assistant",
              "Error: " + (error.message || String(error))
            );
            statusBox.textContent = "Request failed";
          } finally {
            sendButton.disabled = false;
            promptBox.focus();
          }
        }

        sendButton.addEventListener("click", sendMessage);

        promptBox.addEventListener("keydown", event => {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
          }
        });

        clearButton.addEventListener("click", () => {
          history.length = 0;
          messages.replaceChildren();
          addMessage("assistant", "Chat cleared. What shall we discuss?");
          statusBox.textContent = "Ready to chat";
        });
      </script>
    </body>
    </html>
    """,
    height=690,
    scrolling=True,
)
