import os 
from openai import OpenAI 
import streamlit as st 
from dotenv import load_dotenv 
 
# 環境変数読み込み 
load_dotenv() 
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 
 
def get_recipes(items): 
    prompt = f""" 
    冷蔵庫にある食材: {items} 
    条件: 
    - 簡単・早く・楽に作れる料理を3つ提案 
    - 各料理ごとに「料理名」「必要な追加食材」「作り方（3ステップ以内）」を記載 
    出力は以下の形式で: 
    --- 
    料理名: ○○ 
    追加食材: △△ 
    作り方: 
    1. ... 
    2. ... 
    3. ... 
    --- 
    """ 
 
    response = client.chat.completions.create( 
        model="gpt-4o-mini", 
        messages=[{"role": "user", "content": prompt}], 
    ) 
 
    return response.choices[0].message.content.strip() 
 
# Streamlit UI 
st.title("簡単・早いレシピ提案AI") 
 
# セッションステートでレシピと選択状態を管理 
if "recipes" not in st.session_state: 
    st.session_state.recipes = {} 
if "selected_recipe" not in st.session_state: 
    st.session_state.selected_recipe = None 
 
# 材料入力欄 
items = st.text_input("材料を入力", "") 
 
# 検索ボタン 
if st.button("検索"): 
    recipes_text = get_recipes(items) 
    recipes = recipes_text.split("---") 
    recipe_dict = {} 
    for r in recipes: 
        if "料理名:" in r: 
            lines = r.strip().split("\n") 
            name = lines[0].replace("料理名:", "").strip() 
            recipe_dict[name] = "\n".join(lines[1:]).strip() 
    st.session_state.recipes = recipe_dict 
    st.session_state.selected_recipe = None 
 
# 料理候補がある場合 
if st.session_state.recipes: 
    # プルダウンで料理選択 
    selected = st.selectbox( 
        "料理を選んでください", 
        list(st.session_state.recipes.keys()), 
        index=0 if st.session_state.selected_recipe is None else 
list(st.session_state.recipes.keys()).index(st.session_state.selected_recipe), 
        key="selectbox_recipe" 
    ) 
    st.session_state.selected_recipe = selected 
 
# 選択中の料理名を常に表示 
if st.session_state.get("selected_recipe"): 
st.markdown(f"### 選択中の料理: **{st.session_state['selected_recipe']}**") 
st.markdown("---") 
st.subheader(st.session_state.selected_recipe) 
st.text(st.session_state.recipes[st.session_state.selected_recipe])