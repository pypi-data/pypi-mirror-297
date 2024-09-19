from langchain.agents import load_tools, initialize_agent
from langchain.llms import OpenAI
import ast

class search_engine:
    def __init__(self, model):
        tools = load_tools(["google-serper"])
        self.agent = initialize_agent(tools, model, agent="zero-shot-react-description", verbose=False)

    def assets(assets_array, prompt=None):
        if prompt is None:
            search_asset_prompt = """
            Please look up the instrument %s with ISIN %s and provide the details in the following format:
            {
            'Asset class': 'Equity/Bond/Money Market/Alternatives/Other',
            'Currency': 'USD/EUR/Other',
            'Country': 'ISO code (e.g., US, FR)'
            'Market': 'emerging markets/developed markets/Other',
            'Rating': 'government bond/high yield/investment grade/Other'
            }
            """
        else:
            search_asset_prompt = prompt

        items = []
        for item in assets_array:
            try:
                response = agent.run(search_asset_prompt % (item['id'], item['isin']))
                item = {**{'Isin':item['isin'], 'Name':item['id']}, **ast.literal_eval(response)}
            except Exception as e:
                item = {'Isin':item['isin'], 'Name':item['id'], 'Asset class':'', 'Currency':'', 'Country':'', 'Market':'', 'Rating':''}
                print(f'Cannot identify instrument:{str(e)}')
            items.append(item)
        
        return pd.DataFrame(items)