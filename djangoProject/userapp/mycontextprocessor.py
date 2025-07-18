import jsonpickle

def getSessionInfo(request):
    suser = request.session.get('user', '')
    try:
        if suser:
            # 尝试反序列化用户数据
            user = jsonpickle.loads(suser)
            return {'user': user}
    except jsonpickle.JsonpickleError:
        # 如果反序列化失败，返回None或适当的错误信息
        pass
    # 如果会话中没有用户信息或反序列化失败，返回一个空的用户字典
    return {'user': None}