
import os
from openai import OpenAI
import ast

class OpenAIService:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def _create_completion(self, messages: list[dict], model: str) -> str:
        response = self.client.chat.completions.create(
            messages=messages,
            model=model
        )
        return response.choices[0].message.content

    def get_education_level(self, educational_experiences: str) -> str:
        messages = [
            {
                "role": "system",
                "content": """You will receive a list of educational experiences as user input (that can be in any language) and you will return the
                        educational level of the user 
                        your response needs to be one of the following educational levels:
                            Pós-graduação Lato Sensu
                            MBA
                            Técnico
                            Licenciatura
                            Fundamental
                            Tecnólogo
                            Outros
                            Bacharelado
                            Doutorado
                            Mestrado
                            Médio
                        answer ONLY with one of the given educational levels exactly as it is written and NOTHING ELSE
                    """
            },
            {
                "role": "user",
                "content": educational_experiences
            }
        ]
        return self._create_completion(messages, "gpt-4o-mini")

    def get_work_fields(self, professional_experiences: str) -> list[str]:
        messages = [
            {
                "role": "system",
                "content": """You will receive a list of professional experiences as user input (that can be in any language) and you will return the
                        work fields of the user 
                        your response needs to be one or more of the following work fields:
                            Tecnologia
                            Administração
                            Outros
                            Engenharia
                            Saúde
                            Marketing
                            Educação
                            Vendas
                            Recursos Humanos
                            Comunicação
                            Finanças
                            Agropecuária
                            Negócios
                        answer ONLY with a list of the given work fields exactly as it is written and NOTHING ELSE

                        answer example: ['Tecnologia', 'Administração']
                    """
            },
            {
                "role": "user",
                "content": professional_experiences
            }
        ]
        string_work_fields = self._create_completion(messages, "gpt-4o-mini")
        return ast.literal_eval(string_work_fields)

    def get_language(self, summary: str) -> str:
        messages = [
            {
                "role": "system",
                "content": """You will receive a user bio and you will return the language it is written. Answer with the language and NOTHING else.
                    """
            },
            {
                "role": "user",
                "content": summary
            }
        ]
        return self._create_completion(messages, "gpt-4o-mini")

    def get_summary(self, professional_experiences: str, educational_experiences: str, work_fields: list[str], language: str) -> str:
        messages = [
            {
                "role": "system",
                "content": f"""You will receive the following information about a user:
                        - Professional experiences: {professional_experiences}
                        - Educational experiences: {educational_experiences}
                        - Work fields: {', '.join(work_fields)}
                        - Language: {language}
                        
                        Based on this information, generate a concise summary of the user's professional and educational background.
                    """
            },
            {
                "role": "user",
                "content": f"""Professional experiences: {professional_experiences}
                        Educational experiences: {educational_experiences}
                        Work fields: {', '.join(work_fields)}
                        Language: {language}
                    """
            }
        ]
        return self._create_completion(messages, "gpt-4o-mini")