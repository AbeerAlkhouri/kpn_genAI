from langchain_openai import AzureChatOpenAI
from langchain.agents import create_agent
from app.services.kpn_tools import kpn_annual_report_search, kpn_news_tool, kpn_products_tool
from core.config import settings


class KPNAgentService:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            openai_api_key=settings.AZURE_OPENAI_KEY,
            azure_deployment=settings.AZURE_GPT_DEPLOYMENT,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            temperature=0.2,
        )

        self.tools = [kpn_annual_report_search, kpn_news_tool, kpn_products_tool]

        self.system_prompt = """You are a helpful and professional AI assistant specialized in KPN (Koninklijke KPN N.V.). 
    Your goal is to answer questions from KPN customers or stakeholders using the documents provided in your knowledge base.

    Always use the 'kpn_annual_report_search' tool to find accurate and up-to-date information about KPN's financials, strategy, sustainability goals, and general operations.

    If a question cannot be answered by the documents, politely inform the user.
    Always mention that the information was retrieved from official KPN documentation."""

        self.agent_graph = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt,
            debug=False
        )

    async def run_agent(self, user_input: str, chat_history: list = None):
        """
        Executes the agent for a given user input.
        """
        messages = []
        if chat_history:
            for msg in chat_history:
                # Ensure each message has the required keys for LangChain/OpenAI
                if isinstance(msg, dict) and "role" in msg and "content" in msg:
                    messages.append(msg)

        messages.append({"role": "user", "content": user_input})

        inputs = {"messages": messages}

        try:
            result = await self.agent_graph.ainvoke(inputs)

            output_messages = result.get("messages", [])
            if output_messages:
                last_message = output_messages[-1]
                if hasattr(last_message, "content"):
                    return str(last_message.content)
                elif isinstance(last_message, dict):
                    return str(last_message.get("content", "No response generated."))

            return "No response generated."
        except Exception as e:
            raise e


agent_service = KPNAgentService()
