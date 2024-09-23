# From project chatglm-langchain

import os
import os
import uuid
import tqdm
import shutil
import threading
import numpy as np
from void_terminal.toolbox import Singleton
from loguru import logger
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
from typing import List, Tuple
from void_terminal.crazy_functions.vector_fns.general_file_loader import load_file

embedding_model_dict = {
    "ernie-tiny": "nghuyong/ernie-3.0-nano-zh",
    "ernie-base": "nghuyong/ernie-3.0-base-zh",
    "text2vec-base": "shibing624/text2vec-base-chinese",
    "text2vec": "GanymedeNil/text2vec-large-chinese",
}

# Embedding model name
EMBEDDING_MODEL = "text2vec"

# Embedding running device
EMBEDDING_DEVICE = "cpu"

# Context-based prompt template，请务必保留"{question}"and"{context}"
PROMPT_TEMPLATE = """Known Information：
{context}

Based on the Above Known Information，Answer user questions concisely and professionally。If unable to get an answer from it，Please say `Cannot answer the question based on available information` or `Not enough relevant information is provided`，Fabrication is not allowed in the answer，Please answer in Chinese。 The Issue Is：{question}"""

# Length of text segmentation
SENTENCE_SIZE = 100

# Length of single segment context after matching
CHUNK_SIZE = 250

# LLM input history length
LLM_HISTORY_LEN = 3

# return top-k text chunk from vector store
VECTOR_SEARCH_TOP_K = 5

# Knowledge retrieval content relevance score, The numerical range is approximately 0-1100，If it is 0，Will not take effect，After testing, set it to less than 500，More accurate matching results
VECTOR_SEARCH_SCORE_THRESHOLD = 0

NLTK_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "nltk_data")

FLAG_USER_NAME = uuid.uuid4().hex

# Whether to enable cross-domain，Default is False，If needed to enable，Please set to True
# is open cross domain
OPEN_CROSS_DOMAIN = False

def similarity_search_with_score_by_vector(
        self, embedding: List[float], k: int = 4
) -> List[Tuple[Document, float]]:

    def seperate_list(ls: List[int]) -> List[List[int]]:
        lists = []
        ls1 = [ls[0]]
        for i in range(1, len(ls)):
            if ls[i - 1] + 1 == ls[i]:
                ls1.append(ls[i])
            else:
                lists.append(ls1)
                ls1 = [ls[i]]
        lists.append(ls1)
        return lists

    scores, indices = self.index.search(np.array([embedding], dtype=np.float32), k)
    docs = []
    id_set = set()
    store_len = len(self.index_to_docstore_id)
    for j, i in enumerate(indices[0]):
        if i == -1 or 0 < self.score_threshold < scores[0][j]:
            # This happens when not enough docs are returned.
            continue
        _id = self.index_to_docstore_id[i]
        doc = self.docstore.search(_id)
        if not self.chunk_conent:
            if not isinstance(doc, Document):
                raise ValueError(f"Could not find document for id {_id}, got {doc}")
            doc.metadata["score"] = int(scores[0][j])
            docs.append(doc)
            continue
        id_set.add(i)
        docs_len = len(doc.page_content)
        for k in range(1, max(i, store_len - i)):
            break_flag = False
            for l in [i + k, i - k]:
                if 0 <= l < len(self.index_to_docstore_id):
                    _id0 = self.index_to_docstore_id[l]
                    doc0 = self.docstore.search(_id0)
                    if docs_len + len(doc0.page_content) > self.chunk_size:
                        break_flag = True
                        break
                    elif doc0.metadata["source"] == doc.metadata["source"]:
                        docs_len += len(doc0.page_content)
                        id_set.add(l)
            if break_flag:
                break
    if not self.chunk_conent:
        return docs
    if len(id_set) == 0 and self.score_threshold > 0:
        return []
    id_list = sorted(list(id_set))
    id_lists = seperate_list(id_list)
    for id_seq in id_lists:
        for id in id_seq:
            if id == id_seq[0]:
                _id = self.index_to_docstore_id[id]
                doc = self.docstore.search(_id)
            else:
                _id0 = self.index_to_docstore_id[id]
                doc0 = self.docstore.search(_id0)
                doc.page_content += " " + doc0.page_content
        if not isinstance(doc, Document):
            raise ValueError(f"Could not find document for id {_id}, got {doc}")
        doc_score = min([scores[0][id] for id in [indices[0].tolist().index(i) for i in id_seq if i in indices[0]]])
        doc.metadata["score"] = int(doc_score)
        docs.append(doc)
    return docs


class LocalDocQA:
    llm: object = None
    embeddings: object = None
    top_k: int = VECTOR_SEARCH_TOP_K
    chunk_size: int = CHUNK_SIZE
    chunk_conent: bool = True
    score_threshold: int = VECTOR_SEARCH_SCORE_THRESHOLD

    def init_cfg(self,
                 top_k=VECTOR_SEARCH_TOP_K,
                 ):

        self.llm = None
        self.top_k = top_k

    def init_knowledge_vector_store(self,
                                    filepath,
                                    vs_path: str or os.PathLike = None,
                                    sentence_size=SENTENCE_SIZE,
                                    text2vec=None):
        loaded_files = []
        failed_files = []
        if isinstance(filepath, str):
            if not os.path.exists(filepath):
                logger.error("Path Does Not Exist")
                return None
            elif os.path.isfile(filepath):
                file = os.path.split(filepath)[-1]
                try:
                    docs = load_file(filepath, SENTENCE_SIZE)
                    logger.info(f"{file} Successfully loaded")
                    loaded_files.append(filepath)
                except Exception as e:
                    logger.error(e)
                    logger.error(f"{file} Failed to Load Successfully")
                    return None
            elif os.path.isdir(filepath):
                docs = []
                for file in tqdm(os.listdir(filepath), desc="Load file"):
                    fullfilepath = os.path.join(filepath, file)
                    try:
                        docs += load_file(fullfilepath, SENTENCE_SIZE)
                        loaded_files.append(fullfilepath)
                    except Exception as e:
                        logger.error(e)
                        failed_files.append(file)

                if len(failed_files) > 0:
                    logger.error("The Following Files Failed to Load：")
                    for file in failed_files:
                        logger.error(f"{file}\n")

        else:
            docs = []
            for file in filepath:
                docs += load_file(file, SENTENCE_SIZE)
                logger.info(f"{file} Successfully loaded")
                loaded_files.append(file)

        if len(docs) > 0:
            logger.info("File loaded，Generating vector library")
            if vs_path and os.path.isdir(vs_path):
                try:
                    self.vector_store = FAISS.load_local(vs_path, text2vec)
                    self.vector_store.add_documents(docs)
                except:
                    self.vector_store = FAISS.from_documents(docs, text2vec)
            else:
                self.vector_store = FAISS.from_documents(docs, text2vec)  # docs Are a List of Documents

            self.vector_store.save_local(vs_path)
            return vs_path, loaded_files
        else:
            raise RuntimeError("File loading failed，Please check if the file format is correct")

    def get_loaded_file(self, vs_path):
        ds = self.vector_store.docstore
        return set([ds._dict[k].metadata['source'].split(vs_path)[-1] for k in ds._dict])


    # query      Query Content
    # vs_path    Knowledge Base Path
    # chunk_conent   Whether to enable context association
    # score_threshold    Search match score threshold
    # vector_search_top_k   Search Knowledge Base Content Count，Default search for 5 results
    # chunk_sizes    Matching single section content connection context length
    def get_knowledge_based_conent_test(self, query, vs_path, chunk_conent,
                                        score_threshold=VECTOR_SEARCH_SCORE_THRESHOLD,
                                        vector_search_top_k=VECTOR_SEARCH_TOP_K, chunk_size=CHUNK_SIZE,
                                        text2vec=None):
        self.vector_store = FAISS.load_local(vs_path, text2vec)
        self.vector_store.chunk_conent = chunk_conent
        self.vector_store.score_threshold = score_threshold
        self.vector_store.chunk_size = chunk_size

        embedding = self.vector_store.embedding_function.embed_query(query)
        related_docs_with_score = similarity_search_with_score_by_vector(self.vector_store, embedding, k=vector_search_top_k)

        if not related_docs_with_score:
            response = {"query": query,
                        "source_documents": []}
            return response, ""
        # prompt = f"{query}. You should answer this question using information from following documents: \n\n"
        prompt = f"{query}. You must use the information contained in the following document to answer this question: \n\n---\n\n"
        prompt += "\n\n".join([f"({k}): " + doc.page_content for k, doc in enumerate(related_docs_with_score)])
        prompt += "\n\n---\n\n"
        prompt = prompt.encode('utf-8', 'ignore').decode()   # avoid reading non-utf8 chars
        # logger.info(prompt)
        response = {"query": query, "source_documents": related_docs_with_score}
        return response, prompt




def construct_vector_store(vs_id, vs_path, files, sentence_size, history, one_conent, one_content_segmentation, text2vec):
    for file in files:
        assert os.path.exists(file), "Input File Does Not Exist：" + file
    import nltk
    if NLTK_DATA_PATH not in nltk.data.path: nltk.data.path = [NLTK_DATA_PATH] + nltk.data.path
    local_doc_qa = LocalDocQA()
    local_doc_qa.init_cfg()
    filelist = []
    if not os.path.exists(os.path.join(vs_path, vs_id)):
        os.makedirs(os.path.join(vs_path, vs_id))
    for file in files:
        file_name = file.name if not isinstance(file, str) else file
        filename = os.path.split(file_name)[-1]
        shutil.copyfile(file_name, os.path.join(vs_path, vs_id, filename))
        filelist.append(os.path.join(vs_path, vs_id, filename))
    vs_path, loaded_files = local_doc_qa.init_knowledge_vector_store(filelist, os.path.join(vs_path, vs_id), sentence_size, text2vec)

    if len(loaded_files):
        file_status = f"Added {'、'.join([os.path.split(i)[-1] for i in loaded_files if i])} Content to knowledge base，And the knowledge base has been loaded，Please Begin Your Question"
    else:
        pass
        # file_status = "File未成功加载，请重新Upload file"
    # logger.info(file_status)
    return local_doc_qa, vs_path

@Singleton
class knowledge_archive_interface():
    def __init__(self) -> None:
        self.threadLock = threading.Lock()
        self.current_id = ""
        self.kai_path = None
        self.qa_handle = None
        self.text2vec_large_chinese = None

    def get_chinese_text2vec(self):
        if self.text2vec_large_chinese is None:
            # < ------------------- Preheating text vectorization module--------------- >
            from void_terminal.toolbox import ProxyNetworkActivate
            logger.info('Checking Text2vec ...')
            from langchain.embeddings.huggingface import HuggingFaceEmbeddings
            with ProxyNetworkActivate('Download_LLM'):    # Temporarily activate proxy network
                self.text2vec_large_chinese = HuggingFaceEmbeddings(model_name="GanymedeNil/text2vec-large-chinese")

        return self.text2vec_large_chinese


    def feed_archive(self, file_manifest, vs_path, id="default"):
        self.threadLock.acquire()
        # import uuid
        self.current_id = id
        self.qa_handle, self.kai_path = construct_vector_store(
            vs_id=self.current_id,
            vs_path=vs_path,
            files=file_manifest,
            sentence_size=100,
            history=[],
            one_conent="",
            one_content_segmentation="",
            text2vec = self.get_chinese_text2vec(),
        )
        self.threadLock.release()

    def get_current_archive_id(self):
        return self.current_id

    def get_loaded_file(self, vs_path):
        return self.qa_handle.get_loaded_file(vs_path)

    def answer_with_archive_by_id(self, txt, id, vs_path):
        self.threadLock.acquire()
        if not self.current_id == id:
            self.current_id = id
            self.qa_handle, self.kai_path = construct_vector_store(
                vs_id=self.current_id,
                vs_path=vs_path,
                files=[],
                sentence_size=100,
                history=[],
                one_conent="",
                one_content_segmentation="",
                text2vec = self.get_chinese_text2vec(),
            )
        VECTOR_SEARCH_SCORE_THRESHOLD = 0
        VECTOR_SEARCH_TOP_K = 4
        CHUNK_SIZE = 512
        resp, prompt = self.qa_handle.get_knowledge_based_conent_test(
            query = txt,
            vs_path = self.kai_path,
            score_threshold=VECTOR_SEARCH_SCORE_THRESHOLD,
            vector_search_top_k=VECTOR_SEARCH_TOP_K,
            chunk_conent=True,
            chunk_size=CHUNK_SIZE,
            text2vec = self.get_chinese_text2vec(),
        )
        self.threadLock.release()
        return resp, prompt