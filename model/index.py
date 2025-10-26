# 导入获取公共数据的工具函数
from utils.getPublicData import getAllCommentsData
# 导入中文分词库 jieba
import jieba
# 导入 jieba 的关键词提取模块
import jieba.analyse as analyse
# 设置分词结果保存的目标文件
targetTxt = 'comment_1_fenci.txt'

# 加载停用词列表
def stopwordslist():
    # 读取停用词表文件，去除每行首尾空格并保存为列表
    stopwords = [line.strip() for line in open('./stopWords.txt',encoding='UTF-8').readlines()]
    return stopwords

# 获取评论数据列表
def getCommentList():
    # 调用 getAllCommentsData 函数获取所有评论数据
    return getAllCommentsData()

# 对句子进行分词并去除停用词
def seg_depart(sentence):
    # 提取评论中的文本内容并连接成字符串，然后进行分词
    # sentence 是评论数据列表，每个评论的第5个元素是评论内容
    sentence_depart = jieba.cut(" ".join([x[4] for x in sentence]).strip())
    # 获取停用词列表
    stopwords = stopwordslist()
    # 初始化输出字符串
    outstr = ''
    # 遍历分词结果，去除停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                outstr += word
    return outstr

# 将分好词的评论写入文件
def writer_comment_fenci():
    # 以追加模式打开目标文件
    with open(targetTxt, 'a+', encoding='utf-8') as targetFile:
        # 对评论进行二次分词，使用精确模式（cut_all=False）
        seg = jieba.cut(seg_depart(getCommentList()), cut_all=False)
        # 分好词后用空格分隔
        output = ' '.join(seg)
        # 写入文件
        targetFile.write(output)
        targetFile.write('\n')
        print('写入成功！')

# 主函数，提取关键词的入口
def main():
    # 调用函数将分好词的评论写入文件
    writer_comment_fenci()

# 当作为主程序直接运行时，执行主函数
if __name__ == '__main__':
    main()

