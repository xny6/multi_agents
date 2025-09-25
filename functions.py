import requests
import re
import json
import os
import re
import time
from tqdm import tqdm
from sql_agent import run_sql_query

def generate_sql_query(model='qwen2', host='http://localhost:11434', user_query=None, kg_agent_response=None):

    prompt = f'''
    ### Role: Manager Agent
    **Mission**: Generate ONLY the [Query for SQL Agent] using [User Query] and [Knowledge Graph Agent Response]. Output must be in the specified format.

    ### Input Structure
    - [User Query]: Original customer question
    - [Knowledge Graph Agent Response]: KG Agent's output containing product information

    ### Processing Rules
    1. **Identify SQL Attributes** (from User Query):
    - Extract ALL attributes matching: price, cost, stock quantity, release date, rating, weight, size, availability, delivery, discount, warranty, status, inventory.
    - If no attributes found, use "specifications" as default
    - Ignore non-SQL attributes (features, problems, technical requirements, other devices) Just focus on SQL-relevant terms
    
    2. **Extract Product Identifiers** (from KG Response):
    - Find ALL product names/models (ignore descriptions, features, dates)
    - Handle formats:
        • Explicit lists: "Product A, Product B, and Product C" → ["Product A", "Product B", "Product C"]
        • Implicit references: "the XPhone series" → ["XPhone series"]
        • Single products: "our flagship model Z10" → ["Z10"]

    3. **Construct SQL Query**:
    - Template: `Get name and [ATTRIBUTES] of [PRODUCTS] or similar products`
    - Always include `name` as first attribute
    - Always append `or similar products` clause

    ### Examples
    ***[User Query]: Does Phone 12 supports fast charging, and what is the release date of it?***
    ***[Knowledge Graph Agent Response]: Yes, accorfing to the description, the product Phone 12 supports fast charging***
    ***[Query for SQL Agent]: Get name and release date of Phone 12 or similar products***

    ***[User Query]: I found that you have a new device which supports foldable screen, can you tell me how much is it?***
    ***[Knowledge Graph Agent Response]: The device with a foldable screen is the XPhone 15 Pro, XPhone 15 Pro Max and XPhone 15 Pro Ultra. They are all new released in 2024, with lots of new features.***
    ***[Query for SQL Agent]: Get name and price of XPhone 15 Pro, XPhone 15 Pro Max, XPhone 15 Pro Ultra or similar products***

    ***[User Query]: Does Nothing Phone 1 supports wireless charging, and what is the release date of it?***
    ***[Knowledge Graph Agent Response]: Yes, the Nothing Phone 1 supports wireless charging via Qi-certified chargers, allowing convenient and efficient recharging without the need for cables. This feature provides users with a seamless charging experience that complements its advanced features and compatibility with various charging technologies.\n\n[DC] [unknown_source]\n\nReferences:\n- [DC]***
    ***[Query for SQL Agent]: Get name and release date of Nothing Phone 1 or similar products***

    ### Special Cases Handling
    - If User Query mentions multiple attributes:
    'Ask infromation about the topic in the SQL database, such as price, stock, quantity, color, rating, weight, size, availability, delivery, discount, warranty, status, inventory, shipping, capacity.'
    - If KG mentions NO products:  
    `Get name and [ATTRIBUTES] of products matching "[KEY PHRASE]" or similar products`
    - If multiple attribute types:  
    `Get name, attribute1, attribute2 of [PRODUCTS] or similar products`
    - If ambiguous references:  
    `Get name and [ATTRIBUTES] of "[KG DESCRIPTOR]" products or similar`

    '''
    full_prompt = (f'''{prompt} \n\n'''
                   f''' Now, do this for user_query: {user_query}''' 
                   f''' and kg_agent_response: {kg_agent_response}''' 
                   f''' Please Only return the SQL query in natural language with one sentence. Do not include any other information.''' )

    url = f'{host}/api/generate'
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"❌ 出错：{e}"




def generate_kg_query(model='qwen2', host='http://localhost:11434', user_query=None):

    prompt = f"""
    ### Role: Manager Agent
    **Mission**: Analyze the [User Query] and generate ONLY the [Query for Knowledge Graph Agent]. Output must be a single, focused question.

    ### Agent Responsibilities
    | Agent Type          | Scope of Work                          | Examples of Data                    |
    |---------------------|----------------------------------------|-------------------------------------|
    | **KG Agent**        | Product features/solutions/technical details | Feature descriptions, troubleshooting guides, compatibility specs, usage instructions |
    | **SQL Agent**       | Discrete business/product data         | Prices, stock quantities, order status, ratings, specifications |

    ### Critical Thinking Process
    1. **Identify Core KG Element**  
    Extract **EXACTLY ONE** of these from [User Query]:
    - 🔍 `Product Feature` (e.g., "foldable screen", "waterproof")
    - ⚠️ `Problem Scenario` (e.g., "battery drains fast")
    - 🧩 `Technical Requirement` (e.g., "compatible with iOS 16")

    2. **Purify Query**  
    Remove ALL SQL-related elements:
    - ✂️ Numeric terms (price/quantity/rating/size)
    - ✂️ Business terms (order/stock/discount/availability)
    - ✂️ Comparison terms (cheapest/most popular/highest rated)

    3. **Construct KG Query**  
    Format: `[Action Phrase] + [KG Element]`  
    - ✅ **Valid Patterns**: 
        - "Which products support [feature]?"
        - "What are solutions for [problem]?"
        - "How does [feature] work with [requirement]?"
        - If the user query contains specific product names, include them in the query.
    - ❌ **Forbidden**: 
        - Any mention of price/quantity/rating/release date/supplier/weight
        - Compound questions

    ### Transformation Examples
    | User Query                                                        | KG Element           | Query for KG Agent                          |
    |-------------------------------------------------------------------|----------------------|---------------------------------------------|
    | "I found a new device with foldable screen, how much is it?"      | foldable screen      | Which devices support foldable screen?      |
    | "Smartphones with 120Hz display, what's the stock quantity?"      | 120Hz display        | Which smartphones have 120Hz display?       |
    | "Laptop overheating during gaming, can I get refund?"             | overheating          | What are solutions for laptop overheating?  |
    | "Wireless earbuds with ANC, what's the average rating?"           | ANC                  | Which wireless earbuds support ANC?         |
    | "Camera with 4K video stabilization, what colors are available?"  | 4K video stabilization | Which cameras support 4K video stabilization? |
    """


    full_prompt = (f'''{prompt} \n\n'''
                   f''' Now, do this for user_query: {user_query}'''
                   f''' Please Only return the query for Knowledge Graph Agent in natural language. Do not include any other information.''' )

    url = f'{host}/api/generate'
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"❌ 出错：{e}"


def summary_response(model='deepseek-r1:32b', host='http://localhost:11434', user_query='', sql_answer='', kg_answer=''):


    prompt = f'''
    ### Role: Customer Service Agent
    **Mission**: Combine SQL Agent data and KG Agent knowledge to provide rich, coherent responses to user queries.

    ### Input Structure
    1. **[User Query]**: Original customer question
    2. **[SQL Agent Response]**: Structured data (products, orders, specifications)
    3. **[Knowledge Graph Agent Response]**: Descriptive content (solutions, features, guides)

    ### Response Guidelines
    1. **Tone & Style**:
    - Professional yet friendly (use "you/your" not "the user")
    - Concise but comprehensive (2-4 sentences)
    - Use markdown for readability (bold key terms, line breaks)

    2. **Content Integration**:
    - Combine SQL data and KG insights naturally
    - Avoid redundancy (do not repeat information)
    - If there is conflicting info, please flexibly integrate

    3. **Response Structure**:
    - **Acknowledge**: Briefly restate query
    - **Answer**: Combine SQL data + KG context
    - **Value-add**: Suggest next steps or related info

    ### Examples
    [User Query]: What's the battery life of your noise-cancelling headphones?
    [SQL Agent Response]: Product: SoundSilencer Pro, Battery: 40 hours
    [KG Agent Response]: Our ANC headphones feature adaptive battery optimization. Actual usage varies (30-50 hrs) based on ANC intensity.
    [Final Response]: For our SoundSilencer Pro noise-cancelling headphones, you'll typically get around 40 hours of battery life according to product specs. With our adaptive power optimization (as described in the product guide), this can range from 30-50 hours depending on your noise-cancellation settings. Would you like tips to maximize battery life?

    [User Query]: How do I troubleshoot my foldable phone's screen flickering?
    [SQL Agent Response]: Model: XFold Pro, Warranty: Active
    [KG Agent Response]: For foldable screens: 1) Update OS 2) Run display calibration 3) Avoid extreme temperatures
    [Final Response]: For your XFold Pro's screen flickering, I recommend:

    Updating to the latest OS version

    Running display calibration (Settings > Display > Calibrate)

    Keeping the device at room temperature
    Since your warranty is active, we can expedite service if this persists.
    '''

    full_prompt = (f'''{prompt} \n\n'''
                f''' Now, do this for user_query: {user_query}, sql_answer: {sql_answer}, kg_answer: {kg_answer}''' 
                f''' Please return the final response in natural language, do not return any other information.''' )

    url = f'{host}/api/generate'
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"❌ 出错：{e}"




def process_kg_sql(model_name,input_file, output_file):
    """
    处理知识图谱到SQL的转换任务，并将结果保存到指定文件中。

    参数:
        input_file (str): 输入文件路径，包含原始数据。
        output_file (str): 输出文件路径，用于保存处理后的数据。
    """
    # 读取原始输入
    with open(input_file, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    while True:
        # 如果已处理文件存在，加载；否则为空列表
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                processed_data = json.load(f)
        else:
            processed_data = []

        # 获取已处理的 "User Query" 集合
        processed_queries = set(item.get("User Query", "") for item in processed_data)

        # 筛选未处理的项
        unprocessed_items = [item for item in all_data if item.get("User Query", "") not in processed_queries]

        print(f"\n🔍 Still {len(unprocessed_items)} unprocessed items out of {len(all_data)} total.")

        # 如果全部处理完毕，退出循环
        if not unprocessed_items:
            print("\n✅ All items processed successfully!")
            break

        # 使用 tqdm 展示进度条
        for item in tqdm(unprocessed_items, desc="🚀 Processing", unit="item"):
            user_query = item.get("User Query", "")
            KG_Query = item.get("KG Query", "")
            KG_Result = item.get("KG Result", "")

            try:
                SQL_Query = generate_sql_query(model=model_name, user_query=user_query, kg_agent_response=KG_Result)
                SQL_Query = re.sub(r'<think>.*?</think>', '', SQL_Query, flags=re.DOTALL)

                SQL_Result = run_sql_query(question=SQL_Query)

                Summary_Result = summary_response(
                    model=model_name,
                    user_query=user_query,
                    sql_answer=SQL_Result,
                    kg_answer=KG_Result
                )
                Summary_Result = re.sub(r'<think>.*?</think>', '', Summary_Result, flags=re.DOTALL)

                # 添加处理结果
                processed_data.append({
                    "User Query": user_query,
                    "SQL Query": SQL_Query,
                    "SQL Result": SQL_Result,
                    "KG Query": KG_Query,
                    "KG Result": KG_Result,
                    "Summary Result": Summary_Result
                })

                # 写入文件（每个 item 后写一次，避免中断丢数据）
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(processed_data, f, ensure_ascii=False, indent=4)

            except Exception as e:
                print(f"\n❌ Error processing query: {user_query}")
                print(f"   Reason: {e}")
                continue

        # 每轮处理后等待一小段时间，防止重复频繁触发
        time.sleep(1)




def query_ollama_for_user_name(model='qwen2', host='http://localhost:11434', user_query=None):
    """
    Query the Ollama model to extract the user's name from the user query.
    
    Args:
        model (str): The model name to use for querying.
        host (str): The host URL for the Ollama API.
        user_query (str): The user query containing the user's name.
        
    Returns:
        str: The extracted user's name.
    """
    prompt = f'''I will give you the user query, you will return the name of the user'''
    full_prompt = (f'''{prompt} \n\n'''
                   f''' Now, do this for user_query: {user_query}''' 
                   f''' Please return the user's name. Do not include any other information.''' )

    url = f'{host}/api/generate'
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"❌ 出错：{e}"

def query_ollama_for_date(model='qwen2', host='http://localhost:11434', user_query=None):
    """
    Query the Ollama model to extract the date from the user query.
    
    Args:
        model (str): The model name to use for querying.
        host (str): The host URL for the Ollama API.
        user_query (str): The user query containing the date.
        
    Returns:
        str: The extracted date.
    """
    prompt = f'''
    I will give you the user query, you will return the date in YYYY-MM-DD format

    ***Example***
    [User Query]:I return a product on 2025-05-02. How do I use the flashlight on the Watch Pro?
    [Date]: 2025-05-02
    '''
    full_prompt = (f'''{prompt} \n\n'''
                   f''' Now, do this for user_query: {user_query}''' 
                   f''' Please return the date in YYYY-MM-DD format. Do not include any other information.''' )

    url = f'{host}/api/generate'
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"❌ 出错：{e}"



def generate_sql_query_name(user_name):
    """
    Generate a SQL query to get purchase date, products, warranty status and manufacturing batch ID for the user's order.
    
    Args:
        user_name (str): The name of the user.
        
    Returns:
        str: The generated SQL query.
    """
    sql_template = '''Get purchase date, products, price and warranty status for {user_name}\'s order, check them in products, orders, order_items and customers tables.'''
    return sql_template.format(user_name=user_name)

def generate_sql_query_date(date):
    sql_template="Get the product name in return form where return date is {date}"
    return sql_template.format(date=date)

kg_query_prompt = '''
        You are a helpful manager agent, who can divided the work between a SQL Agent and Knowledge Graph Agent to help the user. You will receive [User Query] and [SQL Agent Response] as input, generate [Query for Knowledge Graph Agent] as output.
        ****Example:****
        ***[User Query]: [My XPhone 15 Pro is randomly restarting. Is this a known issue for my specific phone, and what can I do?]
        ***[SQL Agent Response]: {[
        {
            "order_date":"2025-1-13",
            "product_name":"XPhone 15 Pro",
            "warranty_status":"In Warranty",
            "manufacturing_batch_id":"BATCH-X15P-2025-Q2-612"
        },
        {
            "order_date":"2025-1-13",
            "product_name":"XBook Air",
            "warranty_status":"In Warranty",
            "manufacturing_batch_id":"BATCH-X15P-2025-Q2-612"
        }
        ] }
        ***[Query for Knowledge Graph Agent]: [Find Restart Issues related to Product 'XPhone 15 Pro', and their associated Troubleshooting Steps.]

        Here is the thinking process:
        1. Find the key element and topic in [user query], which is "XPhone 15 Pro" and "randomly restarting".
        2. Find the key element and ignore the irrelevant elements in [SQL Agent response]. Key elements are "XPhone 15 Pro" and "In Warranty". Ignore irrelevant elements like "XBook Air".
        3. Combine the [user query] and [SQL Agent response] to form a query for the Knowledge Graph Agent. 
        
        Now, do this for the following input:
        '''

def generate_kg_query_sql_kg(prompt=kg_query_prompt, model='qwen2', host='http://localhost:11434', user_query=None, sql_agent_response=None):


    full_prompt = (f'''{prompt} \n\n'''
                f''' user_query: {user_query}, sql_agent_response: {sql_agent_response}''' 
                f''' Please return the query in natural language, do not return any other information.''' )
    url = f'{host}/api/generate'
    payload = {
        "model": model,
        "prompt": full_prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"❌ 出错：{e}"
    


def sql_kg_process_date(input_file, output_file,model_name):
    """
    处理用户查询，将其转换为 SQL 查询和 KG 查询，并保存结果到 JSON 文件。

    参数:
        input_file (str): 包含用户查询的输入文件路径。
        output_file (str): 保存处理结果的输出文件路径。
    """
    # 加载原始 user_queries
    with open(input_file, 'r', encoding='utf-8') as file:
        user_queries = [line.strip() for line in file if line.strip()]

    # 加载已处理数据（如存在）
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            processed_data = json.load(f)
    else:
        processed_data = []

    # 提取已处理的 user queries
    processed_queries = set(item.get("User Query", "") for item in processed_data)

    # 过滤未处理的 user queries
    unprocessed_queries = [uq for uq in user_queries if uq not in processed_queries]

    print(f"🔍 Total: {len(user_queries)} queries, {len(unprocessed_queries)} left to process.")

    while True:
        # 过滤未处理的 user queries
        unprocessed_queries = [uq for uq in user_queries if uq not in set(item.get("User Query", "") for item in processed_data)]
        if not unprocessed_queries:
            print("✅ All queries processed!")
            break
        print(f"🔍 {len(unprocessed_queries)} queries left to process.")
        for user_query in tqdm(unprocessed_queries, desc="Processing queries", unit="query"):
            try:
                date = query_ollama_for_date(model=model_name,user_query=user_query)
                date = re.sub(r'<think>.*?</think>', '', date, flags=re.DOTALL)
                SQL_Query = generate_sql_query_date(date)
                SQL_Result = run_sql_query(question=SQL_Query)
                KG_Query = generate_kg_query_sql_kg(
                    model=model_name,
                    user_query=user_query,
                    sql_agent_response=SQL_Result
                )
                KG_Query = re.sub(r'<think>.*?</think>', '', KG_Query, flags=re.DOTALL)
                result = {
                    "User Query": user_query,
                    "SQL Query": SQL_Query,
                    "SQL Result": SQL_Result,
                    "KG Query": KG_Query,
                    "KG Result": "",
                    "Summary Result": ""
                }
                processed_data.append(result)
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(processed_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"❌ Error processing '{user_query}': {e}")
                print("🔁 Skipping to next...")
                continue
            
def sql_kg_process_name(input_file, output_file,model_name):
    """
    处理用户查询，将其转换为 SQL 查询和 KG 查询，并保存结果到 JSON 文件。

    参数:
        input_file (str): 包含用户查询的输入文件路径。
        output_file (str): 保存处理结果的输出文件路径。
    """
    # 加载原始 user_queries
    with open(input_file, 'r', encoding='utf-8') as file:
        user_queries = [line.strip() for line in file if line.strip()]

    # 加载已处理数据（如存在）
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf-8') as f:
            processed_data = json.load(f)
    else:
        processed_data = []

    # 提取已处理的 user queries
    processed_queries = set(item.get("User Query", "") for item in processed_data)

    # 过滤未处理的 user queries
    unprocessed_queries = [uq for uq in user_queries if uq not in processed_queries]

    print(f"🔍 Total: {len(user_queries)} queries, {len(unprocessed_queries)} left to process.")

    while True:
        # 过滤未处理的 user queries
        unprocessed_queries = [uq for uq in user_queries if uq not in set(item.get("User Query", "") for item in processed_data)]
        if not unprocessed_queries:
            print("✅ All queries processed!")
            break
        print(f"🔍 {len(unprocessed_queries)} queries left to process.")
        for user_query in tqdm(unprocessed_queries, desc="Processing queries", unit="query"):
            try:
                name = query_ollama_for_user_name(model=model_name,user_query=user_query)
                name = re.sub(r'<think>.*?</think>', '', name, flags=re.DOTALL)
                SQL_Query = generate_sql_query_name(name)
                SQL_Result = run_sql_query(question=SQL_Query)
                KG_Query = generate_kg_query_sql_kg(
                    model=model_name,
                    user_query=user_query,
                    sql_agent_response=SQL_Result
                )
                KG_Query = re.sub(r'<think>.*?</think>', '', KG_Query, flags=re.DOTALL)
                result = {
                    "User Query": user_query,
                    "SQL Query": SQL_Query,
                    "SQL Result": SQL_Result,
                    "KG Query": KG_Query,
                    "KG Result": "",
                    "Summary Result": ""
                }
                processed_data.append(result)
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(processed_data, f, ensure_ascii=False, indent=4)
            except Exception as e:
                print(f"❌ Error processing '{user_query}': {e}")
                print("🔁 Skipping to next...")
                continue
            

def add_summary_to_json(input_file, output_file, model_name):
    with open(input_file, 'r') as f:
        data = json.load(f)
    result = []
    for item in data:
        user_query = item.get("User Query", "")
        sql_answer = item.get("SQL Result", "")
        kg_answer = item.get("KG Result", "")
        response = summary_response(model=model_name, user_query=user_query, sql_answer=sql_answer, kg_answer=kg_answer)
        response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        print(f"Response: {response}")
        item["Summary Result"] = response
        result.append(item)
    with open(output_file, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)