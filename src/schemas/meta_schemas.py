from pydantic import BaseModel
from datetime import datetime, timezone
import json


class Meta(BaseModel):
  created_by: int
  updated_by: int
  created_at: datetime
  updated_at: datetime

  def to_json(self):
    return json.dumps({
      "created_by": self.created_by,
      "updated_by": self.updated_by,
      "created_at": self.created_at,
      "updated_at": self.updated_at,
    }, default=str)
  
  @staticmethod
  def add_meta(model, creator_id):
    now = datetime.now(timezone.utc)
    model.meta = Meta(
      created_by=creator_id,
      updated_by=creator_id,
      created_at=now,
      updated_at=now
    ).to_json()
  
  @staticmethod
  def update_meta(model, updator_id):
    now = datetime.now(timezone.utc)
    meta = Meta(**json.loads(model.meta)) if isinstance(model.meta, str) else model.meta
    meta.updated_by = updator_id
    meta.updated_at = now
    model.meta = meta.to_json()

  @staticmethod
  def deserialize_meta(model):
    model.meta = Meta(**json.loads(model.meta)) if isinstance(model.meta, str) else model.meta

  @staticmethod
  def deserialize_meta_foreach(list):
    for model in list:
      Meta.deserialize_meta(model)
  
