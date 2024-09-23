
from openai import OpenAI
import ast

class OpenAIService:
    def __init__(self, openai_key: str):
        self.client = OpenAI(api_key=openai_key)

    def get_education_level(self, educational_experiences: str) -> str:
        educational_level = self.client.chat.completions.create(
            messages=[
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
                    "content": f"{educational_experiences}"
                }
            ],
            model="gpt-4o-mini"
        )
        return educational_level.choices[0].message.content

    def get_work_fields(self, professional_experiences: str) -> list[str]:
        work_field = self.client.chat.completions.create(
            messages=[
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
                    "content": f"{professional_experiences}"
                }
            ],
            model="gpt-4o-mini"
        )
        string_work_fields = work_field.choices[0].message.content
        return ast.literal_eval(string_work_fields)

    def get_language(self, summary: str) -> str:
        language = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You will receive a user bio and you will return the language it is written. Answer with the language and NOTHING else.
                        """
                },
                {
                    "role": "user",
                    "content": f"{summary}"
                }
            ],
            model="gpt-3.5-turbo"
        )
        return language.choices[0].message.content

