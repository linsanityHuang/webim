// 获取URL中的查询参数
function get_query_param(name) {
    var url = window.location.href
    var paraString = url.substring(url.indexOf("?") + 1, url.length).split("&")
    var paraObj = {}
    for (var i = 0; i < paraString.length; i++) {
        paraPair = paraString[i]
        let key_ = paraPair.substring(0, paraPair.indexOf("="))
        let value_ = paraPair.substring(paraPair.indexOf("=") + 1, paraPair.length)
        paraObj[key_] = value_
    }
    return paraObj[name]
}