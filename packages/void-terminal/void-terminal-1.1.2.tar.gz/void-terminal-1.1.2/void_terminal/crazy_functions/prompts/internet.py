SearchOptimizerPrompt="""As a web search assistant，Your task is to combine historical records，From different perspectives，Generate different versions of `search terms` for the `original question`，To improve the accuracy of webpage retrieval。The generated question requires clear and specific references to the object，And in the same language as the original question。For example：
History record: 
"
Q: Conversation background。
A: The current conversation is about the introduction of Nginx and its use on Ubuntu, etc.。
"
Original question: How to download
Search term: ["Nginx 下载","Ubuntu Nginx","UbuntuInstallationNginx"]
----------------
History record: 
"
Q: Conversation background。
A: The current conversation is about the introduction and use of Nginx, etc.。
Q: 报错 "no connection"
A: 报错"no connection"可能是因为……
"
Original question: How to solve
Search term: ["Nginx报错"no connection" 解决","Nginx'no connection'报错 原因","Nginxprompt'no connection'"]
----------------
History record:
"

"
Original question: Do you know Python?？
Search term: ["Python","Python Use教程。","Python 特点and优势"]
----------------
History record:
"
Q: List three characteristics of Java？
A: Java is a compiled language。
   Java is an object-oriented programming language。
   3. Java is a cross-platform programming language。
"
Original question: Introduce the second point。
Search term: ["Java 面To对象特点","Java 面To对象programming优势。","Java 面To对象programming"]
----------------
Now there is a history record:
"
{history}
"
Has its original question: {query}
Directly provide up to {num} search terms，Must be provided in JSON format，No extra characters allowed:
"""

SearchAcademicOptimizerPrompt="""As an academic paper search assistant，Your task is to combine historical records，From different perspectives，Generate different versions of `search terms` for the `original question`，To improve the accuracy of academic paper retrieval。The generated question requires clear and specific references to the object，And in the same language as the original question。For example：
History record: 
"
Q: Conversation background。
A: The current conversation is about the introduction of deep learning and its applications in image recognition, etc.。
"
Original question: How to download related papers
Search term: ["深度学习 图像识别 Paper下载","图像识别 深度学习 研究Paper","深度学习 图像识别 Paper资源","Deep Learning Image Recognition Paper Download","Image Recognition Deep Learning Research Paper"]
----------------
History record: 
"
Q: Conversation background。
A: The current conversation is about the introduction and applications of deep learning。
Q: 报错 "Model不收敛"
A: 报错"Model不收敛"可能是因为……
"
Original question: How to solve
Search term: ["深度学习 Model不收敛 解决方案 Paper","深度学习 Model不收敛 原因 研究","深度学习 Model不收敛 Paper","Deep Learning Model Convergence Issue Solution Paper","Deep Learning Model Convergence Problem Research"]
----------------
History record:
"

"
Original question: Do you know about GAN?？
Search term: ["生成对抗网络 Paper","GAN Use教程 Paper","GAN 特点and优势 研究","Generative Adversarial Network Paper","GAN Usage Tutorial Paper"]
----------------
History record:
"
Q: List three applications of machine learning？
A: 1. The application of machine learning in image recognition。
   Applications of machine learning in natural language processing。
   3. Application of machine learning in recommendation systems。
"
Original question: Introduce the second point。
Search term: ["机器学习 自然语言处理 应用 Paper","机器学习 自然语言处理 研究","机器学习 NLP 应用 Paper","Machine Learning Natural Language Processing Application Paper","Machine Learning NLP Research"]
----------------
Now there is a history record:
"
{history}
"
Has its original question: {query}
Directly provide up to {num} search terms，Must be provided in JSON format，No extra characters allowed:
"""