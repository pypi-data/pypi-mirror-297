from transformers import TableTransformerForObjectDetection
import torch
import pure_cv as vc
import numpy as np
from .config import config
from moveread import tatr 

def pad_bbox(bbox, *, l=0.05, t=0.05, r=0.05, b=0.05):
  (x0, y0), (x1, y1) = bbox
  w, h = x1-x0, y1-y0
  top = y0 - t*h
  left = x0 - l*w
  bottom = y1 + b*h
  right = x1 + r*w
  return np.array([[left, top], [right, bottom]])

class TableDetector(TableTransformerForObjectDetection):

  def __init__(self, config=config):
    super().__init__(config)
    self.config = config

  def predict(self, img: vc.Img) -> tatr.Preds:
    x = tatr.preprocess(img)
    out = self(x[None, ...].to(self.device))
    return tatr.decode(out)

  def detect(self, img: vc.Img) -> vc.Contours:
    """2-step box detection
    1. Crop to grid
    2. Detect cells
    """
    out1 = self.predict(img)

    h, w = img.shape[:2]
    grid = out1['grid'].reshape(2, 2) * [w, h]
    (x1, y1), (x2, y2) = pad_bbox(grid).round().astype(int).clip(0, [w, h])

    bboxes = self.predict(img[y1:y2, x1:x2])['cell']
    cnts = vc.bbox2contour(bboxes.reshape(-1, 2, 2))

    t = np.array([x1, y1])
    s = [x2, y2] - t
    return (cnts*s + t) / [w, h] # relative w.r.t. original image

  def load(self, weights_path: str):
    self.load_state_dict(torch.load(weights_path, weights_only=True))