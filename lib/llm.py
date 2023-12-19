from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.vectorstores import FAISS

class LLM:

    def __init__(self, OPENAI_KEY):
        self.api_key = OPENAI_KEY
        self.model = ChatOpenAI(openai_api_key=OPENAI_KEY)

    def free_form(self, chatPromptTemplate:str, dump:dict):
        try:
            prompt = ChatPromptTemplate.from_template(chatPromptTemplate)
            chain = prompt | self.model

            print('free form question: {}'.format(prompt.format()))

            query = chain.invoke(dump)
            content = query.content
            return content
        except Exception as err:
            return str(err)


    def sentiment_analysis(self, csvDump):
        try:
            prompt = ChatPromptTemplate.from_template('as a chemist summarize and expand on the comments and respond in MARKDOWN\n {csvDump}')
            chain = prompt | self.model

            print('sentiment_analysis: {}'.format(prompt.format(csvDump=len(csvDump))))
            query = chain.invoke({'csvDump': csvDump})
            content = query.content

            print(f'content: {content}')
            return content
        except Exception as err:
            return str(err)


    def summary(self, csvDump):
        try:
            prompt = ChatPromptTemplate.from_template("as a chemist expand on the dataset and respond in MARKDOWN\n {csvDump}")
            chain = prompt | self.model

            print('langchain query: {}'.format(prompt.format(csvDump=len(csvDump))))
            query = chain.invoke({'csvDump': csvDump})
            content = query.content

            print(f'content: {content}')
            return content
        except Exception as err:
            return str(err)



    def embeddings_chain(self, processedVectors):
        """
        One of the recipes in the langchain cookbook: https://python.langchain.com/docs/expression_language/cookbook/retrieval
        :param processedVectors:
        :return:
        """
        vectorstore = FAISS.from_texts(texts=processedVectors, embedding=OpenAIEmbeddings(openai_api_key=self.api_key))
        retriever = vectorstore.as_retriever()

        template = """Answer the question based on the following context and be verbose, respond with MARKDOWN:
            {context}

            Question: {question}
            """
        prompt = ChatPromptTemplate.from_template(template)

        chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | self.model
                | StrOutputParser()
        )

        return chain