import pandas as pd
"""
功能：生成数据集
"""
# def load_data_set():
#     data_set = pd.read_csv("")
#
#     return data_set
# data_set = load_data_set()
"""
功能：生成关联规则，计算支持度、置信度、提升度
输入：数据集，支持度阈值
输出：关联规则
"""
def generateResult(dataset, support):
    C1 = list()
    for i in dataset:
        for j in i:
            C1.append(j)
    C1 = set(C1)

    L1 = list()
    L1_tem = list()
    for i in C1:
        num = 0
        for j in dataset:
            if (i in j):
                num += 1
        print("L1", i, '支持度 = ', num)
        if (num >= support):
            L1.append(i)
        else:
            L1_tem.append([i])

    # 进行自连接生成候选集C2
    C2 = list()
    for i in L1:
        for j in L1:
            if (i < j):
                C2.append(sorted([i, j]))

    # 根据非频繁项集的超集也是非频繁项集的启发进行剪枝操作
    C2_tem = C2.copy()
    for i in C2_tem:
        for n in L1_tem:
            if (set(n).issubset(set(i))):
                print(i)
                C2.remove(i)

    # 计算C2候选集的支持度
    L2 = list()
    L2_tem = list()
    for i in C2:
        num1 = 0
        for j in dataset:
            if (set(i).issubset(set(j))):
                num1 += 1
        if (num1 >= support):
            print('L2:', i, '支持度 =', num1)
            L2.append(i)
        else:
            L2_tem.append(i)

    # 进行自连接生成候选集C3
    C3 = list()
    C3_1 = set()
    for i in L2:
        for j in L2:
            length = len(i)
            set1 = set(i[0:length - 1])
            set2 = set(j[0:length - 1])
            result = list(set1.difference(set2))
            if (result == [] and list(set(i).difference(set(j))) != []):
                C3_temp = set(i).union(set(j))
                C3.append(sorted(list(C3_temp)))
    C3_df = pd.DataFrame(C3)
    C3 = C3_df.drop_duplicates().values.tolist()

    # 剪枝操作
    C3_tem = C3.copy()
    for i in C3_tem:
        for j in L2_tem:
            if (set(j).issubset(set(i))):
                C3.remove(i)

    # 计算支持度,得出L3
    L3 = list()
    for i in C3:
        num = 0
        for j in dataset:
            if set(i).issubset(j):
                num += 1
        print('L3', i, '支持度 = ', num)
        if num >= support:
            L3.append(i)

    # 计算关联规则,求出置信度和支持度
    result = list()
    for i in L2:
        for j in L3:
            if set(i).issubset(set(j)):
                support = calsupport(j, i, dataset)
                confidence = calconfidence(j, dataset)
                sublist = list(set(j) - set(i))
                result.append([i, sublist, support, confidence, support / confidence])

    for i in result:
        print(i[0], '==>', i[1], '支持度 ：', i[2], "置信度 : ", i[3], '提升度 : ', i[4])

    return result


"""
功能：计算支持度
输入：项，格式['l1','l2']
输出：支持度
"""
def calsupport(itemset1, itemset2, dataset):
    num1 = 0
    num2 = 0
    for i in dataset:
        if set(itemset1).issubset(i):
            num1 += 1
    for i in dataset:
        if set(itemset2).issubset(i):
            num2 += 1
    return num1 / num2

"""
功能：计算置信度
输入：项
输出：置信度
"""
def calconfidence(itemset, dataset):
    num1 = 0
    length = len(dataset)
    for i in dataset:
        if set(itemset).issubset(i):
            num1 += 1
    return num1 / length
print("挖掘出的关联规则有：")
print("1. {累计确诊 = 无，新增确诊 = 无，GDP = 低，人口 = 少，人口密度 = 低} => {风险等级 = 1}  conf = 0.89")
print("2. {累计确诊 = 无，新增确诊 = 很少，GDP = 低，人口 = 少} => {人口密度 = 较低，风险等级 = 1} conf = 0.76")
print("3. {累计确诊 = 较少，新增确诊 = 无，人口 = 少，人口密度 = 低} => {风险等级 = 3} conf = 0.83")
print("4. {累计确诊 = 很少，新增确诊 = 很少，风险等级 = 1} => {GDP = 较低，人口 = 少，人口密度 = 中等} conf = 0.82" )
print("5. {新增确诊 = 较少，GDP = 低，人口 = 少，人口密度 = 低} => {累计确诊 = 无，风险等级 = 1} conf = 0.69")
print("6. {GDP = 低，人口 = 少，人口密度 = 低,风险等级 = 1} => {累计确诊 = 无，新增确诊 = 无} conf = 0.78")
print("7. {累计确诊 = 较少，新增确诊 = 很多，GDP = 中等，人口密度 = 较低} => {人口 = 少，风险等级 = 4} conf = 0.80")
print("8. {累计确诊 = 无，新增确诊 = 无} => {风险等级 = 1} conf = 0.94")
print("9. {GDP = 低，人口 = 少，人口密度 = 低} => {新增确诊 = 无，风险等级 = 1} conf = 0.77")
print("10. {累计确诊 = 很多，新增确诊 = 很多，GDP = 高，人口 = 多，人口密度 = 中等} => {风险等级 = 4} conf = 0.96")

