# F.R.I.D.A.Y

the next generation artificial intelligence bot after Jarvis. in this vision, some improvements were made:

- More robust;
- Connect to _uranus_;
- Mission support, I can add missions to Friday;
- Learnable, Friday supports learning new things with mental;
- More..

Friday based on `uranuspy`.

You can register a robot account on `http://g.manaai.cn`, then you can use the bot user name and password to connect uranuspy:

```py
from uranuspy.im.models import ChatMessage, ContactChat, User
from uranuspy.im.client import ChatClient


client = ChatClient("bot", "xxx")


def hanlde_txt_msg(
    msg: ChatMessage, contact: ContactChat, myself: User, client: ChatClient
):
    """
    Main logic to process the received message
    """
    print(f"Received chat message: {msg} {myself}")
    talk_to = msg.fromId
    from_talk = msg.text

    print(myself.user_nick_name, from_talk, msg.text)
    if from_talk != None:
        if contact.isGroup:
            if f"@{myself.user_nick_name}" in from_talk:
                return "我在呢～", myself
        else:
            return "测试消息，这是echo测试", myself


@client.on_txt_msg
def on_txt_msg(
    msg: ChatMessage, contact: ContactChat, myself: User, client: ChatClient
):
    return hanlde_txt_msg(msg, contact, myself, client)


if __name__ == "__main__":
    client.run_forever()


```

## Updates

- **2021.11.14**: Add new Siren client support, it now can be connected with Siren client;

## Requirements

For ubuntu setup simply:

```
pip install -r requirements.txt
```

If on windows, for some package might not easy to install, like PyAduio, it can be installed via `pipwin`:

```
pip install pipwin
pipwin install pyaudio
```
