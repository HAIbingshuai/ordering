def judgment_void(required_fields, request):
    """
    字段项有无 判断
    :param required_fields: 必须要字段
    :param request: 传入的内容文件
    :return:
    """
    missing_fields = [field for field in required_fields if field not in request.data]
    if missing_fields:
        Res_boo, Res_str = False, f'缺少必需的字段: {", ".join(missing_fields)}'
    else:
        Res_boo, Res_str = True, ''
    return Res_boo, Res_str


def judgment_null(required_fields, request):
    """
    字段项的值 判断
    :param required_fields: 必须要字段
    :param request: 传入的内容文件
    :return:
    """
    # 判断字段存在空值
    empty_fields = [field for field in required_fields if request.data.get(field) in [None, '']]
    if empty_fields:
        Res_boo, Res_str = False, f'字段存在空值: {", ".join(empty_fields)}'
    else:
        Res_boo, Res_str = True, ''
    return Res_boo, Res_str
