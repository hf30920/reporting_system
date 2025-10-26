# 导入情感分析工具
from snownlp import SnowNLP
import csv
# 导入分词处理和词频统计的主函数
from index import main as indexMain,getCommentList
from ciPingTotal import main as ciPingTotalMain
import os

# 生成目标文件（包含评论内容和情感标签）
def targetFile():
    targetFile = 'target.csv'
    # 获取评论列表
    commentList = getCommentList()

    rateData = []
    good = 0  # 正面评论计数
    bad = 0   # 负面评论计数
    midlle = 0  # 中性评论计数
    # 分析每条评论的情感倾向
    for index, i in enumerate(commentList):
        try:
            # 使用SnowNLP进行情感分析
            value = SnowNLP(i[4]).sentiments
            if value > 0.5:
                good += 1
                rateData.append([i[4], '正面'])
            elif value == 0.5:
                midlle += 1
                rateData.append([i[4], '中性'])
            elif value < 0.5:
                bad += 1
                rateData.append([i[4], '负面'])
        except:
            continue

    # 将分析结果写入目标文件
    for i in rateData:
        with open(targetFile, 'a+', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(i)

# 主函数，执行完整的舆情分析流程
def main():
    try:
        # 删除旧的结果文件
        os.remove('./target.csv')
        os.remove("./comment_1_fenci.txt")
        os.remove("./comment_1_fenci_qutingyongci_cipin.csv")
    except:
        pass
    # 执行分词处理
    indexMain()
    # 执行词频统计
    ciPingTotalMain()
    # 生成目标文件
    targetFile()

# 当作为主程序直接运行时，执行主函数
if __name__ == '__main__':
    main()