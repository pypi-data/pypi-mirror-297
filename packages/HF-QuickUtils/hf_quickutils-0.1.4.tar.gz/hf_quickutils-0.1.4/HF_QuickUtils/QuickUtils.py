from huggingface_hub import snapshot_download
from transformers import AutoTokenizer, AutoModel, pipeline


class QuickDownload:
    def __init__(self, repo, local="", name="", hf_home=""):
        from HF_QuickUtils import get_hf_home
        self.repo = repo
        self.hf_home = get_hf_home() if hf_home == "" else hf_home #设置hf_home
        if name == "":  # 如果未设置名称 则模型名称设置为仓库名
            self.modelName = repo
        else:
            self.modelName = name
        if local == "":  # 如果local为空 则将模型下载到默认路径
            self.local = self.hf_home + "/" + repo
        else:  # 否则下载到指定路径
            self.local = local

    def download(self, max_workers=8) -> str:
        print("Waiting for download...")
        #使用snapshot_download下载模型
        snapshot_download(
            repo_id=self.repo,
            local_dir=self.local,
            max_workers=max_workers,
        )
        print("Download complete!")
        return self.local


class QuickLoader:
    def __setup__(self):
        self.processor = None
        print("初始化")

    def __init__(self, repo="", local="", maxworkers=8, tokenizer_type=AutoTokenizer, model_type=AutoModel,
                 processor_type=None, device="cpu"):
        # 初始化下载连接和仓库
        self.repo = repo
        self.local = local
        self.__setup__()
        self.device = device

        if repo != "" and local != "":
            self.local = QuickDownload(repo=repo, local=local).download(maxworkers)
        elif repo != "":
            self.local = QuickDownload(repo=repo).download(maxworkers)
        elif local != "":
            self.local = local
        elif repo == "" and local == "":
            raise Exception("Error You need to specify at least one of the <repo> and <local>")
        self.tokenizer = tokenizer_type.from_pretrained(self.local, device=device)
        self.model = model_type.from_pretrained(self.local)
        if processor_type is not None:
            self.processor = processor_type.from_pretrained(self.local, device=device)

    def get_model_and_tokenizer(self):
        return self.model, self.tokenizer

    def get_processor(self):
        return self.processor

    def get_pipeline(self, pipeline_type):
        return pipeline(pipeline_type, model=self.model, tokenizer=self.tokenizer, image_processor=self.processor,
                        device=self.device,)