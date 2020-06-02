import streamlit as st
import numpy as np
import pandas as pd
import lightfm as lf
import nmslib
import pickle
import scipy.sparse as sparse


def nearest_items_nms(item_id, index, n=10):
    """ Функция для поиска ближайших соседей, возвращает построенный индекс """
    nn = index.knnQuery(item_embeddings[item_id], k=n)
    return nn


def read_files(folder_name='data'):
    """
    Функция для чтения файлов + преобразование к нижнему регистру
    """
    ratings = pd.read_csv(folder_name + '/rating.csv')
    items = pd.read_csv(folder_name + '/items.csv')
    items['title'] = items.title.str.lower()
    return ratings, items 


def load_embeddings(folder_name='data'):
    """
    Функция для загрузки векторных представлений
    """
    with open(folder_name + '/item_embeddings.pickle', 'rb') as f:
        item_embeddings = pickle.load(f)

    #Используем nmslib, чтобы создать быстрый knn
    nms_idx = nmslib.init(method='hnsw', space='cosinesimil')
    nms_idx.addDataPointBatch(item_embeddings)
    nms_idx.createIndex(print_progress=True)
    return item_embeddings, nms_idx


def id_to_int(ID):
    """ Приводит ID к типу int """
    try:
        ID = int(ID)
        flag = True
    except:
        flag = False
    return ID, flag


def find_recommendations(itemid, items, num_items):
    """ Принимает itemid (int), items (dataframe), num_items (int).
        Возвращает похожие товары в виде датафрейма """
    nearest_items = nearest_items_nms(itemid, nms_idx)[0]
    rec = items[items['itemid'].isin(nearest_items)].sort_values(by='overall_avg', ascending=False).head(num_items)
    rec = rec[['number_ratings', 'category', 'title', 'overall_avg', 'price']]
    rec.rename(columns={'number_ratings': 'n_ratings', 'overall_avg': 'rating'}, inplace=True)
    return rec
    

#Загружаем данные
ratings, items  = read_files() 
item_embeddings, nms_idx = load_embeddings()

st.title('Recommender system')
st.write("The system contains users with identifiers from 0 to 127496 \
and products with identifiers from 0 to 41319. \
If the user exists, then recommendations are given for his last 3 ratings. If the user is new, \
then recommendations are given on the product that he is currently viewing. \
Try entering a nonexistent user in \"User ID\". For example, enter -1 in \"User ID\". \
Then enter the identifier of the product in \"Item ID\".")

#Форма для ввода текста
user_id = st.text_input('User ID', '')
user_id, user_id_is_int = id_to_int(user_id)

if(user_id_is_int == True):
    #Получаем пять последних оценок пользователя
    user_df = ratings[ratings['userid'] == user_id].sort_values(by='reviewTime', ascending=False).head(5)
    len_user_df = len(user_df)
    if len_user_df > 0:
        #Пользователь не новичок 
        user_df = user_df.merge(items, left_on='asin', right_on='asin', how='inner', suffixes=('_left', '_right'))
        user_df = user_df[['reviewTime', 'category', 'title', 'overall', 'itemid_left']]
        user_df.rename(columns={'itemid_left': 'itemid'}, inplace=True)
        
        st.header("User history")
        st.write(user_df)
        list_df = []
        
        st.header("Recommendations")
        for i in range(len_user_df):
            if i > 2:
                break
            #Ищем рекомендации
            item_id = user_df.iloc[i]['itemid']
            rec = find_recommendations(item_id, items, 3)
            if len(rec) > 0:
                list_df.append(rec)
        
        if len(list_df) > 0:
            df = pd.concat(list_df)
            st.table(df)
        else:
            st.write("No recommendations")
    else:
        #Пользователь новичок (холодный старт)
        st.write("This is a new user.")
        #Форма для ввода текста
        item_id = st.text_input('Item ID', '')
        item_id, item_id_is_int = id_to_int(item_id)
        if(item_id_is_int == True):
            #Получаем сведения о товаре
            item_df = items[items['itemid'] == item_id]
            if len(item_df) > 0:
                st.header("About product")
                item_df = item_df[['number_ratings', 'category', 'title', 'overall_avg', 'price']]
                item_df.rename(columns={'number_ratings': 'n_ratings', 'overall_avg': 'rating'}, inplace=True)
                st.table(item_df)
                st.header("Recommendations")
                #Ищем рекомендации
                rec = find_recommendations(item_id, items, 5)
                if len(rec) > 0:
                    st.table(rec)
                else:
                    st.write("No recommendations")
            else:
                st.write("No product with this ID")     
        else:
            st.write("Please enter Item ID (Item ID must be an integer)")
else:
    st.write("Please enter User ID (User ID must be an integer)")
