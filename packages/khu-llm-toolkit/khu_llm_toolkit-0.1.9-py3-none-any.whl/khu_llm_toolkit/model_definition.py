import os
import configparser
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings, ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from llama_index.llms.openai import OpenAI as LlamaIndexOpenAI
from llama_index.llms.azure_openai import AzureOpenAI as LlamaIndexAzureOpenAI
from llama_index.embeddings.openai import OpenAIEmbedding as LlamaIndexOpenAIEmbeddings
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding as LlamaIndexAzureOpenAIEmbeddings
from khu_llm_toolkit.commons import FrameworkType, ModelType, ProviderType


class ModelDefinition(object):
    """
    A class that represents an LLM definition.

    Args:
      provider: The name of the LLM provider.
    """

    def __init__(self, config_file_path: str):
        if not os.path.exists(config_file_path):
            raise FileNotFoundError(f"config file '{config_file_path}' does not exist.")
        self.config_file_path = config_file_path
        self.models = self.__parse_ini_file()

    def __parse_ini_file(self):
        config = configparser.ConfigParser()
        config.read(self.config_file_path)

        models = {}
        for section in config.sections():
            group_dict = {}
            for option, value in config[section].items():
                group_dict[option] = value
            models[section] = group_dict

        # for section, group_dict in models.items():
        #     print(f"[{section}]")
        #     for option, value in group_dict.items():
        #         print(f"{option} = {value}")

        return models

    def __repr__(self):
        return "LmDefinition(config_file={})".format(self.config_file_path)

    def get_model(self, id: str, framework=FrameworkType.LANGCHAIN, **kwargs):
        model_dict = self.models[id]
        model_type = ModelType(model_dict['type'])
        if model_type == ModelType.LLM:
            return self.__get_llm(model_dict, framework, **kwargs)
        else:
            return self.__get_embeddings(model_dict, framework, **kwargs)

    def __get_llm(self, model_dict, framework: FrameworkType, **kwargs):
        provider_type = ProviderType(model_dict['provider'])
        if provider_type == ProviderType.AZURE:
            return self.__azure_llm(model_dict, framework, **kwargs)
        if provider_type == ProviderType.OPENAI:
            return self.__openai_llm(model_dict, framework, **kwargs)
        if provider_type == ProviderType.GOOGLE:
            return self.__google_llm(model_dict, framework, **kwargs)

    def __get_embeddings(self, model_dict, framework: FrameworkType, **kwargs):
        provider_type = ProviderType(model_dict['provider'])
        if provider_type == ProviderType.AZURE:
            if framework == FrameworkType.LANGCHAIN:
                return AzureOpenAIEmbeddings(openai_api_key=model_dict["api_key"],
                                             openai_api_version=model_dict["api_version"],
                                             azure_endpoint=model_dict["api_base"],
                                             deployment=model_dict["embeddings_model"])
            else:
                return LlamaIndexAzureOpenAIEmbeddings(
                    model=model_dict["embeddings_model"],
                    deployment_name=model_dict["embeddings_model"],
                    api_key=model_dict["api_key"],
                    azure_endpoint=model_dict["api_base"],
                    api_version=model_dict["api_version"],
                )
        if provider_type == ProviderType.OPENAI:
            if framework == FrameworkType.LANGCHAIN:
                return OpenAIEmbeddings(openai_api_key=model_dict["api_key"])
            else:
                return LlamaIndexOpenAIEmbeddings(
                    model=model_dict["embeddings_model"],
                    api_key=model_dict["api_key"])
        if provider_type == ProviderType.GOOGLE:
            return GoogleGenerativeAIEmbeddings(google_api_key=model_dict["api_key"],
                                                model=model_dict["embeddings_model"])

    def __azure_llm(self, model_dict, framework: FrameworkType, **kwargs):
        kwargs['azure_deployment'] = model_dict["completions_model"]
        if framework == FrameworkType.LANGCHAIN:
            return AzureChatOpenAI(openai_api_key=model_dict["api_key"],
                                   openai_api_type='azure',
                                   openai_api_version=model_dict["api_version"],
                                   azure_endpoint=model_dict["api_base"],
                                   **kwargs)
        else:
            return LlamaIndexAzureOpenAI(
                model=model_dict["completions_model"],
                deployment_name=model_dict["completions_model"],
                api_key=model_dict["api_key"],
                azure_endpoint=model_dict["api_base"],
                api_version=model_dict["api_version"],
            )

    def __openai_llm(self, model_dict, framework: FrameworkType, **kwargs):
        if framework == FrameworkType.LANGCHAIN:
            kwargs['model_name'] = model_dict["completions_model"]
            return ChatOpenAI(openai_api_key=model_dict["api_key"], **kwargs)
        else:
            return LlamaIndexOpenAI(model=model_dict["completions_model"],
                                    api_key=model_dict["api_key"])

    def __google_llm(self, model_dict, framework: FrameworkType, **kwargs):
        return ChatGoogleGenerativeAI(google_api_key=model_dict["api_key"],
                                          model=model_dict["completions_model"],
                                          **kwargs)

    @staticmethod
    def __reset_env():
        key_list = [k for k in dict(os.environ).keys() if 'OPENAI' in k]
        for key in key_list:
            os.environ.pop(key)


if __name__ == '__main__':
    from khu_llm_toolkit.commons import ProviderType
    from langchain.schema import HumanMessage
    from langchain_core.messages.base import BaseMessage
    model_def = ModelDefinition(config_file_path="/home/ken/Develop/MyLlmUtils/llm-config.ini")
    openai_model = model_def.get_model('kenhu-openai-gpt-4')
    openai_embeddings = model_def.get_model('kenhu-openai-embeddings-ada-002')
    gemini_model = model_def.get_model('gemini-1.5-flash')
    gemini_embeddings = model_def.get_model('gemini-embeddings')

    # test LLM
    message = HumanMessage(
        content="Translate this sentence from English to French. I love programming."
    )
    # answer: BaseMessage = gemini_model.invoke([message])
    # print(answer)

    # test EMmbedding
    text = "This is a test query."
    query_result = gemini_embeddings.embed_query(text)
    print(query_result)
