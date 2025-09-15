import os
from openai import OpenAI
import instructor
from anthropic import Anthropic
from utils.datamodels import PersonalizedMessageResponse
from utils.prompts import personalized_message_generator_system_prompt, personalized_message_generator_user_prompt


def call_personalized_message_generator(final_mass):
    """Function to call the image prompt generator with slide content"""
    anthropic_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    client = instructor.from_anthropic(client=anthropic_client, mode=instructor.Mode.ANTHROPIC_JSON)

    
    AI_Response, completion = client.chat.completions.create_with_completion(
        model="claude-3-7-sonnet-20250219",
        messages=[
            {
                "role": "system",
                "content": personalized_message_generator_system_prompt
            },
            {
                "role": "user",
                "content": personalized_message_generator_user_prompt.format(
                    insan_sarrafi=final_mass['insan_sarrafi'],
                    kultur_mantari=final_mass['kultur_mantari'],
                    vizyoner=final_mass['vizyoner'],
                    teknoloji_gurusu=final_mass['teknoloji_gurusu'],
                    kisisel_gelisen=final_mass['kisisel_gelisen']
                )
            }
        ],
        response_model=PersonalizedMessageResponse,
        temperature=0.7,
        max_tokens=8192,
        top_p=1,
    )

    
    input_tokens = completion.usage.input_tokens
    output_tokens = completion.usage.output_tokens
    
    return AI_Response, input_tokens, output_tokens
