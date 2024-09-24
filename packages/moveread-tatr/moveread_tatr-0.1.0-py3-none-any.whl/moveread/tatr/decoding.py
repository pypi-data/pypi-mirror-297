from typing_extensions import TypedDict, Mapping
from transformers.models.table_transformer.modeling_table_transformer import TableTransformerObjectDetectionOutput
import pure_cv as vc
import numpy as np
from .contours import center2corner
from .config import config

class Preds(TypedDict):
  cell: vc.Contours
  pair: vc.Contours
  block: vc.Contours
  grid: vc.Contours

def decode(
  output: TableTransformerObjectDetectionOutput, *,
  id2label: Mapping[int, str] = config.id2label
) -> Preds:
  
  m = output.logits.softmax(-1).max(-1)
  pred_labels = list(m.indices.detach().cpu().numpy())[0]
  pred_bboxes = center2corner(output.pred_boxes.detach()).cpu().numpy()[0]

  out = {'cell': [], 'pair': [], 'block': [], 'grid': []}
  for label, bbox in zip(pred_labels, pred_bboxes):
    if (lab := id2label.get(int(label))):
      out[lab].append(bbox)
  
  return { k: np.stack(v) for k, v in out.items() } # type: ignore

