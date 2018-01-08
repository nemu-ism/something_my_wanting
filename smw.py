import json
import sys
import generator_url

# sys.argv = terminal入力
args = sys.argv

def load_json(d):
    data = json.loads(d)
    return data

def print_list(data):
    hits_total = int(data["ResultSet"]["totalResultsAvailable"])
    hits_offset = int(data["ResultSet"]["firstResultPosition"])
    item_list = data["ResultSet"]["0"]["Result"]
    results = {}
    for k, v in item_list.items():
        try:
            number = int(v["_attributes"]["index"])
            name = v["Name"]
            url = v["Url"]
            condition = v["Condition"]
            price = int(v["Price"]["_value"])
            rate_average = v["Review"]["Rate"]
            rate_count = int(v["Review"]["Count"])
            results[number] = [name, condition, price, rate_average, rate_count, url]
        except:
            if k == "Request":
                query = v["Query"]

    dic = generator_url.generator_dic(args[1:])
    print(dic)
    print('-' * 40)
    if 'sort' in dic:
        print(dic['sort'], end='')
    print('検索ワード：', query)
    if 'condition' in dic:
        print('状態:{:} only'.format(dic['condition']))
    if 'price_from' or 'price_to' in dic:
        print('価格：', end='')
        if 'price_from' in dic:
            print('{:,}円から'.format(int(dic['price_from'])), end='')
        if 'price_to' in dic:
            print('{:,}円まで'.format(int(dic['price_to'])), end='')
        print('')
    print('{0:,}件中　{1:,}～{2:,}件'.format(hits_total, hits_offset, hits_offset+9))
    print('-' * 40)

    results_keys = list(results.keys())
    results_keys.sort()
    for i in results_keys:
        print(i, results[i][0])
        print(' ' *6, results[i][1], '{:,}円(税込)'.format(results[i][2]),
              '平均評価{0:}点({1:,}人中)'.format(results[i][3], results[i][4]))
        print(' ' *6, '商品ページ：', results[i][5])

# main
if __name__ == '__main__':
    try:
        requests = args[1:]
        json_generated = generator_url.generator_json(requests)
        print_list(load_json(json_generated))
    except:
        print("リクエスト内容に誤りがありました。リクエスト内容を確認してください。")
        sys.exit()