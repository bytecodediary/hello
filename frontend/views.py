from django.http import JsonResponse
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import logging
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.conf import settings

# Define the model path using OS-independent format
model_path = settings.MODEL_PATH

# Configure logging
logger = logging.getLogger('frontend')



# Check if the path exists
if not os.path.exists(model_path):
    logger.error(f"Model path does not exist: {model_path}")
else:
    logger.info(f"Model found at {model_path}")

# Load the trained tokenizer and model (using Hugging Face's AutoModelForCausalLM)
tokenizer = AutoTokenizer.from_pretrained("gpt2")  # Assuming GPT-2 tokenizer, adjust accordingly
model = AutoModelForCausalLM.from_pretrained("gpt2")  # Change to the appropriate model if needed

# Move model to GPU if available
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

def get_chatbot_response(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_input = body.get('message', '')

            if not user_input:
                return JsonResponse({'error': 'Message is empty'}, status=400)

            # Prepare input
            input_ids = tokenizer.encode(user_input, return_tensors='pt')

            # Create attention mask
            attention_mask = (input_ids != tokenizer.pad_token_id).float() # Use float()

            # Ensure pad_token_id is properly set
            if tokenizer.pad_token_id is None:
                logger.error('tokenizer.pad_token_id is not set')
                return JsonResponse({'error': 'Tokenizer pad_token_id is not set'}, status=500)

            
            # Move tensors to the appropriate device
            input_ids = input_ids.to(device)
            attention_mask = attention_mask.to(device)

            # Generate response
            output = model.generate(
                input_ids,
                attention_mask=attention_mask,
                max_length=50,  # Reducing max_length
                temperature=0.7,  # Controls randomness
                top_p=0.9,  # Top-p (nucleus) sampling
                no_repeat_ngram_size=2,
                early_stopping=True
            )
            bot_response = tokenizer.decode(output[0], skip_special_tokens=True)

            # Simple post-processing to filter out unwanted content
            if 'http' in bot_response or len(bot_response.strip()) == 0:
                bot_response = "Sorry, I don't understand that."

            return JsonResponse({'response': bot_response})

        except Exception as e:
            logger.error(f"Error in get_chatbot_response: {str(e)}")
            return JsonResponse({'error': 'An error occurred while processing your request.'}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def home(request):
    return render(request, 'frontend/chatbot.html')