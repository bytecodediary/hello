from django.http import JsonResponse
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import json
import logging
import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Configure logging
logger = logging.getLogger('frontend')

# Define the model path using OS-independent format
model_path = r'C:\Users\lawrence.wafula\git\hello\frontend\model.keras'

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

@login_required
def get_chatbot_response(request):
    if request.method == 'POST':
        try:
            # Load JSON data from the request body
            body = json.loads(request.body)
            user_input = body.get('message', '')

            # Validate input
            if not user_input:
                logger.warning("Received an empty message from the user.")
                return JsonResponse({'error': 'Message is empty'}, status=400)

            logger.info(f"Received message: {user_input}")

            # Tokenize input and generate a response
            input_ids = tokenizer.encode(user_input, return_tensors='pt').to(device)  # Move input tensor to GPU
            output = model.generate(
                input_ids,
                max_length=100,
                num_beams=4,
                no_repeat_ngram_size=2,
                early_stopping=True
            )

            # Decode the model output
            bot_response = tokenizer.decode(output[0], skip_special_tokens=True)

            logger.info(f"Generated response: {bot_response}")

            return JsonResponse({'response': bot_response})

        except Exception as e:
            # Log the error for debugging purposes
            logger.error(f"Error in get_chatbot_response: {str(e)}")
            return JsonResponse({'error': 'An error occurred while processing your request. Please try again later.'}, status=500)
    else:
        logger.warning("Invalid request method received.")
        return JsonResponse({'error': 'Invalid request method'}, status=400)

def home(request):
    return render(request, 'frontend/chatbot.html')