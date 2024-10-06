from PIL import ImageGrab 
import base64
import io
import openai
import pyperclip
import requests

def get_image_from_clipboard():
    img = ImageGrab.grabclipboard()
    if img: 
        return img
    else:
        print("There are no images in the clipboard")
        return None
    
def convert_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img64

def send_to_gpt(img64):
    
    openai.api_key = "YOUR_API_KEY" #change this with your openai api key
    img_str = f"data:image/png;base64,{img64}"
    
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Brindame SOLAMENTE Y UNICAMENTE el texto que contiene esta imagen, no me brindes algo como \'El texto de esta imagen es\'. Nuevamente, SOLO el texto que esta adentro"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": img_str
                        }
                    }
                      
                ],
            }
        ],
        max_tokens = 300
    )
    
    try:
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred while trying to access the response: {str(e)}"
   
if __name__ == '__main__':
    img = get_image_from_clipboard()
    if img:
        img_64 = convert_to_base64(img)
        response = send_to_gpt(img_64)
        pyperclip.copy(response)
        
    
    