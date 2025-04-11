from products.models import Product
from django.views import View
from django.template.loader import render_to_string
from langchain_ollama.llms import OllamaLLM
from langchain_core.runnables import RunnableSequence
from langchain.prompts import PromptTemplate
import numpy as np
import re,json
from django.http import HttpResponse


def prompt_model(data,prompt):
    try:
        llm = OllamaLLM(model="deepseek-r1:1.5b")
        template = """
        Given the following product data:
        {product_info}

        Answer the following query: "{user_prompt}"
        Return your answer as a single JSON list of product PKs (integers) that satisfy the query.
        If no products match, return an empty list: []
        """
        prompt_template = PromptTemplate(input_variables=["product_info", "user_prompt"], template=template)
        chain = RunnableSequence(prompt_template | llm)
        response = chain.invoke({"product_info": data, "user_prompt": prompt})
        print(response)
        json_match = re.search(r'\[.*?\]', response, re.DOTALL)
        print(json_match)
        if not json_match:
            raise ValueError("No valid JSON list found in LLM response")
        
        json_str = json_match.group(0)
        print(f"Extracted JSON string: {json_str}")
        
        pk_list = json.loads(json_str)
        print(f"Parsed PK list: {pk_list}")
        return pk_list
    except Exception as e:
        return f"Error processing the request: {str(e)}"

class Result(View):
    def post(self,request):
        prompt = request.POST.get('prompt')
        print(prompt)
        with open("product_data.txt", 'r') as f:
            product_data = f.read().strip()
            
            # Execute the LLM query
        result = prompt_model(product_data, prompt)
        print(result)
        matching_products = Product.objects.filter(pk__in=result)
        print(matching_products)
        products = {'product':matching_products}
        html = render_to_string('products/products_partial.html',products)
        return HttpResponse(html)

        
        

