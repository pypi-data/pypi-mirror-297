import openai
from loguru import logger
from flask import Blueprint, Flask, request, render_template
from .nocodb import NocodbClient

__all__ = ["init_app"]

def init_app(app: Flask, config=None):
    # Merge the default config with the provided config
    base_config = app.config.get("CHATGPT_CONFIG", {})
    if config:
        base_config.update(config)
    config = base_config

    if config.get("blueprint", True):
        bp_name = config.get("blueprint_name", "chatgpt")
        bp_url_prefix = config.get("blueprint_url_prefix", "/chatgpt")
        bp = Blueprint(bp_name, __name__, url_prefix=bp_url_prefix, template_folder="templates")  # 创建一个蓝图对象
        
        # Initialize the storage client
        storage = None
        table_id = None
        storage_config = config.get("storage")
        if storage_config:
            storage_type = storage_config.get("type")
            if storage_type == "nocodb":
                storage = NocodbClient(**storage_config)
                table_id = storage_config.get("table_id")
        @logger.catch
        def save_chat_record(chat_id, user_input, message):
            if storage:
                    storage.add_one(table_id, {
                        "chat_id": chat_id,
                        "user_input": user_input,
                        "message": message
                    }, key="chat_id")

        @bp.route('/')
        def index():
            return render_template("chatgpt/index.html")
        
        @bp.route('/ask', methods=["POST"])
        def ask():
            user_input = request.json.get("user_input")
            max_tokens = request.json.get("max_tokens", 500)
            logger.debug("[{}]{}", max_tokens, user_input)
            if not user_input:
                return {"error": "User input is required."}, 400
            data = {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ],
                "max_tokens": max_tokens,
                "model": "4o-test",
                "temperature": 0.5,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.,
                "stream": False
            }
            response = openai.chat.completions.create(
                **data
            )
            # for chunk in response:
            #     message = chunk.choices[0].delta.content or ""
            logger.debug(response)
            message = response.choices[0].message.content or ""
            save_chat_record(response.id, user_input, message)
            return message

        app.register_blueprint(bp)  # 注册蓝图
        logger.info("Registered the ChatGPT blueprint")
