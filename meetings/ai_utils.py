

# # from openai import OpenAI
# # import os
# # # from openai.error import RateLimitError

# # from dotenv import load_dotenv
# # from openai import OpenAIError
  

# # load_dotenv()


# # client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# # def generate_summary(transcript):
# #     prompt = f"""
# # Analyze the meeting transcript and return STRICT JSON with:
# # summary, key_points, decisions, action_items, agenda

# # Transcript:
# # {transcript}
# # """
# #     try:  
# #         response = client.chat.completions.create(
# #             model="gpt-4o-mini",
# #             messages=[{"role": "user", "content": prompt}],
# #             temperature=0.3
# #         )
# #         return response.choices[0].message.content

# #     except RateLimitError:  
# #         return '{"summary": "OpenAI quota exceeded. Summary unavailable.", "key_points": [], "decisions": [], "action_items": [], "agenda": []}'

# from openai import OpenAI
# from openai import OpenAIError
# import os
# from dotenv import load_dotenv
# import json

# load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def generate_summary(transcript):
#     prompt = f"""
# Analyze the meeting transcript and return STRICT JSON with:
# summary, key_points, decisions, action_items, agenda

# Transcript:
# {transcript}
# """
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.3
#         )
#         return response.choices[0].message.content

#     except OpenAIError as e:
#         # 🔹 Handle quota / rate limit errors
#         if hasattr(e, "code") and e.code == "insufficient_quota":
#             return '{"summary": "OpenAI quota exceeded. Summary unavailable.", "key_points": [], "decisions": [], "action_items": [], "agenda": []}'
#         else:
#             # 🔹 Handle other OpenAI errors
#             return f'{{"summary": "OpenAI Error: {str(e)}"}}'
from openai import OpenAI
from openai import OpenAIError
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(transcript):
    prompt = f"""
Analyze the meeting transcript and return STRICT JSON with:
summary, key_points, decisions, action_items, agenda

Transcript:
{transcript}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content

        # 🔹 Check if content is valid JSON
        try:
            json.loads(content)
            return content
        except json.JSONDecodeError:
            return json.dumps({
                "summary": "AI response invalid or empty.",
                "key_points": [],
                "decisions": [],
                "action_items": [],
                "agenda": []
            })

    except OpenAIError as e:
        # 🔹 Handle quota / rate limit errors
        if hasattr(e, "code") and e.code == "insufficient_quota":
            return json.dumps({
                "summary": "OpenAI quota exceeded. Summary unavailable.",
                "key_points": [],
                "decisions": [],
                "action_items": [],
                "agenda": []
            })
        else:
            return json.dumps({
                "summary": f"OpenAI Error: {str(e)}",
                "key_points": [],
                "decisions": [],
                "action_items": [],
                "agenda": []
            })
