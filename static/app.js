class Chatbox{
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    //  chatbot toggle
    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);

        //  'http://127.0.0.1:5000'
        fetch($SCRIPT_ROOT+'/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })
          .then(r => r.json())
          .then(r => {
            let msg2 = JSON.parse(r.answer);
            let text = msg2.texts[0].split("\\n")[0];
            let titles = msg2.titles || [];
            let posters = msg2.posters || [];

            titles.forEach((title, index) => {
                text += `<br><br>${index + 1}. ${title}<br>${posters[index] || '포스터 없음'}\n\n`;
            });

            let msg_bot = { name: "Choi", message: text };
            console.log("Texts:", msg2);
            this.messages.push(msg_bot);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            var message = item.message;
            var bracketRegex = /\[.*?\]/g;
            message = message.replace(bracketRegex, '');
            var imgRegex = /(https?:\/\/.*?\.jpg)/g;

        var formattedMessage = message.replace(imgRegex, function(match, url) {
            return '<img src="' + url + '" alt="Image" style="max-height: 250px; width: auto; height: auto;" />';
        });
            if (item.name === "Choi")
            {
                html += '<div class="messages__item messages__item--visitor">' + formattedMessage + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
    
}


const chatbot = new Chatbox();
chatbot.display();