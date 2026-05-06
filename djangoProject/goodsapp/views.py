from __future__ import unicode_literals
from django.shortcuts import render
from django.views import View
from goodsapp.models import Category, Goods
from django.core.paginator import Paginator
import math
from cartsapp.models import *



class IndexView(View):
    def get(self, request,cid=8,num=1):
        #查询
        cid = int(cid)
        num = int(num)
        categoryList = Category.objects.all()

        goodsList = Goods.objects.filter(Category_id = cid).order_by('id')
        paginator_obj = Paginator(goodsList, 8)
        page_obj = paginator_obj.page(num)
        #页码范围
        begin = num - int(math.ceil(10.0/2))
        if begin < 1:
            begin = 1
        end = begin + 9
        if end > paginator_obj.num_pages:
            end = paginator_obj.num_pages
        if end < 10:
            begin = 1
        else:
            begin = end-9
        page_list = range(begin, end+1)

        return render(request, 'index.html', {'categoryList': categoryList, 'cid':cid,'goodsList':page_obj,'page_list':page_list,'num':num})






from django.shortcuts import render
from django.views import View
from goodsapp.models import Goods, Category
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba
from django.shortcuts import render
from django.views import View
from goodsapp.models import Goods
from cartsapp.models import CartItem
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba

from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import AnonymousUser  # 导入AnonymousUser模型
from goodsapp.models import Goods
from cartsapp.models import CartItem
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba


class DetailView(View):
    def get(self, request, goodsid):
        goodsid = int(goodsid)
        current_goods = Goods.objects.get(id=goodsid)

        # 获取与当前商品相同类别的其他商品作为候选推荐商品
        candidate_recommendations = Goods.objects.filter(Category_id=current_goods.Category_id)

        # 获取用户已经加入购物车的商品ID列表
        if isinstance(request.user, AnonymousUser):
            cart_goods_ids = []
        else:
            cartitems = CartItem.objects.filter(user=request.user)
            cart_goods_ids = [item.goodsid for item in cartitems]

        # 从候选推荐中排除用户购物车中已有的商品
        candidate_recommendations = candidate_recommendations.exclude(id__in=cart_goods_ids)

        # 构建商品的标题和描述文本列表，并进行中文分词
        current_text = [current_goods.gname + " " + current_goods.gdesc]
        candidate_texts = [goods.gname + " " + goods.gdesc for goods in candidate_recommendations]
        current_text = [list(jieba.cut(text)) for text in current_text]
        candidate_texts = [list(jieba.cut(text)) for text in candidate_texts]

        # 使用TF-IDF向量化器处理分词后的文本数据
        vectorizer = TfidfVectorizer(tokenizer=lambda x: x, lowercase=False)
        X = vectorizer.fit_transform(current_text + candidate_texts)

        # 计算当前商品与候选商品的相似度矩阵
        similarities = cosine_similarity(X[0:1], X[1:])

        # 将相似度与候选推荐商品进行配对，并按照相似度降序排列
        similarity_pairs = list(zip(candidate_recommendations, similarities.flatten()[1:]))
        similarity_pairs.sort(key=lambda x: x[1], reverse=True)

        # 整合购物车数据，调整推荐分数
        adjusted_similarity_pairs = []
        for goods, similarity in similarity_pairs:
            if goods.id in cart_goods_ids:
                adjusted_similarity = similarity * 1.2  # 假设对购物车中商品的相似度给予20%的加权
            else:
                adjusted_similarity = similarity
            adjusted_similarity_pairs.append((goods, adjusted_similarity))

        # 提取相似度前四的推荐商品
        recommend_list = [pair[0] for pair in adjusted_similarity_pairs[:4]]

        return render(request, 'detail.html', {'goods': current_goods, 'recommend_list': recommend_list})