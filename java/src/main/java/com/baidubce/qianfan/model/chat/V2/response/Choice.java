package com.baidubce.qianfan.model.chat.V2.response;

import com.baidubce.qianfan.model.chat.V2.Message;

public class Choice extends BaseChoice<Choice> {

    private Message message;

    public Message getMessage() {
        return message;
    }

    public Choice setMessage(Message message) {
        this.message = message;
        return this;
    }

}
