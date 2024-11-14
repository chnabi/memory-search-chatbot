'use client'
import Image from "next/image";
import { Message, messageSchema } from "@/schema"
import {ChangeEvent, useEffect, useState} from 'react';
import { HtmlContext } from "next/dist/server/route-modules/pages/vendored/contexts/entrypoints";
import { z } from "zod"



export default function Home() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')

 const handleChatSubmit = async() => {
  if(input == ""){
    setMessages([...messages, { role: 'System', content: 'Must type an input'}]);
    return
  }
  console.log(input)
  const response = await fetch('https://chatbotdeliv.onrender.com/conversation/chat', {
    method: 'POST',  
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ input:input }),
  });
  const data = await response.json();
  console.log(data)
  setMessages([...messages, { role: 'User', content: input }, { role: 'Assistant', content: data.response }]);
  setInput('')
 }

 const handleMemorizeSubmit = async() => {
  if(input == ""){
    setMessages([...messages, { role: 'System', content: 'Must type an input'}]);
    return
  }
  const response = await fetch('https://chatbotdeliv.onrender.com/conversation/memorize', {
    method: 'POST',  
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ data:[input] }),
  });
  const status = await response.json();
  setMessages([...messages, { role: 'System', content: status.status}]);
  setInput("")
 }

  return (
    <div className="bg-slate-500 flex flex-col items-center h-screen w-screen ">
      <h1
      className="text-lg"
      >Personal Chatbot</h1>
      <div
      className="bg-slate-300 text-slate-800 rounded-lg"
      >
        {messages.map((msg, index) => (
          <div key={index} style={{ marginBottom: '8px' }}>
             {msg.role}: {msg.content}
          </div>
        ))}
      </div>
      <input
      type = 'text'
      placeholder="enter your text here"
      value = {input}
      onChange = {(e) => setInput(e.target.value)} 
      className = 'text-slate-800 mr-2 rounded-md my-2.5'   
      ></input>
      <div className="flex"> 
      <button
      onClick = {(e) => {
        handleChatSubmit()
        console.log("submitted")
      }}
      className="mr-2 bg-slate-100 rounded-md text-slate-800 h-5 w-40 my-2.5"
      >
        Submit  
      </button>
      <button
      onClick={(e) => {
        handleMemorizeSubmit()
      }}
      className="mr-2 bg-slate-100 rounded-md text-slate-800 h-5 w-40 my-2.5"
      >
        Memorize 
      </button>
      </div>
    </div>
  );
}
