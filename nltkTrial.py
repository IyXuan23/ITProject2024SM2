import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import stopwords

# 用户查询
user_query = "Whats the contact information for COMP10001?"

# 分词
tokens = word_tokenize(user_query)

# 识别课程代码的正则表达式模式（例如：COMP20008）
course_code_pattern = r'\b[A-Z]{4}\d{5}\b'

# 提取课程代码
course_codes = re.findall(course_code_pattern, user_query)

# 识别复合词（比如 machine learning）
multiword_expressions = [('machine', 'learning'), ('artificial', 'intelligence')]

# 用bigram匹配可能的复合词
bigrams = list(nltk.bigrams(tokens))
compound_keywords = [' '.join(bigram) for bigram in bigrams if bigram in multiword_expressions]

# 词性标注
tagged = pos_tag(tokens)

# 停用词
stop_words = set(stopwords.words('english'))

# 设定词性权重映射
weight_map = {
    'NN': 1.0,    # 名词
    'NNS': 1.0,   # 复数名词
    'VB': 1.5,    # 动词
    'VBP': 1.5,   # 动词
    'VBZ': 1.5,   # 动词
}

# 提取单个关键词并为其分配权重
single_keyword_weights = {word: weight_map.get(pos, 0.5) for word, pos in tagged if pos in weight_map and word.lower() not in stop_words}

# 将复合词添加到关键词中并分配权重
compound_keyword_weights = {kw: 1.7 for kw in compound_keywords}

# 将课程代码加入到关键词中并分配权重
course_code_weights = {code: 2.0 for code in course_codes}  # 为课程代码赋予较高的权重

# 合并所有关键词和权重
keyword_weights = {**single_keyword_weights, **compound_keyword_weights, **course_code_weights}

# 要增加权重的特定词列表
specific_terms = ['prerequisite', 'name', 'code', 'contact']

# 遍历特定词列表并增加权重
for term in specific_terms:
    if term in keyword_weights:
        keyword_weights[term] += 0.5  # 增加这些特定词的权重
# 最终关键词和权重
print(f"关键词及其权重: {keyword_weights}")
