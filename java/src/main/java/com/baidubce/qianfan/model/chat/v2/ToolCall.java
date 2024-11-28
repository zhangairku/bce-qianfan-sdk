package com.baidubce.qianfan.model.chat.v2;

import com.baidubce.qianfan.model.chat.v2.response.Function;

public class ToolCall {

    public final String type = "function";

    private String id;

    private Function function;

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public Function getFunction() {
        return function;
    }

    public void setFunction(Function function) {
        this.function = function;
    }
}
