import os
import openai
from langchain_core.prompts import ChatPromptTemplate
import time

# Initialize OpenAI client with Sambanova credentials
client = openai.OpenAI(
    api_key="726c299f-664e-451d-8316-94e68e232718",
    base_url="https://api.sambanova.ai/v1",
)

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
)

def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)

    parsed_results = []

    for i, chunk in enumerate(dom_chunks, start=1):
        try:
            messages = [{"role": "system", "content": "You are a helpful assistant"},
                        {"role": "user", "content": prompt.format(dom_content=chunk, parse_description=parse_description)}]

            response = client.chat.completions.create(
                model="Meta-Llama-3.1-8B-Instruct",  # Or your desired Sambanova model
                messages=messages,
                temperature=0.1,  # Adjust as needed
                top_p=0.1        # Adjust as needed
            )

            result = response.choices[0].message.content
            print(f"Parsed batch: {i} of {len(dom_chunks)}")
            parsed_results.append(result)

        except Exception as e:
            print(f"Error parsing chunk {i}: {e}")
            time.sleep(2)  # Optional retry after short delay
            continue

    return "\n".join(parsed_results)