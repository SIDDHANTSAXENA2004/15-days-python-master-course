from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel

print("Server is starting... 'hiring' and 'training' our AI brains...")
#brain 1 -> sentiment analysis
sentiment_analyzer = pipeline("sentiment-analysis")
#brain 2 -> text generation
text_generator = pipeline("text2text-generation",model="google/flan-t5-large")
print("AI brains are ready! Server is online.")

class PromptRequest(BaseModel):
    text: str

app=FastAPI(
    title="Day 9: AI-Powered API",
    description="The 'brain' is now in the 'waiter'!"
)

@app.get("/")
def read_root():
    return {"message": "Hello, World! Our AI waiter is ready to take your order."}

@app.post("/ask-ai")
def ask_ai(request: PromptRequest):
    prompt_text = request.text
    sentiment_result = sentiment_analyzer(prompt_text)
    sentiment = sentiment_result[0]['label']
    if sentiment == 'POSITIVE':
        prompt_instruction = "Please provide an encouraging and celebratory response"
    elif sentiment == 'NEGATIVE':
        prompt_instruction = "Please provide an empathetic and supportive response"
    else: # Catches NEUTRAL or any other labels
        prompt_instruction = "Please provide a helpful and direct response"
    
    # engineered_prompt = f"The user is feeling {sentiment}. {prompt_instruction} to this user's message: '{prompt_text}'"
    engineered_prompt = f"You are a smart ai assistant . give response to this user's message: '{prompt_text}'"
    
    ai_response_result = text_generator(engineered_prompt, max_length=150, num_return_sequences=1)
    ai_response = ai_response_result[0]['generated_text']
    return {
        "original_prompt": prompt_text,
        "sentiment": sentiment,
        "engineered_prompt": engineered_prompt,
        "ai_response": ai_response
    }
        


