import jsonUtility
from dataclasses import dataclass
from typing import NamedTuple, List, Set, Dict

@dataclass(init=False)
class Config:
  msbuildOptions: str
  repoDir: str
  deployDir: str
  slnFileSubPaths: List[str]
  headerOnlySubDirs: List[str]

def parse(path):
  json = jsonUtility.loadJsonData(path)
  r = Config()

  r.msbuildOptions = json["msbuildOptions"]
  r.repoDir = json["repoDir"]
  r.deployDir = json["deployDir"]
  
  r.slnFileSubPaths = [e for e in json["slnFileSubPaths"]]
  r.headerOnlySubDirs = [e for e in json["headerOnlySubDirs"]]

  return r