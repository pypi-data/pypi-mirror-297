from datetime import datetime

import os
import pytz
import httpx
import math
import asyncio



def count_tokens(message):
    length = len(message)
    num_tokens = length / 4
    result = math.ceil(num_tokens)
    print(f"Number of tokens: {result}")
    return result


def get_token_size(token_count):
    if token_count < 300:
        return "s"
    elif token_count <= 600:
        return "m"
    elif token_count <= 1000:
        return "l"
    elif token_count <= 2000:
        return "xl"
    elif token_count <= 3000:
        return "xxl"
    elif token_count <= 4000:
        return "xxxl"
    else:
        return "4xl"


async def log(input_prompt="", output_completion="", transaction_uuid="", **kwargs):
    try:
        input_found = False
        output_found = False
        input_length = 0
        output_length = 0
        input_token_size = " "
        output_token_size = " "
        num_token_input = 0
        num_token_output = 0

        if not input_prompt and not output_completion:
            raise ValueError("Input Prompt and Output Prompt, Both Cannot be empty, Either one of it, should have value")

        if input_prompt:
            input_found = True
            input_length = len(input_prompt)

        if output_completion:
            output_found = True
            output_length = len(output_completion)

        credit_id = kwargs.get('CREDIT_ID')
        client_id = kwargs.get('CLIENT_ID')
        print("client_id", client_id)
        application_name = kwargs.get('APPLICATION_NAME')
        ai_platform = kwargs.get('AI_PLATFORM')
        model_parent_id = kwargs.get('MODEL_PARENT_ID')
        model_id = kwargs.get('MODEL_ID')
        setnext_ai_metering_api_token = kwargs.get('SETNEXT_METERING_API_TOKEN')

        if not credit_id:
            raise ValueError("SETNEXT-METERING: Validation Error. CREDIT_ID is mandatory.")
        if not client_id:
            raise ValueError("SETNEXT-METERING: Validation Error. CLIENT_ID is mandatory.")
        if not application_name:
            raise ValueError("SETNEXT-METERING: Validation Error. APPLICATION_NAME is not found.")
        if not ai_platform:
            raise ValueError("SETNEXT-METERING: Validation Error. AI_PLATFORM is not found.")
        if not model_parent_id:
            raise ValueError("SETNEXT-METERING: Validation Error. MODEL_PARENT_ID is not found.")
        if not model_id:
            raise ValueError("SETNEXT-METERING: Validation Error. MODEL_ID is not found.")
        if not setnext_ai_metering_api_token:
            raise ValueError("SETNEXT-METERING: Validation Error. SETNEXT_METERING_API_TOKEN is not found.")

        num_token_input = count_tokens(input_prompt)
        num_token_output = count_tokens(output_completion)

        input_token_size = get_token_size(num_token_input)
        output_token_size = get_token_size(num_token_output)

        current_datetime = datetime.now(pytz.UTC)
        india_tz = pytz.timezone('Asia/Kolkata')
        india_datetime = current_datetime.astimezone(india_tz)

        message_body = {
            "credit_id": credit_id,
            "client_id": client_id,
            "num_token_input": num_token_input,
            "input_length": input_length,
            "output_length": output_length,
            "num_token_output": num_token_output,
            "input_token_size": input_token_size,
            "output_token_size": output_token_size,
            "transaction_uuid": transaction_uuid,
            "ai_platform": ai_platform,
            "model_parent_id": model_parent_id,
            "model_id": model_id,
            "application_name": application_name,
            "date_time": current_datetime.isoformat(),
            "india_date_time": india_datetime.strftime('%d-%m-%Y %H:%M:%S %Z%z'),
            "unix_ts": int(current_datetime.timestamp())
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://cj9fivjw52.execute-api.us-east-1.amazonaws.com/dev/metering/',
                json=message_body,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

        print("response", response.json())
        return message_body

    except Exception as err:
        print(err)
        return False

async def log_image_to_text(image_path, input_text,  output_text, transaction_uuid="", **kwargs):
    try:
        image = image_path
        input_length = len(input_text)
        output_length = len(output_text)
        num_token_output = count_tokens(output_text)
        output_token_size = get_token_size(num_token_output)

        credit_id = kwargs.get('CREDIT_ID') or os.environ.get('CREDIT_ID')
        client_id = kwargs.get('CLIENT_ID') or os.environ.get('CLIENT_ID')
        application_name = kwargs.get('APPLICATION_NAME') or os.environ.get('APPLICATION_NAME')
        ai_platform = kwargs.get('AI_PLATFORM') or os.environ.get('AI_PLATFORM')
        model_parent_id = kwargs.get('MODEL_PARENT_ID') or os.environ.get('MODEL_PARENT_ID')
        model_id = kwargs.get('MODEL_ID') or os.environ.get('MODEL_ID')
        setnext_ai_metering_api_token = kwargs.get('SETNEXT_METERING_API_TOKEN') or os.environ.get(
            'SETNEXT_METERING_API_TOKEN')

        if not credit_id:
            raise ValueError("SETNEXT-METERING: Validation Error. CREDIT_ID is mandatory.")
        if not client_id:
            raise ValueError("SETNEXT-METERING: Validation Error. CLIENT_ID is mandatory.")
        if not application_name:
            raise ValueError("SETNEXT-METERING: Validation Error. APPLICATION_NAME is not found.")
        if not ai_platform:
            raise ValueError("SETNEXT-METERING: Validation Error. AI_PLATFORM is not found.")
        if not model_parent_id:
            raise ValueError("SETNEXT-METERING: Validation Error. MODEL_PARENT_ID is not found.")
        if not model_id:
            raise ValueError("SETNEXT-METERING: Validation Error. MODEL_ID is not found.")
        if not setnext_ai_metering_api_token:
            raise ValueError("SETNEXT-METERING: Validation Error. SETNEXT_METERING_API_TOKEN is not found.")

        current_datetime = datetime.now(pytz.UTC)
        india_tz = pytz.timezone('Asia/Kolkata')
        india_datetime = current_datetime.astimezone(india_tz)

        message_body = {
            "credit_id": credit_id,
            "client_id": client_id,
            "image": image,
            "input_length": input_length,
            "output_length": output_length,
            "num_token_output": num_token_output,
            "output_token_size": output_token_size,
            "transaction_uuid": transaction_uuid,
            "ai_platform": ai_platform,
            "model_parent_id": model_parent_id,
            "model_id": model_id,
            "application_name": application_name,
            "date_time": current_datetime.isoformat(),
            "india_date_time": india_datetime.strftime('%d-%m-%Y %H:%M:%S %Z%z'),
            "unix_ts": int(current_datetime.timestamp()),
            "input_type": "image",
            "output_type": "text"
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://cj9fivjw52.execute-api.us-east-1.amazonaws.com/dev/metering/',
                json=message_body,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

        print("response", response.json())
        return message_body

    except Exception as err:
        print(err)
        return False

async def log_text_to_image(input_text, output_image_path, transaction_uuid="", **kwargs):
    try:
        image = output_image_path
        num_token_input = count_tokens(input_text)  # Assuming you have this function
        input_token_size = get_token_size(num_token_input)  # Assuming you have this function

        # Retrieve configuration parameters
        credit_id = kwargs.get('CREDIT_ID') or os.environ.get('CREDIT_ID')
        client_id = kwargs.get('CLIENT_ID') or os.environ.get('CLIENT_ID')
        application_name = kwargs.get('APPLICATION_NAME') or os.environ.get('APPLICATION_NAME')
        ai_platform = kwargs.get('AI_PLATFORM') or os.environ.get('AI_PLATFORM')
        model_parent_id = kwargs.get('MODEL_PARENT_ID') or os.environ.get('MODEL_PARENT_ID')
        model_id = kwargs.get('MODEL_ID') or os.environ.get('MODEL_ID')
        setnext_ai_metering_api_token = kwargs.get('SETNEXT_METERING_API_TOKEN') or os.environ.get(
            'SETNEXT_METERING_API_TOKEN')

        # Validate required parameters
        required_params = {
            'CREDIT_ID': credit_id,
            'CLIENT_ID': client_id,
            'APPLICATION_NAME': application_name,
            'AI_PLATFORM': ai_platform,
            'MODEL_PARENT_ID': model_parent_id,
            'MODEL_ID': model_id,
            'SETNEXT_METERING_API_TOKEN': setnext_ai_metering_api_token
        }

        for param_name, param_value in required_params.items():
            if not param_value:
                raise ValueError(f"SETNEXT-METERING: Validation Error. {param_name} is mandatory.")

        # Prepare timestamp information
        current_datetime = datetime.now(pytz.UTC)
        india_tz = pytz.timezone('Asia/Kolkata')
        india_datetime = current_datetime.astimezone(india_tz)

        # Prepare the message body
        message_body = {
            "credit_id": credit_id,
            "client_id": client_id,
            "imagepath": image,
            "num_token_input": num_token_input,
            "input_token_size": input_token_size,
            "transaction_uuid": transaction_uuid,
            "ai_platform": ai_platform,
            "model_parent_id": model_parent_id,
            "model_id": model_id,
            "application_name": application_name,
            "date_time": current_datetime.isoformat(),
            "india_date_time": india_datetime.strftime('%d-%m-%Y %H:%M:%S %Z%z'),
            "unix_ts": int(current_datetime.timestamp()),
            "input_type": "text",
            "output_type": "image"
        }

        # Send the POST request
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://cj9fivjw52.execute-api.us-east-1.amazonaws.com/dev/metering/',
                json=message_body,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()

        print("response", response.json())
        return message_body

    except Exception as err:
        print(err)
        return False


def get_num_token(message):
    return count_tokens(message)
    pass


async def main():
    try:
        result = await log_text_to_image(
            output_image_path=r"C:\Users\dhara\OneDrive\Pictures\Saved Pictures\download.jpeg",
            input_text="Hello, how are you?",
            transaction_uuid="123456"
        )
        print(result)
    except Exception as err:
        print(f"An error occurred: {err}")


if __name__ == "__main__":
    asyncio.run(main())
