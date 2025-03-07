from products.models import Product
from django.views import View
from langchain_ollama.llms import OllamaLLM
from langchain.chains.llm import LLMChain
from django.core import serializers
from langchain.prompts import PromptTemplate



def prompt_model(data,prompt):
    try:
        llm = OllamaLLM(model="deepseek-r1:1.5b")
        template = "Given the following product data: {product_info}\n\nAnswer the following: {user_prompt}"
        prompt_template = PromptTemplate(input_variables=["product_info", "user_prompt"], template=template)
        llm_chain = LLMChain(llm=llm, prompt=prompt_template)
        response = llm_chain.invoke({"product_info": data, "user_prompt": prompt})
        return response
    except Exception as e:
        return f"Error processing the request: {str(e)}"

class Result(View):
    def post(self,request):
        prompt = request.POST.get('prompt')
        print(prompt)
        data = serializers.serialize('json', Product.objects.all())
        print(data)
        response = prompt_model(data,prompt)
        print(response)

        
        

