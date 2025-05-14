
from groq import Groq
import os
import base64
import json
from PIL import Image

# Configure API key
os.environ["GROQ_API_KEY"] = "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"
client = Groq()

def encode_image(image_path):
    """Encode une image en base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def extract_invoice_data(base64_image):
    system_prompt = """
    You are an OCR-like data extraction tool that extracts hotel invoice data from images.
    
    Instructions:
    - Return the extracted data in valid JSON format.
    - Don't add extra text outside the JSON.
    """

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract the data in this hotel invoice and output into JSON."},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}", "detail": "high"}}
                ]
            }
        ],
        temperature=0.0,
    )

    return response.choices[0].message.content

def extract_from_image(image_path, output_directory):
    base64_image = encode_image(image_path)
    invoice_json = extract_invoice_data(base64_image)
    invoice_data = json.loads(invoice_json)

    filename = os.path.basename(image_path)
    output_filename = os.path.join(output_directory, filename.replace(".jpg", ".json").replace(".png", ".json"))

    os.makedirs(output_directory, exist_ok=True)

    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(invoice_data, f, ensure_ascii=False, indent=4)

    return output_filename
